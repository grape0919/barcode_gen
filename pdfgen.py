from fpdf import FPDF


class PdfGen():
    
    def __init__(self):
        self.pdf_obj = FPDF(unit="mm")
        self.pdf_obj.add_font("yugo330",fname="./윤고딕330.ttf",uni=True)
        self.pdf_obj.set_font("yugo330", size=4.8)
        self.pdf_obj.set_fill_color(0)
        self.pdf_obj.set_draw_color(255)
        self.pdf_obj.add_page()
        
    def makePdf(self, elements, path):
        self.pdf_obj.set_line_width(0)
        # self.pdf_obj.color
        for element in elements:
            x = float(element.getAttribute('x').replace('mm',''))
            y = float(element.getAttribute('y').replace('mm',''))
            if element.tagName == 'rect':
                width = float(element.getAttribute('width').replace('mm',''))
                height = float(element.getAttribute('height').replace('mm',''))
                self.pdf_obj.rect(x,y,width,height,style="F")
            elif element.tagName == 'text':
                text = element.firstChild.data
                self.pdf_obj.font_style = "letter-spacing:0.13em;"
                self.pdf_obj.text(x,y,text)
                
        self.pdf_obj.output(path)