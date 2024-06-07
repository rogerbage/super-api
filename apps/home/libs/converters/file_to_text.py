import docx
import pandas as pd
from io import BytesIO

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