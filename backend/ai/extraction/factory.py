from ai.extraction.txt import TxtExtractor
from ai.extraction.pdf import PDFExtractor

class ExtractorFactory:
    def __init__(self):
        self.extractors = [
            TxtExtractor(),
            PDFExtractor(),
        ]

    def get_extractor(self, mime_type: str):
        for extractor in self.extractors:
            if extractor.supports(mime_type):
                return extractor
        raise ValueError(
            f"No extractor registered for '{mime_type}'"
        )