#!/usr/bin/env python3
"""Check technical constraints for a scene-builder blueprint image.

This is a heuristic checker, not an OCR tool. It verifies image size, aspect
ratio, white background ratio, and saturated-color ratio. Label completeness
still needs human review.
"""

from __future__ import annotations

import argparse
import sys

try:
    from PIL import Image, UnidentifiedImageError
except ImportError as exc:  # pragma: no cover
    sys.stderr.write("Pillow is required: pip install Pillow\n")
    raise SystemExit(2) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", help="Path to blueprint image")
    parser.add_argument("--min-width", type=int, default=768, help="Minimum width (default: 768)")
    parser.add_argument("--min-height", type=int, default=768, help="Minimum height (default: 768)")
    parser.add_argument("--max-aspect", type=float, default=2.4, help="Maximum width/height ratio (default: 2.4)")
    parser.add_argument("--white-ratio", type=float, default=0.60, help="Minimum near-white background ratio (default: 0.60)")
    parser.add_argument("--saturation-ratio", type=float, default=0.08, help="Maximum strongly saturated pixel ratio (default: 0.08)")
    parser.add_argument("--white-threshold", type=float, default=0.82, help="Near-white channel threshold 0-1 (default: 0.82)")
    parser.add_argument("--saturation-threshold", type=float, default=0.28, help="Strong-saturation channel span 0-1 (default: 0.28)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        image = Image.open(args.image)
        image = image.convert("RGB")
    except FileNotFoundError:
        sys.stderr.write(f"FAIL: file not found: {args.image}\n")
        return 1
    except UnidentifiedImageError:
        sys.stderr.write(f"FAIL: not a readable image: {args.image}\n")
        return 1

    width, height = image.size
    errors: list[str] = []
    warnings: list[str] = []

    if width < args.min_width or height < args.min_height:
        errors.append(f"image too small: {width}x{height} < {args.min_width}x{args.min_height}")

    aspect = width / height if height else float("inf")
    if aspect > args.max_aspect or (height and width / height < 1 / args.max_aspect):
        warnings.append(f"aspect ratio is extreme: {aspect:.2f}:1")

    sample = image.copy()
    sample.thumbnail((512, 512))
    pixels = list(sample.getdata())
    total = len(pixels)

    near_white = sum(1 for r, g, b in pixels if min(r, g, b) >= args.white_threshold * 255)
    saturated = sum(1 for r, g, b in pixels if max(r, g, b) - min(r, g, b) >= args.saturation_threshold * 255)

    white_ratio = near_white / total if total else 0.0
    saturated_ratio = saturated / total if total else 0.0

    if white_ratio < args.white_ratio:
        errors.append(f"background is not white enough: {white_ratio:.1%} < {args.white_ratio:.1%}")
    if saturated_ratio > args.saturation_ratio:
        warnings.append(f"too many saturated colors: {saturated_ratio:.1%} > {args.saturation_ratio:.1%}")

    print(f"blueprint: {args.image}")
    print(f"size: {width}x{height}, aspect: {aspect:.2f}:1")
    print(f"near-white background: {white_ratio:.1%}")
    print(f"strongly saturated pixels: {saturated_ratio:.1%}")
    print("note: region labels and legend completeness still require human review")

    for message in warnings:
        print(f"WARN: {message}")
    for message in errors:
        print(f"FAIL: {message}")

    if errors:
        print("status: FAIL")
        return 1
    print("status: " + ("WARN" if warnings else "PASS"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
