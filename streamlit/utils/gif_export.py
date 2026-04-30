import io
import math
from typing import Any

from PIL import Image, ImageColor, ImageDraw

CANVAS_SIZE = 128
MAX_STROKE_WIDTH = 64


class GifExportError(ValueError):
    """Raised when drawing data cannot be converted into a GIF."""


def export_scene_to_gif(
    scene: dict[str, Any],
    *,
    scale_factor: int = 4,
    frame_duration_ms: int = 45,
    max_frames: int = 180,
) -> bytes:
    strokes, background = _normalize_scene(scene)
    canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), background)
    draw = ImageDraw.Draw(canvas)

    capture_step = _capture_step(strokes, max_frames=max_frames)
    frames = [_snapshot(canvas, scale_factor)]
    segment_count = 0

    for color, points in strokes:
        previous = points[0]
        for current in points[1:]:
            draw.line(
                (previous[0], previous[1], current[0], current[1]),
                fill=color,
                width=current[2],
            )
            previous = current
            segment_count += 1
            if segment_count % capture_step == 0:
                frames.append(_snapshot(canvas, scale_factor))

    final_frame = _snapshot(canvas, scale_factor)
    frames.append(final_frame)
    hold_frames = max(1, round(450 / frame_duration_ms))
    frames.extend(final_frame.copy() for _ in range(hold_frames))

    buffer = io.BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration_ms,
        loop=0,
        optimize=False,
        disposal=2,
    )
    return buffer.getvalue()


def _capture_step(strokes: list[tuple[str, list[tuple[int, int, int]]]], *, max_frames: int) -> int:
    total_segments = sum(len(points) - 1 for _, points in strokes)
    return max(1, math.ceil(total_segments / max(1, max_frames)))


def _snapshot(canvas: Image.Image, scale_factor: int) -> Image.Image:
    if scale_factor <= 1:
        return canvas.copy()
    return canvas.resize(
        (canvas.width * scale_factor, canvas.height * scale_factor),
        Image.Resampling.NEAREST,
    )


def _normalize_scene(
    scene: dict[str, Any],
) -> tuple[list[tuple[str, list[tuple[int, int, int]]]], str]:
    if not isinstance(scene, dict):
        raise GifExportError("Couldn't export GIF because drawing data is invalid.")

    palette = scene.get("palette")
    if not isinstance(palette, list) or not palette:
        raise GifExportError("Couldn't export GIF because palette data is missing.")
    normalized_palette = [_normalize_color(color, fallback="#FFFFFF") for color in palette]

    raw_strokes = scene.get("strokes")
    if not isinstance(raw_strokes, list):
        raise GifExportError("Couldn't export GIF because stroke data is invalid.")

    normalized_strokes: list[tuple[str, list[tuple[int, int, int]]]] = []
    for raw_stroke in raw_strokes:
        if not isinstance(raw_stroke, dict):
            continue

        color_index = raw_stroke.get("color", 0)
        if not isinstance(color_index, int) or not 0 <= color_index < len(normalized_palette):
            color_index = 0

        raw_points = raw_stroke.get("shape")
        if raw_points is None:
            raw_points = raw_stroke.get("points")
        points = _normalize_points(raw_points)
        if len(points) < 2:
            continue

        normalized_strokes.append((normalized_palette[color_index], points))

    if not normalized_strokes:
        raise GifExportError("Add at least one stroke before exporting a GIF.")

    background = _normalize_color(scene.get("bg_color", "#03070F"), fallback="#03070F")
    return normalized_strokes, background


def _normalize_points(raw_points: Any) -> list[tuple[int, int, int]]:
    if not isinstance(raw_points, list):
        return []

    points: list[tuple[int, int, int]] = []
    for raw_point in raw_points:
        if not isinstance(raw_point, list) or len(raw_point) < 2:
            continue

        try:
            x = int(round(float(raw_point[0])))
            y = int(round(float(raw_point[1])))
        except (TypeError, ValueError):
            continue

        x = max(0, min(CANVAS_SIZE - 1, x))
        y = max(0, min(CANVAS_SIZE - 1, y))

        width = 1
        if len(raw_point) > 2:
            try:
                width = int(round(float(raw_point[2])))
            except (TypeError, ValueError):
                width = 1
        width = max(1, min(MAX_STROKE_WIDTH, width))

        points.append((x, y, width))
    return points


def _normalize_color(color: Any, *, fallback: str) -> str:
    if isinstance(color, str):
        try:
            ImageColor.getrgb(color)
            return color
        except ValueError:
            pass
    return fallback
