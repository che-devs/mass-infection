from escpos.printer import Usb
from PIL import Image

class Printer:
    font_height = 36
    x_offset_barcode = 160

    def __init__(self):
        self.p = Usb(0x04b8, 0x0e2a)

    def print_barcode(self, barcode: int):
        # Code39
        #self.p.barcode('123456789', 'CODE39', width=2, height=100, function_type='B')
        # UPC-A
        #self.p.barcode('123456789012', 'UPC-A', width=2, height=100, function_type='A')
        
        data = str(barcode)
        data_12 = data.rjust(12, '0')
        # EAN13
        self.p.barcode(data_12, 'EAN13', width=2, height=100, function_type='A')

    def print_picture(self, image: str):
        img = Image.open(image)
        img = img.convert('L')
        img = img.resize([250,250])

        self.p.image(img)

    def print_text(self, text: str):
        self.p.text(text)

    def cut(self):
        self.p.cut()

    def line_space(self):
        self.p.line_spacing()


if __name__ == "__main__":
    printer = Printer()
    printer.print_text('\nPersönliche Identitätskarte\nBitte gut aufbewahren!\n')
    printer.print_picture('media/person.png')
    printer.print_text('Nummer: 123456789012\n\n')
    printer.print_barcode(1)
    printer.cut()
