from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ErrorCode(Enum):
    # Input errors (E1xxx)
    FILE_NOT_FOUND = ("E1001", "Input file not found: {path}")
    INVALID_PPTX = ("E1002", "Input file is not a valid .pptx: {path}")
    INPUT_READ_FAILED = ("E1003", "Failed to read input file: {path}")

    # Output errors (E2xxx)
    OUTPUT_DIR_CREATE_FAILED = ("E2001", "Could not create output directory: {path}")
    OUTPUT_WRITE_FAILED = ("E2002", "Failed writing file: {path}")

    # Parse/render pipeline (E3xxx)
    XML_PARSE_FAILED = ("E3001", "Invalid or unexpected XML content at {location}")
    THEME_RESOLVE_FAILED = ("E3002", "Failed to resolve theme resource: {resource}")
    FONT_EXTRACT_FAILED = ("E3003", "Failed to extract embedded font: {font_name}")

    # Warnings (W3xxx)  usable for UnsupportedFeatureWarning and report entries
    UNSUPPORTED_FEATURE = (
        "W3001",
        "Unsupported feature rendered as placeholder: {feature}",
    )
    RASTERIZED_FALLBACK = ("W3002", "Element rasterized to image: {element}")

    def code(self) -> str:
        return self.value[0]

    def default_message(self) -> str:
        return self.value[1]


@dataclass(eq=False)
class Pptx2HtmlError(Exception):
    """
    Base exception for the library. Always carries a machine-readable ErrorCode
    and a human-friendly message. Optional `context` can include any details
    helpful for logs or telemetry.
    """

    code: ErrorCode
    message: str | None = None
    context: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.message is None:
            # Fill from template; missing keys just render as-is.
            try:
                self.message = self.code.default_message().format(**self.context)
            except Exception:
                self.message = self.code.default_message()
        super().__init__(self.message)

    def __str__(self) -> str:
        # Compact and readable: "E1001 Input file not found: /path/file.pptx"
        return f"{self.code.code()} {self.message}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code.code(),
            "name": self.code.name,
            "message": self.message,
            "context": dict(self.context),
        }


#  High-level categories 


class InputFileError(Pptx2HtmlError):
    """Problems reading or validating the input .pptx (path, format, zip, content-types)."""


class OutputWriteError(Pptx2HtmlError):
    """Problems creating or writing the output directory/files."""


# You'll likely add these later for clarity in the pipeline:
class ParseError(Pptx2HtmlError):
    """XML/theme/model parsing errors."""


class RenderError(Pptx2HtmlError):
    """HTML/CSS generation or rasterization failures."""


#  Fail-soft warnings 


class UnsupportedFeatureWarning(UserWarning):
    """
    Emitted (optionally) via `warnings.warn` when we skip or degrade rendering
    for an unsupported element; also collected into ConversionReport.
    """

    pass
