"""Minimal reporting objects for the public API.

These are intentionally lightweight for the initial hello-world stub. Later, a
more detailed model can track issues, warnings, and tracing information.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ConversionReport:
    """Simple report returned by ``parse_pptx`` when ``debug=True``.

    Attributes
    ----------
    success: bool
        Indicates whether the conversion (stub) completed successfully.
    created_paths: list[str]
        Absolute or relative file paths that were created.
    messages: list[str]
        Human-readable messages summarizing actions or notable events.
    """

    success: bool
    created_paths: list[str] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
