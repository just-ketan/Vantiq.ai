from dataclasses import dataclass, field

@dataclass
class PageExtraction:
    page_number: int
    text: str

@dataclass
class DocumentExtraction:
    text: str
    pages: list[PageExtraction] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

# the above serves as a contract for every extractor