import os
from django.conf import settings
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
from django.utils.timezone import localtime, now

import datetime
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
            column_widths = {
                "رقم الموديل": 20,
                "كود الخامه": 20,
                "اسم الخامه": 40,
                "اللون": 40,
                "عدد الاتواب": 20,
                "الوزن": 20,
                "التاريخ": 25,
                "اسم المصبغة": 30,
                "رقم الموديل": 40,
                "نوع الحركه": 25,
                "مقاسات": 45,
                "الكراتين": 45,
                "عدد القطع": 20,
                "عدد القطع": 20,
                "القطن": 15,
                "الطول": 15,
                "العرض": 15,
                "الارتفاع": 20,
                "المقاس": 20,
                "البوليستر": 20,
                "UPC Number": 30,
            }
            col_widths = [column_widths.get(header, 30) for header in headers]  # Default width = 30
            
            # max_table_width = self.w - 20  # Ensure table fits within the page
            # num_columns = len(headers)
            # max_col_width = max_table_width / num_columns  # Distribute width evenly
        
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


def generate_production_report(cloth_operations, access_models, producion_models, packing_models, output_path):
    footer = format_arabic_text(f"تقرير بتاريخ {localtime(now()).strftime('%Y/%m/%d')}")
    font_path = os.path.join(settings.STATIC_ROOT, "cloth", "arial.ttf")

    pdf = PDF(title="Honest Factory Daily Report", final_footer=footer, font_path=font_path)
    pdf.add_page()

    # ---------------------- تقرير القماش (Cloth Report) ----------------------

    pdf.add_section("تقرير القماش", [])
    has_data = False
    
    operation_headers = {
        "وارد": ["كود الخامه", "اسم الخامه", "عدد الاتواب", "الوزن", "التاريخ"],
        "قص": ["كود الخامه", "اسم الخامه", "عدد الاتواب", "الوزن", "التاريخ"],
        "مرتجع": ["كود الخامه", "اسم الخامه", "عدد الاتواب", "الوزن", "التاريخ"],
    }

    operation_headers_details = {
        "وارد": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "اسم المصبغة"],
        "قص": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "رقم الموديل"],
        "مرتجع": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "رقم الموديل"],
        "احصائيات": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "اسم المصبغة", "رقم الموديل", "نوع الحركه"]
    }
    
    for op_type, headers in operation_headers.items():
        operations = cloth_operations.get(op_type, [])
        if operations:
            has_data = True

            if pdf.get_y() > 230:
                pdf.add_page()

            pdf.chapter_body([op_type])
            
            table_data = []
            detail_headers = operation_headers_details[op_type]
            
            for op in operations:
                if len(op['operations']) > 1:
                    summary_row = [
                        op.get("fabric_code", "------"),
                        op.get("fabric_name", "------"),
                        "------",
                        op.get("roll", 0),
                        op.get("weight", 0),
                        "------",
                        f" تجميع {op_type}"
                    ]
                    table_data.append(summary_row)
                
                    for op_detail in op['operations']:
                        op_detail["كود الخامه"] = op_detail.get("كود الخامه", "------")
                        # op_detail["اسم الخامه"] = op_detail.get("اسم الخامه", "------")
                        table_data.append(list(op_detail.values()))
                else:
                    table_data.append(list(op['operations'][0].values()))
            
            pdf.add_table(detail_headers, table_data)
            pdf.ln(10)
    
    if not has_data:
        pdf.chapter_body(["لا يوجد بيانات متاحة لهذا التقرير."])

    # ---------------------- تقرير الملحقات (Accessories Report) ----------------------
    def date_care_getattr(instant, op_field):
        value = getattr(instant, op_field, None)
        if op_field == 'date' and isinstance(value, datetime.date) :
            return value.strftime("%Y/%m/%d")
        else:
            return value
        
    verbose_field_map = {'المصنع': 'factory', 'supply': 'وارد', 'package': 'تحويل', 'return': 'مرتجع', 'القطن': 'cotton_percentage', 'البوليستر': 'polyester_percentage', 'عدد الكرتون': 'carton_count', 'الطول': 'length', 'العرض': 'width', 'الارتفاع': 'height', 'طول الكيس': 'bag_length', 'العرض الكيس': 'bag_width', 'الاكياس في الكيلو': 'bags_per_kilo'}
    
    pdf.add_section("تقرير الملحقات", [])

    if access_models != None:
        types = ['supply', 'package', 'return']
        for model_data in access_models:
            model_data_used = False
            if pdf.get_y() + 0 > 270:
                pdf.add_page()

            for field in model_data["models"][0]._meta.fields:
                verbose_field_map[field.verbose_name] = field.name

            for type in types:
                if model_data[type]['columns']:
                    pdf.chapter_body([f"{verbose_field_map[type]}: {model_data['model']}"])

                    operations = model_data[type]['operations']
                    headers = model_data[type]['columns']
                    table_data = []

                    if len(operations) == 1:
                        table_data += [[date_care_getattr(operations[0], verbose_field_map[op_field]) for op_field in headers]]
                    else:
                        collection = ['---'] * len(headers)

                        for key in operations[0].keys():
                            arabic_key = next((arabic for arabic, value in verbose_field_map.items() if value == key), None)

                            if arabic_key is not None and arabic_key in headers:
                                index = headers.index(arabic_key)  # Find the correct index
                                collection[index] = operations[0][key]  # Place the value at the right index

                        if headers:
                            collection[0] = 'تجميع'

                        table_data.append(collection)

                        table_data += [
                            [date_care_getattr(operation, verbose_field_map[op_field]) for op_field in headers]
                            for operation in operations[1:]
                        ]
                        
                    pdf.add_table(headers, table_data)
                    pdf.ln(5)
                    model_data_used = True

            
            if model_data_used:
                pdf.ln(10)
    else:
        pdf.chapter_body(["لا يوجد بيانات متاحة لهذا التقرير."])


    # pdf.ln(20)
    # ---------------------- تقرير الإنتاج (Production Report) ----------------------
    pdf.add_section("تقرير الانتاج", [])
    
    if producion_models:
        for model_data in producion_models:
            if pdf.get_y() + 0 > 270:
                pdf.add_page()

            pdf.chapter_body([f"الموديل: {model_data['model']}"])
            
            headers = ["القطعة", "الكمية", "المقاس", "المصنع", "التاريخ"]
            table_data = [
                [p['type'], p['used_amount'], p['size'], p['factory'], p['created_at']]
                for p in model_data["productions"]
            ]
            
            pdf.add_table(headers, table_data)
            pdf.ln(5)

            if "totals" in model_data and model_data["totals"]:
                pdf.chapter_body(["إجمالي الكمية لكل قطعة:"])
                total_headers = ["القطعة", "إجمالي الكمية"]
                total_data = [[t['type'], t['total_used_amount']] for t in model_data["totals"]]
                pdf.add_table(total_headers, total_data)
            
            pdf.ln(10)
    else:
        pdf.chapter_body(["لا يوجد بيانات متاحة لهذا التقرير."])


    # pdf.ln(20)
    # ---------------------- تقرير التعبئة (Packing Report) ----------------------
    pdf.add_section("تقرير التعبئة", [])

    if packing_models:
        for model_data in packing_models:
            if pdf.get_y() > 270:
                pdf.add_page()

            pdf.chapter_body([f"الموديل: {model_data['model']}"])

            headers = ["كراتين", "مقاسات", "الكرتونة", "الموديل", "التاريخ"]
            table_data = [
                [p['used_carton'], p['sizes'], p['carton'], p['model'], p['created_at']]
                for p in model_data["packings"]
            ]

            pdf.add_table(headers, table_data)
            pdf.ln(5)

            # Display total used cartons per model
            pdf.chapter_body(["إجمالي الكمية المستخدمة من الكراتين:"])
            total_headers = ["الموديل", "إجمالي الكراتين"]
            total_data = [[model_data['model'], model_data["totals"]]]

            pdf.add_table(total_headers, total_data)
            pdf.ln(10)
    else:
        pdf.chapter_body(["لا يوجد بيانات متاحة لهذا التقرير."])

    pdf.output(output_path)
    return True