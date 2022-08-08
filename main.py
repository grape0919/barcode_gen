from generator import read_barcode_list, code2img, svg2pdf
import configparser

properties = configparser.ConfigParser()  ## 클래스 객체 생성

properties.read('config.ini')  ## 파일 읽기

config = properties["BARCODE"] ## 섹션 선택
input_file = config['input_file']
output_folder = config['output_folder']
# output_type = config['extension']


barcode_list = read_barcode_list(input_file)

for code in barcode_list:
    svg_path = code2img(code, output_folder)
    svg2pdf(svg_path+".svg")