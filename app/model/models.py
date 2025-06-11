from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.config.logging import setup_logger
from app.exception.custom_exceptions import (
    EmptyTextError,
    InvalidStyleError,
    TextTooLongError,
)
from app.model.enums import StyleEnum

logger = setup_logger(__name__)


class RewriteRequest(BaseModel):
    """Request model for the rewrite endpoint."""

    text: str
    style: str = "formal"

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise EmptyTextError()
        if len(v) > 5000:
            raise TextTooLongError()
        return v.strip()

    @field_validator("style")
    @classmethod
    def validate_style(cls, v: str) -> str:
        valid_styles = ["pirate", "haiku", "formal"]
        if v not in valid_styles:
            raise InvalidStyleError(valid_styles)
        return v


class RewriteResponse(BaseModel):
    """Response model for the rewrite endpoint."""

    original_text: str
    rewritten_text: str
    style: Optional[StyleEnum] = None


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: Literal["ok"] = Field(..., description="Health status")
