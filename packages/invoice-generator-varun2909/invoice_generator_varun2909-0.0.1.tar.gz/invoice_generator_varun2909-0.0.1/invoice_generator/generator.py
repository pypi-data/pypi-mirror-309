# invoice_generator/generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import boto3

class InvoiceGenerator:
    def __init__(self, booking_data, s3_bucket=None):
        self.booking_data = booking_data
        self.s3_bucket = s3_bucket
        self.pdf_buffer = BytesIO()

    def create_pdf(self):
        pdf = canvas.Canvas(self.pdf_buffer, pagesize=A4)
        
        # Set font for the header
        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(colors.HexColor("#333333"))

        # Company Name Header
        pdf.drawCentredString(300, 800, "GoFreight")

        # Reset font for the invoice content
        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(colors.black)

        # Draw invoice details below the header
        pdf.drawString(100, 750, "Freight Booking Invoice")
        pdf.drawString(100, 730, f"Booking ID: {self.booking_data['booking_id']}")
        pdf.drawString(100, 710, f"Customer: {self.booking_data['customer_name']}")
        pdf.drawString(100, 690, f"Freight Details: {self.booking_data['freight_details']}")
        pdf.drawString(100, 670, f"Cost: ${self.booking_data['cost']}")
        pdf.drawString(100, 650, f"Estimated Delivery: {self.booking_data['delivery_estimate']}")
        
        pdf.showPage()
        pdf.save()
        self.pdf_buffer.seek(0)

    def save_pdf_to_s3(self):
        if not self.s3_bucket:
            raise ValueError("S3 bucket name is required for S3 storage.")
        s3 = boto3.client('s3')
        file_name = f"invoices/invoice_{self.booking_data['booking_id']}.pdf"
        s3.upload_fileobj(self.pdf_buffer, self.s3_bucket, file_name)
        return f"https://{self.s3_bucket}.s3.amazonaws.com/{file_name}"

    def save_pdf_locally(self, file_path):
        with open(file_path, 'wb') as f:
            f.write(self.pdf_buffer.getvalue())

    def generate_invoice(self, save_to_s3=False, local_path=None):
        self.create_pdf()
        if save_to_s3:
            return self.save_pdf_to_s3()
        elif local_path:
            self.save_pdf_locally(local_path)
        else:
            raise ValueError("Specify either 'save_to_s3=True' or provide 'local_path' to save locally.")
