import fitz  # PyMuPDF
import pdfplumber
import io


def extract_text(pdf_bytes: bytes) -> str:
    """Extract all text from PDF, page by page."""
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            if page_text.strip():
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page_text
    return text.strip()


def extract_tables(pdf_bytes: bytes) -> list:
    """Extract all tables from PDF as list of lists."""
    all_tables = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                if table:
                    all_tables.append({
                        "page": page_num + 1,
                        "data": table
                    })
    return all_tables


def extract_images(pdf_bytes: bytes) -> list:
    """Extract all embedded images from PDF."""
    images = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page_num, page in enumerate(doc):
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                images.append({
                    "page": page_num + 1,
                    "index": img_index + 1,
                    "extension": base_image["ext"],
                    "bytes": base_image["image"]
                })
    return images


def extract_all(pdf_bytes: bytes) -> dict:
    """Run all three extractors and return combined result."""
    print("Extracting text...")
    text = extract_text(pdf_bytes)

    print("Extracting tables...")
    tables = extract_tables(pdf_bytes)

    print("Extracting images...")
    images = extract_images(pdf_bytes)

    return {
        "text": text,
        "tables": tables,
        "images": images,
        "stats": {
            "text_length": len(text),
            "table_count": len(tables),
            "image_count": len(images)
        }
    }