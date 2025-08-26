# Project Agents.md Guide for OpenAI Codex

This Agents.md file provides comprehensive guidance for OpenAI Codex and other AI agents working with this codebase.

## Project Structure for OpenAI Codex Navigation

- `opc/` OPC (Open Packaging Conventions) reader
    - Resolves [Content_Types].xml, /_rels/.rels, per-part *.rels, external hyperlinks. Mirrors python-pptx’s opc responsibilities but with simpler names.
- `oxml/` -- Thin XML Thin XML façade for PML elements (read-only).
    - PmlPresentation (exposes slide size), PmlSlide, PmlSlideLayout, PmlSlideMaster, PmlShapeEl (x,y,cx,cy, rot, flip flags), PmlPictureEl (blip rId, srcRect crop), PmlTextBodyEl (paras/runs), PmlBackgroundEl (fill reading), PmlThemeEl (colors, minimal)
    - Each is a convenience reader over lxml Elements; no mutation. The focus is surfacing: slide size (sldSz), transform (xfrm), fill, text runs, placeholders.
- `model/` -- Lightweight object model (read-only)
    - PresentationModel (size, slide list), MasterModel, LayoutModel, SlideModel
    - ShapeModel base + TextBoxModel, PictureModel, PlaceholderModel, GroupModel (flattened absolute boxes), TableModel (placeholder in v1), ChartModel (placeholder in v1)
    - HyperlinkModel (external only), ThemeModel (RGB only as agreed).
- `style/` -- Resolution layer
    - StyleCascade (master → layout → slide → shape inheritance per PML rules), FontResolver (embedded font extraction via fonttools with base64 WOFF2 data-URI @font-face, or Arial fallback with logged substitution), ColorMap (RGB only).
- `measure/` — Units & text measurement
    - Units (EMU↔px; 914,400 EMUs/in → 96 DPI → 1 px = 9525 EMU), TextMeasurer (Pillow/FreeType to estimate wrap, shrink-to-fit), OverflowFitter (reduce font-size or lineHeight until content fits the placeholder rectangle; exact line breaks not required per your updated guidance).
- `raster/` — Images & background
    - ImageExtractor (dereference image rIds to /ppt/media/*), BackgroundRenderer (solid/gradient/pattern/blip → single background.png per slide; gradients/patterns painted with Pillow), ChartRasterizer, TableRasterizer, SmartArtRasterizer (stub in v1; placeholders).
- `render/` — HTML/CSS writer
    - HtmlSlideWriter (generates slideN/slideN.html), CssBuilder (inline `<style>` block), DomTemplates (absolute `<div>` nodes), AriaDebug (optional title/alt attributes on images per H).
    - Keeps all styling inline per slide, no shared CSS files.
- `reporting/` — Fail-soft reporting
    - Issue, IssueLog, ConversionReport (returned by API in debug mode), TraceLogger
- `api.py` — parse_pptx(pptx_file, output_dir, debug=False, feature_flags=None)
    Returns ConversionReport if debug=True.

## Coding Conventions for OpenAI Codex

### General Conventions for Agents.md Implementation

1. Read `DEVELOPER.md` for the overall workflow of the project + testing. 
- OpenAI Codex should follow the existing code style in each file
- Agents.md requires meaningful variable and function names in OpenAI Codex output
- Never run a `python` or `pip` command because we are using `uv`.

### Copy-/mirror-worthy bits from python-pptx
> Context: We are building a python library to convert pptx to html files. We are going to heavily be inspirted from an existing python-pptx library that has features mainly meant for creating powerpoints using xml from scratch but also has a feature to modify existing PowerPoints.

Your goal is to detect if any of the following topics come up in any prompts where we can copy/mirror python-pptx instead of "re-inventing the wheel". If you do detect this: **stop all coding** summarize the goal and its relation to python-pptx in the summaries listed below. You will then receive specific instructions later.

- OPC parts & rels. We’ll mirror the concept of Parts and a Relationships index to walk slide order and dereference images/hyperlinks. In UML you can see CT_Relationships and data flows; we’ll implement a minimalist, read-only vari ant to load .rels and map rId → target. This is essential for images and charts/tables later.
- Slide size and transforms. CT_Presentation.sldSz gives us exact canvas size; BaseShapeElement holds x, y, cx, cy and xfrm. We’ll expose those in Pml*El wrappers, convert EMUs to px, and render absolute `<div style="left:Xpx;top:Ypx;width:Wpx;height:Hpx">`.
- Backgrounds & fills. The background element path is visible (CT_CommonSlideData.bg, CT_BackgroundProperties). We’ll read solid/gradient/pattern/blip and rasterize to background.png every time per your latest rule.
- Pictures. CT_Picture.blipFill with srcRect_* cropping must be applied when placing the `<img>` and potentially by pre-cropping a copied PNG to match the PowerPoint crop rectangle. We’ll preserve external hyperlinks on shapes as anchor tags wrapping the absolutely-positioned node.
- Text runs. Text frames/paragraphs/runs (CT_RegularTextRun) provide run-level styling (font family/size/bold/italic/etc.). We’ll generate nested `<div>s` (not semantic h1..h6) with inline CSS and use white-space: pre-wrap so we don’t need to force `<br>` everywhere. We’ll shrink-to-fit if needed to stay inside the shape rectangle.

## Testing Requirements for OpenAI Codex

OpenAI Codex should run tests with the following commands:

```bash

# Run pre-commit hooks
pre-commit run --all-files

# User-Test package via nox_uv
uv run nox -s user_wheel -- --input "./dev/Test.pptx"

# Run all tests with OpenAI Codex
uv run pytest

```

## Pull Request Guidelines for OpenAI Codex

When OpenAI Codex helps create a PR, please ensure it:

1. Includes a clear description of the changes as guided by Agents.md
2. References any related issues that OpenAI Codex is addressing
3. Ensures all tests pass for code generated by OpenAI Codex
5. Keeps PRs focused on a single concern as specified in Agents.md

## Programmatic Checks for OpenAI Codex

Before submitting changes generated by OpenAI Codex, run:

```bash
# Lint check for OpenAI Codex code
uv run ruff check
```

All checks must pass before OpenAI Codex generated code can be merged. Agents.md helps ensure OpenAI Codex follows these requirements.
