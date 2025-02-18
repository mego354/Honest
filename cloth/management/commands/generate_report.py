from datetime import datetime
import os
from django.core.management.base import BaseCommand
from django.conf import settings

from django.core.mail import EmailMessage

from cloth.utils import get_recent_cloth_operations
from production.utils import get_producion_models, get_packing_models

from cloth.reports import generate_production_report

class Command(BaseCommand):
    help = "Generates the daily production report"

    def handle(self, *args, **kwargs):
        # if datetime.today().weekday() == 4:
        #     self.stdout.write(self.style.WARNING("Task skipped: Today is Friday."))
        #     return

        self.stdout.write(self.style.NOTICE("Generating the daily production report..."))

        # Fetch recent operations
        days = 1
        recent_cloth_operations = get_recent_cloth_operations(days=days)
        producion_models = get_producion_models(days=days)
        packing_models = get_packing_models(days=days)

        # Define output path
        report_path = os.path.join("reports", "production_report.pdf")
        full_path = os.path.join(settings.MEDIA_ROOT, report_path)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Generate report
        generated = generate_production_report(recent_cloth_operations, producion_models, packing_models, full_path)
        if generated:
            self.stdout.write(self.style.SUCCESS(f"Report saved at {full_path}"))
            try:
                # send_email_with_attachment()
                self.stdout.write(self.style.SUCCESS("Report Sent Successfully"))
            except:
                self.stdout.write(self.style.NOTICE("Error Sending The Report"))




def send_email_with_attachment():
    subject = "Daily Production Report"
    body = "Hello Ahmed,\n\nPlease find attached the daily production report.\n\nBest regards,\nMahmoud"
    recipient = ["megomego354@gmail.com", "ahnabil148@gmail.com"]
    # recipient = ["megomego354@gmail.com"]

    email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, recipient)

    # Attach the file
    file_path = os.path.join(settings.MEDIA_ROOT, "reports", "production_report.pdf")
    if os.path.exists(file_path):
        email.attach_file(file_path)

    email.send()
    return True


