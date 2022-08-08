import os
from barcode import EAN13
import openpyxl
from barcode.writer import SVGWriter, SIZE, COMMENT, _set_attributes, create_svg_object
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

DEFAULT_OPTIONS = {
    "module_width":0.1674,
    "module_height":5.4,
    "font_size":4.8,
    "font_path":"./윤고딕330.ttf",
    "background":"white",
    "dpi":300
}

class CSTWriter(SVGWriter):
    def __init__(self):
        super(CSTWriter, self).__init__()

    def _init(self, code):
        # width, height = self.calculate_size(len(code[0]), len(code))
        width, height = 18, 7.4
        self._document = create_svg_object(self.with_doctype)
        self._root = self._document.documentElement
        attributes = {
            "width": SIZE.format(width),
            "height": SIZE.format(height),
        }
        _set_attributes(self._root, **attributes)
        if COMMENT:
            self._root.appendChild(self._document.createComment(COMMENT))
        # create group for easier handling in 3rd party software
        # like corel draw, inkscape, ...
        group = self._document.createElement("g")
        attributes = {"id": "barcode_group"}
        _set_attributes(group, **attributes)
        self._group = self._root.appendChild(group)
        background = self._document.createElement("rect")
        attributes = {
            "width": "100%",
            "height": "100%",
            "style": f"fill:{self.background}",
        }
        _set_attributes(background, **attributes)
        self._group.appendChild(background)

    def _create_module(self, xpos, ypos, width, color):
        # Background rect has been provided already, so skipping "spaces"
        if color != self.background:
            element = self._document.createElement("rect")
            height = self.module_height
            if len(self._group.childNodes) in [1,2,15,16,29,30]:
                height = height + 1
            attributes = {
                "x": SIZE.format(xpos-4.5),
                "y": SIZE.format(ypos-1.0),
                "width": SIZE.format(width),
                "height": SIZE.format(height),
                "style": f"fill:{color};",
            }
            _set_attributes(element, **attributes)
            self._group.appendChild(element)
            
    def _create_text(self, xpos, ypos):
        # check option to override self.text with self.human (barcode as
        # human readable data, can be used to print own formats)
        if self.human != "":
            barcodetext = self.human
        else:
            barcodetext = self.text
        ypos = 7.1
        element = self._document.createElement("text")
        temp_text = barcodetext[0]
        attributes = {
            "x": SIZE.format(0),
            "y": SIZE.format(ypos),
            "style": "font-family:'윤고딕330';font-size:4.8pt;letter-spacing:0.12em;",
        }
        _set_attributes(element, **attributes)
        text_element = self._document.createTextNode(temp_text)
        element.appendChild(text_element)
        self._group.appendChild(element)
        
        
        element = self._document.createElement("text")
        temp_text = barcodetext[1:7]
        attributes = {
            "x": SIZE.format(2.55),
            "y": SIZE.format(ypos),
            "style": "font-family:'윤고딕330';font-size:4.8pt;letter-spacing:0.12em;",
        }
        _set_attributes(element, **attributes)
        text_element = self._document.createTextNode(temp_text)
        element.appendChild(text_element)
        self._group.appendChild(element)
        
        
        element = self._document.createElement("text")
        temp_text = barcodetext[7:]
        attributes = {
            "x": SIZE.format(10.3),
            "y": SIZE.format(ypos),
            "style": "font-family:'윤고딕330';font-size:4.8pt;letter-spacing:0.12em;",
        }
        _set_attributes(element, **attributes)
        text_element = self._document.createTextNode(temp_text)
        element.appendChild(text_element)
        self._group.appendChild(element)
            # ypos += pt2mm(self.font_size) + self.text_line_distance
MY_WRITER = CSTWriter()

def read_barcode_list(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    number_list = []

    for i in range(0, sheet.max_row):
        for col in sheet.iter_cols(1, sheet.max_column):
            number_list.append(col[i].value)
            
    return number_list

def svg2pdf(file_path):
    f_, ext = os.path.splitext(file_path)
    drawing = svg2rlg(file_path)
    renderPDF.drawToFile(drawing, f_+".pdf")

def code2img(code, output_path):
    str_number = str(code)
    my_barcode = EAN13(str_number, writer=MY_WRITER)#, writer=image_writer)
    file_name = str_number
    output = os.path.join(output_path, file_name)
    my_barcode.save(output ,DEFAULT_OPTIONS)
    return output
    
