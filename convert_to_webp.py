#!/usr/bin/env python3
"""
Convierte imágenes JPEG a WebP.
Uso:
  python convert_to_webp.py foto.jpg
  python convert_to_webp.py foto1.jpg foto2.jpeg
  python convert_to_webp.py *.jpg
  python convert_to_webp.py carpeta/
  python convert_to_webp.py foto.jpg --quality 90 --output resultado/
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Falta la librería Pillow. Instálala con:")
    print("  pip install Pillow")
    sys.exit(1)

JPEG_EXTENSIONS = {".jpg", ".jpeg", ".JPG", ".JPEG"}


def convert(input_path: Path, output_dir: Path, quality: int) -> bool:
    output_path = output_dir / (input_path.stem + ".webp")
    try:
        with Image.open(input_path) as img:
            img.save(output_path, "WEBP", quality=quality)
        size_before = input_path.stat().st_size / 1024
        size_after = output_path.stat().st_size / 1024
        savings = (1 - size_after / size_before) * 100
        print(f"✓  {input_path.name}  →  {output_path.name}  "
              f"({size_before:.1f} KB → {size_after:.1f} KB, -{savings:.0f}%)")
        return True
    except Exception as e:
        print(f"✗  {input_path.name}: {e}")
        return False


def collect_files(paths: list[str]) -> list[Path]:
    files = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            for ext in JPEG_EXTENSIONS:
                files.extend(path.glob(f"*{ext}"))
        elif path.suffix in JPEG_EXTENSIONS and path.is_file():
            files.append(path)
        else:
            print(f"Ignorado (no es JPEG o no existe): {p}")
    return sorted(set(files))


def main():
    parser = argparse.ArgumentParser(description="Convierte JPEG a WebP")
    parser.add_argument("inputs", nargs="+", help="Archivos o carpetas JPEG")
    parser.add_argument("-q", "--quality", type=int, default=80,
                        help="Calidad WebP 1-100 (default: 80)")
    parser.add_argument("-o", "--output", default=None,
                        help="Carpeta de salida (default: misma que el original)")
    args = parser.parse_args()

    files = collect_files(args.inputs)
    if not files:
        print("No se encontraron archivos JPEG.")
        sys.exit(1)

    print(f"\nConvirtiendo {len(files)} imagen(es) con calidad {args.quality}...\n")
    ok = 0
    for f in files:
        out_dir = Path(args.output) if args.output else f.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        if convert(f, out_dir, args.quality):
            ok += 1

    print(f"\n{ok}/{len(files)} convertida(s) correctamente.")


if __name__ == "__main__":
    main()
