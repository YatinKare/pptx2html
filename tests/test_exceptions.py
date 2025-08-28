import pytest
from pptx2html.exceptions import (
    ErrorCode,
    InputFileError,
    OutputWriteError,
    Pptx2HtmlError,
    UnsupportedFeatureWarning,
)


def test_hierarchy_and_catching() -> None:
    err = InputFileError(
        code=ErrorCode.FILE_NOT_FOUND, context={"path": "/x/Deck.pptx"}
    )
    assert isinstance(err, Pptx2HtmlError)
    with pytest.raises(Pptx2HtmlError):
        raise err  # category catch-all works


def test_stringification_uses_template_and_context() -> None:
    err = InputFileError(
        code=ErrorCode.FILE_NOT_FOUND, context={"path": "/x/Deck.pptx"}
    )
    s = str(err)
    assert "E1001" in s
    assert "Deck.pptx" in s
    assert "not found" in s


def test_stringification_accepts_explicit_message_override() -> None:
    err = OutputWriteError(code=ErrorCode.OUTPUT_WRITE_FAILED, message="Disk full")
    assert str(err).endswith("Disk full")


def test_to_dict_roundtrip() -> None:
    err = OutputWriteError(
        code=ErrorCode.OUTPUT_DIR_CREATE_FAILED, context={"path": "/out"}
    )
    d = err.to_dict()
    assert d["code"] == "E2001"
    assert d["name"] == "OUTPUT_DIR_CREATE_FAILED"
    assert d["context"]["path"] == "/out"


def test_warning_type_is_userwarning() -> None:
    assert issubclass(UnsupportedFeatureWarning, UserWarning)
