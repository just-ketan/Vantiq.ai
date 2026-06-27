from ai.extraction.factory import ExtractorFactory
from models.document import Document

class IngestionPipeline:
    def __init__(self):
        self.extractor_factory = ExtractorFactory()

    def extract_document(self, document: Document):
        extractor = self.extractor_factory.get_extractor(document.mime_type)
        extraction = extractor.extract(document.upload.storage_path)
        return extraction