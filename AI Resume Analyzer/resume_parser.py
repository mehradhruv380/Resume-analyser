from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):

    try:
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