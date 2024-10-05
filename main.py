import json
import time

from docx import Document
from docx.shared import Pt
import requests
from bs4 import BeautifulSoup


def write_h2_title_to_docx(doc_name: str, title: str):
    doc = Document(f'{doc_name}.docx')
    doc.add_heading(title, level=2)
    doc.save(f'{doc_name}.docx')
    print(f'-------------{title}寫入成功-{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}-------------')


def write_text_to_docx(doc_name: str, text: str):
    doc = Document(f'{doc_name}.docx')
    para = doc.add_paragraph()
    para.paragraph_format.first_line_indent = Pt(28)
    run = para.add_run(text)
    run.font.name = '华文宋体'
    run.font.size = Pt(14)

    doc.save(f'{doc_name}.docx')


def get_chapter_content(chapterId: str, doc_name: str):
    chapterURL = f'https://www.shidianguji.com/zh/book/LS0026/chapter/{chapterId}'
    response = requests.get(chapterURL).text
    soup = BeautifulSoup(response, 'html.parser')
    p_tag = soup.find_all(class_='IFkbDzn2')
    for para in p_tag:
        write_text_to_docx(doc_name, para.text)
    print(f'-------------{chapterId}寫入成功-------------')


def write_shilu_to_docx(doc_name: str, volume):
    with open(f'mingshilu_{volume}.json', 'r', encoding='utf-8') as f:
        json_content = f.read()
        dict_content = json.loads(json_content)
        for item in dict_content['bookInfo']['catalog']['chapters']:
            chapterName: str = item['chapterName'][0]['content']
            chapterId: str = item['chapterId']
            write_h2_title_to_docx(doc_name, chapterName)
            get_chapter_content(chapterId, doc_name)


def main(name: str = '明實錄', volume_num: int = 13):
    for volume in range(volume_num):
        volume = volume + 1
        document = Document()
        document.save(f'{name}_{volume}.docx')
        write_shilu_to_docx(f'{name}_{volume}', volume)


if __name__ == '__main__':
    main()
