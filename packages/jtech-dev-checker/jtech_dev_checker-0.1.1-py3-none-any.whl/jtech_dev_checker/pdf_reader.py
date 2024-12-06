from PyPDF2 import PdfReader

def extract_manifesto_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Erro ao processar o manifesto: {e}")