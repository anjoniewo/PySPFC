from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os.path

# pdf_export_path = os.path.join(os.path.dirname(__file__), "../../test/test_export")
# pdf_path = os.path.join(pdf_export_path, "test.pdf")
# canvas = canvas.Canvas(pdf_path, pagesize=letter)

canvas = canvas.Canvas("test.pdf", pagesize=letter)

canvas.setLineWidth(.3)
canvas.setFont('Helvetica', 12)

canvas.drawString(30, 750, 'OFFICIAL COMMUNIQUE')
canvas.drawString(30, 735, 'OF ACME INDUSTRIES')
canvas.drawString(500, 750, "12/12/2010")
canvas.line(480, 747, 580, 747)

canvas.drawString(275, 725, 'AMOUNT OWED:')
canvas.drawString(500, 725, "$1,000.00")
canvas.line(378, 723, 580, 723)

canvas.drawString(30, 703, 'RECEIVED BY:')
canvas.line(120, 700, 580, 700)
canvas.drawString(120, 703, "JOHN DOE")

canvas.save()