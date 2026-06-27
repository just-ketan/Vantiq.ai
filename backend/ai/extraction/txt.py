from pathlib import Path

from ai.extraction.base import BaseExtractor
from ai.schemas.extraction import (DocumentExtraction,PageExtraction,)
from core.logger import logger

class TxtExtractor(BaseExtractor):
    SUPPORTED_TYPES = {
        "text/plain",
    }

    def supports(self, mime_type: str) -> bool:
        return mime_type in self.SUPPORTED_TYPES

    def extract(self, file_path: str) -> DocumentExtraction:
        logger.info(
            "Extracted TXT document '%s'",
            file_path,
        )
        text = Path(file_path).read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return DocumentExtraction(
            text=text,
            pages=[
                PageExtraction(
                    page_number=1,
                    text=text,
                )
            ],
            metadata={
                "page_count": 1,
            },
        )