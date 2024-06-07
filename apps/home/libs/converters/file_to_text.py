import docx
import io
import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader


class file_to_text:

    #############################################################
    def docxToText(file):
        if file and file.filename.endswith('.docx'):
            file_stream = BytesIO(file.read())
            doc = docx.Document(file_stream)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            return '\n'.join(fullText)
        return False
    #############################################################


    #############################################################
    def xlsxToHtml(file):
        if file and file.filename.endswith('.xlsx'):
            file_stream = BytesIO(file.read())
            # df = pd.read_excel(file_stream)
            xlsx = pd.ExcelFile(file_stream)

            html_tables = []
            for sheet_name in xlsx.sheet_names:
                df = pd.read_excel(xlsx, sheet_name=sheet_name)
                html_table = df.to_html(index=False)
                html_tables.append(f"<h2>{sheet_name}</h2>\n{html_table}")

            return '\n'.join(html_tables)
        return False

    #############################################################


    #############################################################
    def xlsxToCsv(file):
        if file and file.filename.endswith('.xlsx'):

            file_stream = BytesIO(file.read())
            xlsx = pd.ExcelFile(file_stream)
            all_csv_text = ""

            for sheet_name in xlsx.sheet_names:
                df = pd.read_excel(xlsx, sheet_name=sheet_name)
                buffer = io.StringIO()
                df.to_csv(buffer, index=False)
                csv_text = buffer.getvalue()
                buffer.close()
                all_csv_text += f"# {sheet_name}\n"
                all_csv_text += csv_text + "\n"

            return all_csv_text
        return False

    #############################################################


    #############################################################
    def pdfToText(file):
        if file and file.filename.endswith('.pdf'):
            file_stream = BytesIO(file.read())
            reader = PdfReader(file_stream)
            concat = ""

            for page in reader.pages:
                concat += page.extract_text()

            return concat
        return False

    #############################################################