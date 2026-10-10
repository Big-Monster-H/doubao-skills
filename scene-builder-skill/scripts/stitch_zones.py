#!/usr/bin/env python3
"""Paste a high-detail zone patch onto a base image at a chosen position.

This is a deterministic local-patch helper. It does not perform AI stitching;
the scene-builder workflow should normally regenerate the full scene instead.
"""

from __future__ import annotations

import argparse
import sys

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError as exc:  # pragma: no cover
    sys.stderr.write("Pillow is required: pip install Pillow\n")
    raise SystemExit(2) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Base image")
    parser.add_argument("--patch", required=True, help="High-detail patch image")
    parser.add_argument("--output", required=True, help="Output image")
    parser.add_argument("--x", type=int, help="Left position of patch on base")
    parser.add_argument("--y", type=int, help="Top position of patch on base")
    parser.add_argument("--width", type=int, help="Patch width; preserves aspect if height omitted")
    parser.add_argument("--height", type=int, help="Patch height; preserves aspect if width omitted")
    parser.add_argument("--opacity", type=float, default=1.0, help="Patch opacity 0-1 (default: 1)")
    parser.add_argument("--feather", type=int, default=0, help="Feather edge in pixels (default: 0)")
    return parser.parse_args()


def resize_patch(patch: Image.Image, width: int | None, height: int | None) -> Image.Image:
    if width and height:
        return patch.resize((width, height), Image.Resampling.LANCZOS)
    if width:
        ratio = width / patch.width
        return patch.resize((width, round(patch.height * ratio)), Image.Resampling.LANCZOS)
    if height:
        ratio = height / patch.height
        return patch.resize((round(patch.width * ratio), height), Image.Resampling.LANCZOS)
    return patch


def make_mask(size: tuple[int, int], feather: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    inset = max(0, min(feather, size[0] // 2, size[1] // 2))
    draw.rectangle([inset, inset, size[0] - inset, size[1] - inset], fill=255)
    if feather > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(feather))
    return mask


def main() -> int:
    args = parse_args()
    try:
        base = Image.open(args.base).convert("RGBA")
        patch = Image.open(args.patch).convert("RGBA")
    except FileNotFoundError as exc:
        sys.stderr.write(f"ERROR: {exc}\n")
        return 2

    patch = resize_patch(patch, args.width, args.height)
    x = args.x if args.x is not None else max(0, (base.width - patch.width) // 2)
    y = args.y if args.y is not None else max(0, (base.height - patch.height) // 2)

    if x < 0 or y < 0 or x + patch.width > base.width or y + patch.height > base.height:
        sys.stderr.write("ERROR: patch placement falls outside the base image.\n")
        return 2

    mask = make_mask(patch.size, args.feather)
    if args.opacity < 1.0:
        mask = mask.point(lambda p: int(p * max(0.0, min(1.0, args.opacity))))

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer.paste(patch, (x, y), mask)
    result = Image.alpha_composite(base, layer)

    if args.output.lower().endswith((".jpg", ".jpeg")):
        result.convert("RGB").save(args.output, quality=95)
    else:
        result.save(args.output)
    print(f"saved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
