import os
from django.core.management.base import BaseCommand
from django.conf import settings

from django.core.mail import EmailMessage

from cloth.models import Fabric, CutTransfer, ReturnTransfer, Statistics

from cloth.utils import get_recent_cloth_operations
from production.utils import get_recent_models

from cloth.reports import generate_production_report

class Command(BaseCommand):
    help = "Generates the daily production report"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Generating the daily production report..."))

        # Fetch recent operations
        models = [Fabric, CutTransfer, ReturnTransfer, Statistics]
        recent_cloth_operations = get_recent_cloth_operations(models,days=5)
        recent_models = get_recent_models(days=5)

        # Define output path
        report_path = os.path.join("reports", "production_report.pdf")
        full_path = os.path.join(settings.MEDIA_ROOT, report_path)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Generate report
        generated = generate_production_report(recent_cloth_operations, recent_models, full_path)
        if generated:            
            self.stdout.write(self.style.SUCCESS(f"Report saved at {full_path}"))
            try:
                send_email_with_attachment()
                self.stdout.write(self.style.SUCCESS(f"Report Sent Successfully"))
            except:
                self.stdout.write(self.style.NOTICE("Error Sending The Report"))
                



def send_email_with_attachment():
    subject = "Daily Production Report"
    body = "Hello Ahmed,\n\nPlease find attached the daily production report.\n\nBest regards,\nMahmoud"
    recipient = ["megomego354@gmail.com", "ahnabil148@gmail.com"]
    recipient = ["megomego354@gmail.com"]

    email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, recipient)

    # Attach the file
    file_path = os.path.join(settings.MEDIA_ROOT, "reports", "production_report.pdf")
    if os.path.exists(file_path):
        email.attach_file(file_path)

    email.send()
    return True


