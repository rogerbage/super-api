import docx
from io import BytesIO

class file_to_text:
    def docxToText(file):
        if file and file.filename.endswith('.docx'):
            file_stream = BytesIO(file.read())
            doc = docx.Document(file_stream)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            return '\n'.join(fullText)
        return "not docx"
