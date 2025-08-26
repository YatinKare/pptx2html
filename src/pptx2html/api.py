from __future__ import annotations

from pathlib import Path

from pptx2html.reporting.report import ConversionReport

__all__ = ["parse_pptx"]


_WHITE_PNG_1X1 = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\x9cc``\xf8\xff\xff?\x00\x05\xfe\x02\xfeA\x85\xe1\xb7\x00\x00\x00\x00IEND\xaeB`\x82"


def parse_pptx(
    input_path: str | Path, output_dir: str | Path, debug: bool = False
) -> ConversionReport | None:
    """Create a hello-world output layout for a PPTX conversion.

    Parameters
    ----------
    input_path: str | Path
        Path to a ``.pptx`` file. Presence is validated but not parsed.
    output_dir: str | Path
        Directory where the output structure is created.
    debug: bool
        When ``True``, returns a ``ConversionReport`` describing created paths.

    Returns
    -------
    Optional[ConversionReport]
        ``ConversionReport`` if ``debug=True``, otherwise ``None``.
    """

    input_pptx = Path(input_path)
    if not input_pptx.is_file():
        raise FileNotFoundError(f"PPTX not found: {input_pptx}")

    out_root = Path(output_dir)
    slide_dir = out_root / "output_presentation" / "slide1"
    media_dir = slide_dir / "media"

    # Ensure directories exist
    media_dir.mkdir(parents=True, exist_ok=True)

    # Write a blank white PNG as the background placeholder
    # Note: keep the filename extension consistent with the PNG bytes below.
    background_png = media_dir / "background.png"
    if not background_png.exists():
        background_png.write_bytes(_WHITE_PNG_1X1)

    # Minimal fixed-size canvas that should avoid scrollbars on typical laptops
    # at 100% zoom. Using a 16:9 canvas of 960x540.
    slide_html = slide_dir / "slide1.html"
    html_content = _build_minimal_slide_html(width_px=960, height_px=540)
    slide_html.write_text(html_content, encoding="utf-8")

    if debug:
        return ConversionReport(
            success=True,
            created_paths=[str(slide_html), str(background_png)],
            messages=["Created hello-world slide output."],
        )
    return None


def _build_minimal_slide_html(*, width_px: int, height_px: int) -> str:
    """Return a minimal HTML document with inline styles for a single slide.

    The background image is referenced at ``media/background.png`` relative to
    the slide HTML.
    """

    import htpy as h

    css = (
        "html, body { margin:0; padding:0; background:#ffffff; overflow:hidden; }\n"
        + ".slide-canvas { position:relative; width:"
        + str(width_px)
        + "px; height:"
        + str(height_px)
        + "px; background-color:#ffffff; background-image:url(media/background.png); "
        + "background-repeat:no-repeat; background-size:cover; background-position:center; }\n"
        + "/* Shapes/content will be absolutely positioned within .slide-canvas */\n"
    )

    # htpy elements use [] for children and () for attributes
    doc = h.html[
        h.head[
            h.meta(charset="utf-8"),
            h.meta(name="viewport", content="width=device-width, initial-scale=1"),
            h.title["slide1"],
            h.style[css],
        ],
        h.body[h.div(class_="slide-canvas", aria_label="Slide 1"),],
    ](lang="en")

    # htpy's html element already emits the <!doctype html>
    return str(doc) + "\n"
