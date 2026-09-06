import fitz  # PyMuPDF
import csv
import io

def parse_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file."""
    text = ""
    try:
        # Open PDF from bytes
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

def parse_csv(file_bytes: bytes) -> list[dict]:
    """Parses a CSV file and returns a list of dictionaries."""
    try:
        # Decode bytes to string
        content = file_bytes.decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        return [row for row in reader]
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return []

def parse_text(file_bytes: bytes) -> str:
    """Parses a plain text file."""
    try:
        return file_bytes.decode('utf-8').strip()
    except Exception as e:
        print(f"Error parsing text: {e}")
        return ""
