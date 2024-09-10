import os
from generator import read_barcode_list, code2img
import configparser

from pdfgen import PdfGen

properties = configparser.ConfigParser()  ## 클래스 객체 생성

properties.read('config.ini')  ## 파일 읽기

config = properties["BARCODE"] ## 섹션 선택
input_file = config['input_file']
output_folder = config['output_folder']
barcode_type = config['barcode_type']
output_folder_svg = os.path.join(output_folder, "svgs")
output_folder_pdf = os.path.join(output_folder, "pdfs")

for folder in [output_folder, output_folder_pdf, output_folder_svg]:
    try:
        os.mkdir(folder)
    except :
        pass

barcode_list = read_barcode_list(input_file)

merge_barcode_list = ""

for cnt, code in enumerate(barcode_list):
    group, merge_barcode_group = code2img(code, output_folder_svg, cnt)
    if group is None:
        continue
    merge_barcode_list += merge_barcode_group
#
#     pdf_gen = PdfGen()
#     pdf_gen.makePdf(group.childNodes, os.path.join(output_folder_pdf,str(code))+".pdf")

with open("./merge_temp.svg", "r") as read_file:
    svg_xml = read_file.read()
    result_xml = svg_xml.replace("${SVG_LIST}", merge_barcode_list)
    
    with open(os.path.join(output_folder,"merge_barcodes.svg"), "w", encoding='utf-8') as write_file:
        write_file.write(result_xml)
        