from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_file):

    try:
        # File ko beginning par le jao
        pdf_file.seek(0)

        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    except Exception as e:

        print("PDF Error:", e)

        return ""