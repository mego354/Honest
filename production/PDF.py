from contextlib import suppress
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
from django.utils.timezone import localtime, now


def format_arabic_text(text):
    """Reshape and reorder Arabic text for proper RTL display."""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)


@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        try:
            # Parse the request data
            request_data = json.loads(request.body)
            row_data_table = request_data.get('row_data_table', {})
            total_data_table = request_data.get('total_data_table', {})
            # Generate the PDF
            pdf_path = generate_production_record(row_data_table, total_data_table)

            # Read the generated PDF file
            with open(pdf_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()

            # Create the response
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="production_record.pdf"'
            return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)


class PDF(FPDF):
    def __init__(self, title="Report", footer="Honest Factory - All Rights Reserved", font_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.footter = footer
        self.font_path = font_path or os.path.join(settings.STATIC_ROOT, "cloth", "arial.ttf")
        self.setup_fonts()
        self.set_auto_page_break(auto=True, margin=15)

    def setup_fonts(self):
        """Register custom fonts for the PDF."""
        if not os.path.exists(self.font_path):
            raise FileNotFoundError(f"Font file not found at: {self.font_path}")

        self.add_font("ArialUnicode", "", self.font_path, uni=True)
        self.add_font("ArialUnicode", "B", self.font_path, uni=True)

    def header(self):
        self.set_font("ArialUnicode", "B", 16)
        self.set_fill_color(50, 50, 50)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, self.title, ln=True, align="C", fill=True)
        self.ln(10)

    def footer_section(self):
        """ Add the footer text at the end of the document. """
        self.set_y(-20)
        self.set_font("ArialUnicode", "B", 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, self.footter, align="C")

    def chapter_title(self, title):
        self.set_font("ArialUnicode", "B", 14)
        self.set_fill_color(200, 200, 200)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, format_arabic_text(title), ln=True, align="R", fill=True)
        self.ln(5)

    def add_table(self, headers, data):
        """Create a table with given headers and data."""
        self.set_font("ArialUnicode", "B", 12)
        self.set_fill_color(230, 230, 230)

        column_widths = {
            "رقم الموديل": 40,
            "القطعة": 35,
            "المقاس": 35,
            "الكمية": 25,
            "المصنع": 30,
            "التاريخ": 30,
        }
        col_widths = [column_widths.get(header, 30) for header in headers]

        # Centering the table
        table_width = sum(col_widths)
        margin_x = (self.w - table_width) / 2
        self.set_x(margin_x)

        # Add headers
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, format_arabic_text(header), border=1, align="C", fill=True)
        self.ln()

        # Add rows
        self.set_font("ArialUnicode", "", 10)

        for row in data:
            self.set_x(margin_x)
            with suppress(ValueError):
                row[-1] = datetime.strptime(row[-1], "%Y/%m/%d %I:%M %p").strftime('%Y/%m/%d')
            
            for i, item in enumerate(row):
                self.cell(col_widths[i], 10, format_arabic_text(str(item)), border=1, align="C")
            self.ln()


def generate_production_record(row_data_table, total_data_table):
    """Generates a production record PDF."""
    output_dir = os.path.join(settings.STATIC_ROOT, "cloth")
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    output_path = os.path.join(output_dir, "output.pdf")
    font_path = os.path.join(output_dir, "arial.ttf")

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found at: {font_path}")

    footer = format_arabic_text(f"تقرير بتاريخ {localtime(now()).strftime('%Y/%m/%d')}")

    pdf = PDF(title="Honest Factory Production Record", footer=footer, font_path=font_path)
    pdf.add_page()

    if total_data_table:
        pdf.chapter_title("ملخص تقرير الإنتاج")

        headers = total_data_table.get('columns', [])
        table_data = total_data_table.get('data', [])

        pdf.add_table(headers, table_data)
        pdf.ln(10)

    if row_data_table:
        pdf.chapter_title("تقرير الإنتاج")

        headers = row_data_table.get('columns', [])
        table_data = row_data_table.get('data', [])

        pdf.add_table(headers, table_data)
        pdf.ln(10)

    pdf.output(output_path)
    return output_path
