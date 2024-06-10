import docx
import io
import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader
from apps.home.libs.chat import chats


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


    #############################################################
    def fileToText(file):
        text = ""
        if file:
            if file.filename.endswith('.pdf'):
                text = file_to_text.pdfToText(file)
            elif file.filename.endswith('.txt'):
                text = file.read()
            elif file.filename.endswith('.json'):
                text = file.read()
            elif file.filename.endswith('.xml'):
                text = file.read()
            elif file.filename.endswith('.html'):
                text = file.read()
            elif file.filename.endswith('.csv'):
                text = file.read()
            elif file.filename.endswith('.docx'):
                text = file_to_text.docxToText(file)
            elif file.filename.endswith('.xlsx'):
                text = file_to_text.xlsxToHtml(file) 

        return text

    #############################################################


    ##################################################################
    def chatFile(data):
        
        text = file_to_text.fileToText(data['file'])
        if (not text):
            return "Invalid or empty file", 400
        

        slices = file_to_text.slice_string(text, 32000)
        print("LEN SLICES: "+ str(len(slices)))
        resposta = chats.modeloRefinaResposta(slices, data['prompt'])
        # file_info = {
        #     'prompt': data['prompt'] ,
        #     'file_text': text,
        # }

        # prompt_1 = (
        #     f"Precisamos consultar o documento abaixo;\n"
        #     f"Responda ao 'Comando' baseado no documento;\n"
        #     f"Utilize apenas o documento como contexto. Evite utilizar informação externa.\n\n"
        #     f"/////\n"
        #     f"Comanando: \n"
        #     f"{data['prompt']}\n"
        #     f"/////\n\n"
        #     f"/////\n"
        #     f"Documento: \n"
        #     f"{text}\n"
        #     f"/////\n\n"
        # )

        # resposta = chats.basicOpenai(prompt_1)

        return resposta
    ##################################################################


    ##################################################################
    def slice_string(string, max_size):
        slices = []
        
        for i in range(0, len(string), max_size):
            slices.append(string[i:i+max_size])
        
        return slices
    ##################################################################
