import os
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
from django.utils.timezone import localtime, now

def format_arabic_text(text):
    """
    Reshape and reorder Arabic text for proper RTL display.
    """
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class PDF(FPDF):
    def __init__(self, title="Report", final_footer="Honest Factory - All Rights Reserved", font_path="arial.ttf", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.final_footer = final_footer
        self.font_path = font_path
        self.setup_fonts()
        self.set_auto_page_break(auto=True, margin=15)

    def setup_fonts(self):
        """
        Register custom fonts for the PDF.
        """
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

    def add_final_footer(self):
        """ Add the footer text at the end of the document. """
        self.ln(20)
        self.set_font("ArialUnicode", "B", 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, self.final_footer, align="C")


    def chapter_title(self, title):
        self.set_font("ArialUnicode", "B", 14)
        self.set_fill_color(200, 200, 200)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, format_arabic_text(title), ln=True, align="R", fill=True)
        self.ln(5)

    def chapter_body(self, data):
        self.set_font("ArialUnicode", "", 12)
        for line in data:
            self.cell(0, 7, format_arabic_text(line), ln=True, align="C")
        self.ln(5)

    def add_table(self, headers, data, col_widths=None):
        self.set_font("ArialUnicode", "B", 12)
        self.set_fill_color(230, 230, 230)
        
        # Auto-size columns to fit within the page width
        if col_widths is None:
            max_table_width = self.w - 20  # Ensure table fits within the page
            num_columns = len(headers)
            max_col_width = max_table_width / num_columns  # Distribute width evenly
            col_widths = [max_col_width] * num_columns  # Apply fixed column widths
        
        table_width = sum(col_widths)
        margin_x = (self.w - table_width) / 2
        self.set_x(margin_x)
        
        # Add headers
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, format_arabic_text(header), border=1, align="C", fill=True)
        self.ln()
        
        # Add rows
        self.set_font("ArialUnicode", "", 10)
        def truncate_text(text, max_width, font_size):
            self.set_font("ArialUnicode", "", font_size)
            hidden = False
            while self.get_string_width(text) > max_width:
                text = text[1:]  # Remove last character until it fits
                hidden = True
            return text if not hidden else "…" + text[3:]

        for row in data:
            self.set_x(margin_x)
            for i, item in enumerate(row):
                truncated_item = truncate_text(format_arabic_text(str(item)), col_widths[i], 10)
                self.cell(col_widths[i], 10, truncated_item, border=1, align="C")
            self.ln()        

    def add_section(self, title, content):
        self.chapter_title(title)
        self.chapter_body(content)


def generate_production_report(recent_cloth_operations, recent_models, output_path):
    footer = format_arabic_text(f"تقرير بتاريخ {localtime(now()).strftime('%Y/%m/%d')}")

    pdf = PDF(title="Honest Factory Daily Report", final_footer=footer, font_path="cloth/static/cloth/arial.ttf")
    pdf.add_page()

    pdf.add_section("تقرير الانتاج", [])

    if len(recent_models) > 0:  # Ensures that there is data before processing
        for model_data in recent_models:
            pdf.chapter_body([f"الموديل: {model_data['model']}"])
            headers = ["القطعة", "الكمية", "المقاس", "المصنع", "التاريخ"]
            table_data = [[p['type'], p['used_amount'], p['size'], p['factory'], p['created_at']] for p in model_data["productions"]]
            pdf.add_table(headers, table_data)
            pdf.ln(10)
    else:
        pdf.chapter_body(["لا يوجد بيانات متاحة لهذا التقرير."])  # Display a message if no data exists

    pdf.add_section("تقرير القماش", [])

    operation_headers = {
        "وارد": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "اسم المصبغة"],
        "قص": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "رقم الموديل"],
        "مرتجع": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "رقم الموديل"],
        "احصائيات": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "اسم المصبغة", "رقم الموديل", "نوع الحركه"]
    }

    operation_key = {
        "كود الخامه": "fabric_code",
        "اسم الخامه": "fabric_name",
        "اللون": "color",
        "عدد الاتواب": "roll",
        "الوزن": "weight",
        "التاريخ": "date",
        "اسم المصبغة": "dyehouse_name",
        "رقم الموديل": "model_number",
        "نوع الحركه": "movement_type",
    }

    # Track whether we added any data
    has_data = False

    for op_type, headers in operation_headers.items():
        if recent_cloth_operations.get(op_type):
            has_data = True
            pdf.chapter_body([op_type])
            
            # Extract table data safely
            table_data = [
                [f"{getattr(op, operation_key.get(field))}" for field in headers]
                for op in recent_cloth_operations[op_type]
            ]
            
            pdf.add_table(headers, table_data)
            pdf.ln(10)

    # If no data was added, show a fallback message
    if not has_data:
        pdf.chapter_body(["لا يوجد بيانات متاحة لهذا التقرير."])
    
    pdf.add_final_footer()
    pdf.output(output_path)

    return True