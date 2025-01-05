from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

class PDFTableGenerator:
    # def __init__(self, data, columns, footer, file_name="cloth/static/cloth/output.pdf"):
    def __init__(self, data, columns, footer, file_name="/home/honestfabrics/Honest/cloth/static/cloth/output.pdf"):
        self.data = data
        self.columns = columns
        self.footer = footer
        self.file_name = file_name

        # Register an Arabic font
        # pdfmetrics.registerFont(TTFont('Arabic', 'cloth/static/cloth/arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arabic', '/home/honestfabrics/Honest/cloth/static/cloth/arial.ttf'))

    def reshape_text(self, text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def generate_pdf(self):
        # Setup canvas
        c = canvas.Canvas(self.file_name, pagesize=A4)
        width, height = A4
        margin = 5 * mm

        # Title
        title = "\u062C\u062F\u0648\u0644 \u0627\u0644\u0628\u064A\u0627\u0646\u0627\u062A"
        bidi_title = self.reshape_text(title)
        bidi_title = "Honest Fabrics"
        c.setFont("Arabic", 16)
        c.drawCentredString(width / 2, height - (margin + 15 * mm), bidi_title)

        # Table setup
        table_start_y = height - margin - 70
        column_widths = [width / len(self.columns) for _ in self.columns]
        reshaped_headers = [self.reshape_text(header) for header in self.columns]

        # Draw headers
        c.setFont("Arabic", 11)
        x = margin
        y = table_start_y
        for i, header in enumerate(reshaped_headers):
            c.drawString(x, y, header)
            x += column_widths[i]

        # Draw data
        c.setFont("Arabic", 8)
        y -= 15
        for row in self.data:
            x = margin
            for i, cell in enumerate(row):
                bidi_cell = self.reshape_text(str(cell))
                c.drawString(x, y, bidi_cell)
                x += column_widths[i]
            y -= 15
            if y < margin + 50:  # New page if space is insufficient
                c.showPage()
                y = table_start_y
                c.setFont("Arabic", 8)

        # Footer
        bidi_footer = self.reshape_text(f"{self.footer} : تم تحديث هذه البيانات بتاريخ")
        c.setFont("Arabic", 12)
        c.drawCentredString(width / 2, margin / 2, bidi_footer)

        # Save PDF
        c.save()
        return self.file_name

# Example usage
# data = [
#     ['1/1/2025', '519', 'برسولا قطن', 'احمر (36dg)', '21.00', '485.40', 'طيبه'],
#     ['31/12/2024', '520', 'برسولا قطن مفتوح', 'ابيض(36dg)', '4.00', '97.10', 'طيبه'],
# ]
# columns = ["التاريخ", "رقم", "الوصف", "اللون", "الكمية", "السعر", "الجهة"]
# footer = "تم إنشاء هذا الجدول بواسطة برنامج بايثون"

# pdf_generator = PDFTableGenerator(data, columns, footer)
# pdf_generator.generate_pdf()
