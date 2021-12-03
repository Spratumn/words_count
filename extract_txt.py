from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import re
import os

def get_select_test(pdfpath, start, end):
    print(f'Extracting selected content from {pdfpath}...')
    with open(pdfpath, 'rb') as pdf_file:
        pdf_parse = PDFParser(pdf_file)
        pdf_doc = PDFDocument(pdf_parse)
        if pdf_doc.is_extractable:
            pdf_rm = PDFResourceManager(caching=True)
            pdf_lap = LAParams()
            pdf_pa = PDFPageAggregator(pdf_rm, laparams=pdf_lap)
            pdf_pi = PDFPageInterpreter(pdf_rm, pdf_pa)

        pdf_page = PDFPage.create_pages(pdf_doc)

        text = ''
        is_find_start_page = False
        for index, page in enumerate(pdf_page):
            pdf_pi.process_page(page)
            layout = pdf_pa.get_result()

            page_text = ''
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal): 
                    page_text += x.get_text() + '\n'
            if re.search(start, page_text) and re.search(r'目录', page_text) is None: 
                is_find_start_page = True
                text += page_text
                print(f'Found select content in in page: {index}')
                continue

            if is_find_start_page:
                text += page_text
                print(f'Found select content in in page: {index}')
                if re.search(end, page_text): 
                    break
    txtpath = pdfpath.lower().replace('.pdf', '.txt')
    with open(txtpath, 'w') as out:
        out.write(text)
    get_valid_content(txtpath, start, end)


def get_valid_content(txtpath, start, end):
    with open(txtpath, 'r') as f1:
        orilines = f1.readlines()

    alllines = []
    validline = False
    for line in orilines:
        if not validline:
            if re.search(start, line):
                validline=True
                alllines.append(line.rstrip('\n'))
            continue
        if re.search(end, line):
            break
        alllines.append(line.rstrip('\n'))
    with open(txtpath, 'w') as o1:
        o1.write('\n'.join(alllines))


if __name__ == '__main__':
    pdfdir = './pdf'
    start = r'第.节\s*经营情况讨论与分析\s'
    end = r'第.节\s*.*\s'

    filelist = os.listdir(pdfdir)
    for pdfpath in filelist:
        if not pdfpath.lower().endswith('.pdf'):continue
        get_select_test(os.path.join(pdfdir, pdfpath), start, end)