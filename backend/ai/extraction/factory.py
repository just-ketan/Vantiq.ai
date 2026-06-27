from ai.extraction.txt import TxtExtractor

class ExtractorFactory:
    def __init__(self):
        self.extractors = [
            TxtExtractor(),
        ]

    def get_extractor(self, mime_type: str):
        for extractor in self.extractors:
            if extractor.supports(mime_type):
                return extractor
        raise ValueError(
            f"No extractor registered for '{mime_type}'"
        )