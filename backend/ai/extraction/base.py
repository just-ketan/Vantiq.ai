from abc import ABC, abstractmethod
from ai.schemas.extraction import DocumentExtraction

class BaseExtractor(ABC):
    @abstractmethod
    def supports(self, mime_type: str) -> bool:
        """
        Returns True if this extractor supports the supplied MIME type.
        """
        pass

    @abstractmethod
    def extract(self, file_path: str) -> DocumentExtraction:
        """
        Extract text and metadata from the document.
        """
        pass