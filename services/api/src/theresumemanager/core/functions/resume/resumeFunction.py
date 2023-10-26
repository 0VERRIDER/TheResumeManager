from ..figma.figmaFunction import get_designs_from_figma
from ..cleanup.fileCleanupFunction import cleanupFunction
from ...tools.pdf.PdfTools import compressPdf
from ...tools.qrcode.qrcodeTools import generate_qrcode
from ...tools.json.jsonTools import generate_json_file
from ....data.database.operations.create import create
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import time
from PyPDF2 import PdfReader, PdfWriter

def generate_resume_pdf(figma_config, job_config, export_location = "/content/" ):

  job_folder_url = export_location + str(job_config["uuid"])

  get_designs_from_figma(figma_config, job_config, export_location=export_location)

  # generate a json file
  generate_json_file(job_folder_url + "/details.json", job_config)

  # Create Database Entry
  data = {
    "uuid": job_config["uuid"],
    "job_number": job_config["job_number"],
    "employer_name": job_config["employer_name"],
    "job_title": job_config["job_role"],
    "status": "PENDING",
    "generated_on": time.strftime('%Y-%m-%d %H:%M:%S'),
    "application_link": job_config["application_link"]
  }

  create(data)
  
  # Register The Font
  pdfmetrics.registerFont(
    TTFont('Poppins', "./src/theresumemanager/resources/fonts/Poppins-Medium.ttf")
  )

  # Load Buffer
  buffer = BytesIO()

  # Set width and height
  width = A4[0]
  height = A4[1]

  # create a new Canvas with Reportlab
  p = canvas.Canvas(buffer, pagesize=A4)
  p.setFont("Poppins", 15)
  job_title = job_config["job_role"]

  # hide the background with rect
  p.setFillColorRGB(255, 255, 255, 1)
  # Set the stroke color to white.
  p.setStrokeColorRGB(255, 255, 255)
  p.rect(width - 400, height - 100, 300, 30, fill=1, stroke=1)

  #set the JobTitle text
  p.setFillColor("#788A84")
  p.drawString(width - (300 + len(job_title) * (14/4)), height - 92, job_title)

  # Set the Tracking QRcode

  generate_qrcode(job_config, export_location=export_location)

  p.drawImage(job_folder_url +'/temp/qrcode.png', width - 570, height - 263, width=40, height=40)
  p.showPage()
  p.save()

  #move to the beginning of the StringIO buffer
  buffer.seek(0)
  newPdf = PdfReader(buffer)

  # #######DEBUG NEW PDF created#############
  # pdf1 = buffer.getvalue()
  # open( job_folder_url + '/temp/edited.pdf', 'wb').write(pdf1)
  # #########################################

  # read your existing PDF
  existingPdf = PdfReader(open(job_folder_url + "/temp/Resume_Merged.pdf", 'rb'))
  output = PdfWriter()

  # add the "watermark" (which is the new pdf) on the existing page
  page = existingPdf.pages[0]
  page.merge_page(newPdf.pages[0])
  output.add_page(page)

  # addevery other pages
  for page_num in range(1, len(existingPdf.pages)):
    output.add_page(existingPdf.pages[page_num])

  # finally, write "output" to a real file
  final_file = job_folder_url + '/Resume_Final.pdf'
  outputStream = open(job_folder_url + '/Resume_Final.pdf', 'wb')
  output.write(outputStream)
  outputStream.close()

  #compressPdf
  compressPdf(final_file)

#   preview_name = job_folder_url + '/temp/Resume_Final_thumbnail.png'
#   preview =  previewPdf(final_file, width, height, name = preview_name)

  # cleanup
  cleanupFunction( job_folder_url + "/temp")

#   return preview
  return final_file