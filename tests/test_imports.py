# tests/test_imports.py
# type: ignore
import importlib

import pytest

MODULES = [
    "pptx2html",
    "pptx2html.api",
    "pptx2html.exceptions",
    "pptx2html.utils",
    "pptx2html.utils.units",
    "pptx2html.measure",
    "pptx2html.model",
    "pptx2html.opc",
    "pptx2html.opc.content_types",
    "pptx2html.opc.parts",
    "pptx2html.opc.rels",
    "pptx2html.opc.zip_reader",
    "pptx2html.oxml",
    "pptx2html.raster",
    "pptx2html.render",
    "pptx2html.reporting",
    "pptx2html.reporting.report",
    "pptx2html.style",
]


@pytest.mark.parametrize("module_name", MODULES)
def test_import_module(module_name) -> None:
    importlib.import_module(module_name)
