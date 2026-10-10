#!/usr/bin/env python3
"""Apply a distance fog / atmospheric perspective effect to an image.

Far areas are made cooler, hazier, lower-contrast, and slightly blurred.
Without a depth mask, distance is estimated with a gradient.
"""

from __future__ import annotations

import argparse
import sys

try:
    from PIL import Image, ImageFilter, ImageOps
except ImportError as exc:  # pragma: no cover
    sys.stderr.write("Pillow is required: pip install Pillow\n")
    raise SystemExit(2) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Input image")
    parser.add_argument("output", help="Output image")
    parser.add_argument("--mask", help="Optional grayscale depth mask; white = far")
    parser.add_argument("--gradient", choices=["top", "bottom", "radial"], default="top", help="Distance direction when no mask is provided")
    parser.add_argument("--strength", type=float, default=0.55, help="Fog strength 0-1 (default: 0.55)")
    parser.add_argument("--blur-radius", type=float, default=4.0, help="Gaussian blur radius for far areas (default: 4)")
    parser.add_argument("--fog-color", default="190,210,235", help="Fog RGB color, comma separated (default: 190,210,235)")
    return parser.parse_args()


def parse_color(value: str) -> tuple[int, int, int]:
    parts = [int(part.strip()) for part in value.split(",")]
    if len(parts) != 3 or any(part < 0 or part > 255 for part in parts):
        raise ValueError("fog color must be R,G,B with values 0-255")
    return tuple(parts)  # type: ignore[return-value]


def build_depth(size: tuple[int, int], mask_path: str | None, gradient: str) -> Image.Image:
    if mask_path:
        mask = Image.open(mask_path).convert("L").resize(size, Image.Resampling.LANCZOS)
        return ImageOps.autocontrast(mask)

    if gradient == "radial":
        try:
            return Image.radial_gradient("L").resize(size, Image.Resampling.LANCZOS)
        except AttributeError:
            gradient = "top"

    gradient_image = Image.linear_gradient("L").resize(size, Image.Resampling.LANCZOS)
    if gradient == "top":
        return ImageOps.invert(gradient_image)
    return gradient_image


def main() -> int:
    args = parse_args()
    try:
        fog_color = parse_color(args.fog_color)
    except ValueError as exc:
        sys.stderr.write(f"ERROR: {exc}\n")
        return 2

    try:
        image = Image.open(args.input).convert("RGB")
    except FileNotFoundError:
        sys.stderr.write(f"ERROR: file not found: {args.input}\n")
        return 2

    depth = build_depth(image.size, args.mask, args.gradient)
    blurred = image.filter(ImageFilter.GaussianBlur(args.blur_radius))
    fog = Image.new("RGB", image.size, fog_color)

    fog_mask = depth.point(lambda p: min(255, int(p * args.strength)))
    blur_mask = depth.point(lambda p: min(255, int(p * args.strength * 0.75)))
    desat_mask = depth.point(lambda p: min(255, int(p * args.strength * 0.35)))

    result = Image.composite(fog, image, fog_mask)
    result = Image.composite(blurred, result, blur_mask)
    desaturated = ImageOps.grayscale(result).convert("RGB")
    result = Image.composite(desaturated, result, desat_mask)

    if args.output.lower().endswith((".jpg", ".jpeg")):
        result.save(args.output, quality=95)
    else:
        result.save(args.output)
    print(f"saved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
