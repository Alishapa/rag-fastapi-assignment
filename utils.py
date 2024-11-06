import fitz  # PyMuPDF for PDFs
from docx import Document
from io import BytesIO

async def extract_text_from_file(content: bytes, filename: str) -> str:
    """
    Extracts text from a file based on its extension.
    """
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(content)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(content)
    elif filename.endswith(".txt"):
        return content.decode("utf-8")
    else:
        return ""

def extract_text_from_pdf(content: bytes) -> str:
    """
    Extract text from a PDF file.
    """
    text = ""
    pdf = fitz.open(stream=BytesIO(content), filetype="pdf")
    for page_num in range(pdf.page_count):
        page = pdf.load_page(page_num)
        text += page.get_text("text")
    return text

def extract_text_from_docx(content: bytes) -> str:
    """
    Extract text from a DOCX file.
    """
    text = ""
    docx = Document(BytesIO(content))
    for paragraph in docx.paragraphs:
        text += paragraph.text + "\n"
    return text
