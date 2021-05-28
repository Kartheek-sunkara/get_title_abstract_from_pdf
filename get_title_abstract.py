"""Get title and abstract from pdf"""
import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from tika import parser
from flashtext import KeywordProcessor
KEY_PRO = KeywordProcessor(case_sensitive=False)
from get_font import *
def list_to_string(listvalue):
    """liust to string function"""
    my_string = ' '.join(listvalue)
    return my_string
def get_text(pdf_file):
    """ get pdf data of first page"""
    try:
        file_path = open(pdf_file, 'rb')
        pdf_parser = PDFParser(file_path)
        pdf_document = PDFDocument(pdf_parser)
        if not pdf_document.is_extractable:
            raise PDFTextExtractionNotAllowed
        pdf_rsrcmgr = PDFResourceManager()
        pdf_laparams = LAParams()
        pdf_device = PDFPageAggregator(pdf_rsrcmgr, laparams=pdf_laparams)
        pdf_interpreter = PDFPageInterpreter(pdf_rsrcmgr, pdf_device)
        pdf_textdata = []
        for page in PDFPage.create_pages(pdf_document):
            pdf_interpreter.process_page(page)
            pdf_layout = pdf_device.get_result()
            for obj in pdf_layout._objs:
                if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                    pdf_textdata.append(obj.get_text().replace('\n', '_'))
            break
        return pdf_textdata
    except Exception as error:
        return error
def get_meta_data(pdf_file):
    """get pdf metadata"""
    try:
        parsed_pdf = parser.from_file(pdf_file)
        pdf_meta_data = parsed_pdf["metadata"]
        return pdf_meta_data
    except Exception as error:
        return error
def get_pdf_content(pdf_file):
    """get pdf content"""
    try:
        parsed_pdf = parser.from_file(pdf_file)
        pdf_meta_data = parsed_pdf["content"]
        return pdf_meta_data
    except Exception as error:
        return error
def get_abstract(textdata):
    """get abs related content"""
    data = []
    words = ['A B S T R A C T    _', 'a b s t r a c t_', 'abstract', 'abstract:', 'Abstract:']
    KEY_PRO.add_keywords_from_list(words)
    for sent in textdata:
        found_sent = []
        found_sent = KEY_PRO.extract_keywords(sent)
        if len(found_sent) > 0:
            if len(sent) > 20:
                doi_num = sent
    if len(doi_num) == 0:
        doi_num = max(textdata, key=len)
        for i in textdata:
            if "*" not in i:
                data.append(i)
        doi_num = max(data, key=len)
    return doi_num.replace("_", "")
def journal_abs(meta_data, text_data):
    """get abstract from pdf"""
    try:
        pdf_abs = meta_data.get("subject")
        if pdf_abs != None:
            if len(pdf_abs.split()) < 15:
                pdf_abs = get_abstract(text_data)
                if "KEYWORDS:" in pdf_abs:
                    abstract_lst = pdf_abs.split("KEYWORDS:")
                    abs_content = abstract_lst[0]
                    pdf_abs = abs_content.replace('ABSTRACT:', '')
        elif pdf_abs == None:
            pdf_abs = get_abstract(text_data)
            if "KEYWORDS:" in pdf_abs:
                abstract_lst = pdf_abs.split("KEYWORDS:")
                abs_content = abstract_lst[0]
                pdf_abs = abs_content.replace('ABSTRACT:', '')
        return pdf_abs
    except Exception as error:
        return error
def get_title(textdata):
    """get title related content from pdf"""
    try:
        for i in textdata:
            word = i.split()
            if len(word) >= 10:
                test_list = i.split("_")
                res = [test_list[0], test_list[1]]
                final_title = list_to_string(res)
                title_lst = final_title.split(",")
                if len(title_lst) >=3:
                    index = textdata.index(i)
                    final_text = textdata[:index]
                    final_title = max(final_text, key=len)
                break
        return final_title.replace("_", " ")
    except Exception as error:
        return error
def journal_title(meta_data, text_data, pdf_path):
    """get title based get_title function output"""
    try:
        pdf_titile = meta_data.get("title")
        get_pdf_title = []
        if pdf_titile != None:
            if len(pdf_titile.split()) <= 3:
                get_pdf_title.append(get_title(text_data))
                get_pdf_title.append(get_jour_title(pdf_path))
                pdf_titile = max(get_pdf_title, key=len)
        elif pdf_titile == None:
            get_pdf_title.append(get_title(text_data))
            get_pdf_title.append(get_jour_title(pdf_path))
            pdf_titile = max(get_pdf_title, key=len)
        return pdf_titile
    except Exception as error:
        return error

##PDF Path
PDF_FILE = "C:\\Users\\kartheek.sunkara\\Desktop\\AIML\\meta_data\\pdf\\1532.pdf"
META_TIKA = get_meta_data(PDF_FILE)
PDF_MINR = get_text(PDF_FILE)
ABSTRACT_CONTENT = journal_abs(META_TIKA, PDF_MINR)
print("Abstract:::", ABSTRACT_CONTENT)
TITLE_CONTENT = journal_title(META_TIKA, PDF_MINR, PDF_FILE)
print("Title:::", TITLE_CONTENT)
