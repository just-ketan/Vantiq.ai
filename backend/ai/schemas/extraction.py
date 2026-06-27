from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class PageExtraction:
    page_number: int
    text: str

@dataclass
class DocumentExtraction:
    text: str
    pages: list[PageExtraction] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    mime_type: str = ""
    file_name: str = ""
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    extractor: str = ""
    success: bool = True
    warnings: list[str] = field(default_factory=list)

# the above serves as a contract for every extractor