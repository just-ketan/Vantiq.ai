import fitz
from ai.extraction.base import BaseExtractor
from ai.schemas.extraction import (DocumentExtraction, PageExtraction,)
from models.document import Document

class PDFExtractor(BaseExtractor):
    SUPPORTED_TYPES = {
        "application/pdf",
    }

    def supports(self, mime_type: str) -> bool:
        return mime_type in self.SUPPORTED_TYPES
    
    def extract(self, document: Document) -> DocumentExtraction:
        pdf = fitz.open(document.upload.storage_path)
        pages=[]
        full_text=[]

        for idx, page in enumerate(pdf):
            text = page.get_text()
            pages.append(PageExtraction(
                page_number=idx+1, text=text,
            ))
            full_text.append(text)
        
        metadata = pdf.metadata or {}
        metadata["page_count"] = pdf.page_count
        pdf.close()

        return DocumentExtraction(
            text="\n".join(full_text),
            pages=pages,
            metadata=metadata,
            mime_type=document.mime_type,
            file_name=document.filename,
            extractor="PDFExtractor",
        )
        