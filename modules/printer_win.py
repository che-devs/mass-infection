import win32print
import win32ui
from PIL import Image, ImageWin
from io import BytesIO


class Printer:
    font_height = 36
    x_offset_barcode = 160

    def __init__(self, printer_name: str, my_barcode: any) -> None:
        self.printer_name = printer_name
        self.printer_handle = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(self.printer_handle)
        device_mode = win32print.GetPrinter(self.printer_handle, 2)["pDevMode"]

        self.my_barcode = my_barcode

        self.image_stream = BytesIO()

    def print_job(self, text: str = "", barcode: str = ""):
        self._start_print_job()
        if text != "":
            self._print_text(text)
        if barcode != "":
            self._print_barcode_image_stream(barcode)
        self._close_print_job()

    def _print_barcode(self, data: str):
        self.my_barcode.create_png(data)
        self._print_picture("temp_barcode.png")

    def _print_barcode_image_stream(self, data: str):
        self.image_stream.seek(0)
        barcode = self.my_barcode.create_barcode(data)
        barcode.write(self.image_stream)
        self._print_picture_from_stream()

    def _print_picture_from_stream(self):
        self.hdc.StartPage()
        self.image_stream.seek(0)
        image = Image.open(self.image_stream)
        dib = ImageWin.Dib(image)
        dib.draw(
            self.hdc.GetHandleOutput(),
            (
                self.x_offset_barcode,
                0,
                image.size[0] // 2 + self.x_offset_barcode,
                image.size[1] // 2,
            ),
        )
        self.hdc.EndPage()

    def _print_picture(self, image_path):
        self.hdc.StartPage()
        image = Image.open(image_path)
        dib = ImageWin.Dib(image)
        dib.draw(
            self.hdc.GetHandleOutput(),
            (
                self.x_offset_barcode,
                0,
                image.size[0] // 2 + self.x_offset_barcode,
                image.size[1] // 2,
            ),
        )
        self.hdc.EndPage()

    def _print_text(self, text_to_print: str):
        self.hdc.StartPage()
        font = win32ui.CreateFont(
            {"name": "Arial", "height": self.font_height, "weight": 200}
        )
        self.hdc.SelectObject(font)
        x = 20
        y = 20

        for text in text_to_print.splitlines():
            self.hdc.TextOut(x, y, text)
            y += self.font_height
        self.hdc.TextOut(x, y + self.font_height, "_")
        self.hdc.EndPage()

    def _start_print_job(self):
        self.hdc = win32ui.CreateDC()
        self.hdc.CreatePrinterDC(self.printer_name)
        self.hdc.StartDoc("Taskmanager - Etikette")

    def _close_print_job(self):
        self.hdc.EndDoc()
        # win32print.ClosePrinter(self.printer_name)


if __name__ == "__main__":
    from my_barcode import MyBarcode

    my_barcode = MyBarcode()
    printer = Printer("EPSON TM-m30II Receipt", my_barcode)
    printer.print_job('test_string', '123456789012')
    