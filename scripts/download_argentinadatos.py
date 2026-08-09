import argparse
import json
import os
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def normalize_name(path: str) -> str:
    name = path.strip("/").replace("/", "_")
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
    return name


def default_path_value(parameter: dict) -> str:
    if "example" in parameter:
        return str(parameter["example"])

    schema = parameter.get("schema", {})
    ptype = schema.get("type", "string")
    pname = parameter.get("name", "")

    if pname.lower() in {"año", "anio", "year"}:
        return str(2026)
    if pname.lower().startswith("fecha") or pname.lower().endswith("fecha"):
        return "ultimo"
    if ptype == "integer":
        return str(schema.get("minimum", 0) or 0)
    if "enum" in schema and schema["enum"]:
        return str(schema["enum"][0])
    return "default"


def build_path(path_template: str, parameters: List[Dict[str, Any]]) -> Tuple[str, Dict[str, str]]:
    values: Dict[str, str] = {}
    for param in parameters:
        if param.get("in") != "path":
            continue
        if not param.get("required", False):
            continue
        values[param["name"]] = default_path_value(param)

    built = path_template
    for name, value in values.items():
        built = built.replace("{" + name + "}", value)
    return built, values


def load_openapi(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def fetch_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"User-Agent": "argentinadatos-downloader/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            raise ValueError(f"Respuesta inesperada: {content_type}")
        return json.load(response)


def guess_output_dir(output: Optional[str]) -> Path:
    if output:
        return Path(output).expanduser()

    onedrive = os.environ.get("OneDrive")
    if onedrive:
        return Path(onedrive) / "ArgentinaDatosAPI"

    userprofile = os.environ.get("USERPROFILE")
    if userprofile:
        candidate = Path(userprofile) / "OneDrive" / "ArgentinaDatosAPI"
        if candidate.exists() or candidate.parent.exists():
            return candidate

    return Path.cwd() / "argentinadatos_downloads"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Descarga endpoints de ArgentinaDatos API usando el OpenAPI JSON y guarda los resultados en OneDrive.")
    parser.add_argument(
        "--api",
        default="argentinadatos_api.json",
        help="Archivo OpenAPI JSON (por defecto argentinadatos_api.json)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Carpeta de salida. Si no se indica, usa OneDrive/ArgentinaDatosAPI si está disponible.",
    )
    parser.add_argument(
        "--skip-parameterized",
        action="store_true",
        help="Omitir endpoints que requieren parámetros en la ruta.",
    )
    args = parser.parse_args()

    api_path = Path(args.api)
    if not api_path.exists():
        raise FileNotFoundError(f"No existe el archivo API: {api_path}")

    api = load_openapi(api_path)
    server_url = api.get("servers", [{"url": "https://api.argentinadatos.com"}])[0]["url"].rstrip("/")
    output_dir = guess_output_dir(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Servidor: {server_url}")
    print(f"Salida: {output_dir}")

    for path_template, methods in api.get("paths", {}).items():
        if "get" not in methods:
            continue

        parameters = methods["get"].get("parameters", [])
        required_path = [p for p in parameters if p.get("in") == "path" and p.get("required")]

        if required_path and args.skip_parameterized:
            print(f"Omitiendo {path_template} (requiere parámetros)")
            continue

        if required_path:
            built_path, used = build_path(path_template, required_path)
            if "{" in built_path or "}" in built_path:
                print(f"No se pueden construir todos los parámetros para {path_template}, se omite")
                continue
            actual_path = built_path
        else:
            actual_path = path_template
            used = {}

        url = f"{server_url}{actual_path}"
        filename = normalize_name(actual_path)
        if used:
            suffix = "_" + "_".join(f"{k}-{v}" for k, v in used.items())
            filename = normalize_name(actual_path + suffix)
        output_file = output_dir / filename

        try:
            print(f"Descargando {url} -> {output_file.name}")
            data = fetch_json(url)
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except urllib.error.HTTPError as exc:
            print(f"Error HTTP {exc.code} en {url}: {exc.reason}")
        except Exception as exc:
            print(f"Error en {url}: {exc}")

    print("Descarga finalizada.")


if __name__ == "__main__":
    main()
