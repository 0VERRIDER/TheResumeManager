from ..figma.figmaFunction import get_designs_from_figma
from ..cleanup.fileCleanupFunction import cleanupFunction
from ...tools.pdf.PdfTools import compressPdf
from ...tools.qrcode.qrcodeTools import generate_qrcode
from ...tools.json.jsonTools import generate_json_file
from ....data.database.DB import DB
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import time
from PyPDF2 import PdfReader, PdfWriter
from src.theresumemanager.resources.config import designs


def set_job_title(
  title, 
  p, 
  width, 
  height, 
  x = 300, 
  y = 92, 
  text_color = "#788A84", 
  font_size= 15, 
  font_name = "Poppins"
  ):

  #fontSize
  p.setFont(font_name, font_size)
  # hide the background with rect
  p.setFillColorRGB(255, 255, 255, 1)
  # Set the stroke color to white.
  p.setStrokeColorRGB(255, 255, 255)

  p.rect(width - (x + 100), height - ( y + 8 ), 300, 30, fill=1, stroke=1)

  #set the JobTitle text
  p.setFillColor(text_color)
  p.drawString(width - (x + len(title) * (14/4)), height - y, title)


def set_qr_code(
  job_folder_url,
  p, 
  width, 
  height, 
  x = 570, 
  y = 263, 
  qr_code_width = 40, 
  qr_code_height = 40
  ):

  p.drawImage(job_folder_url +'/temp/qrcode.png', width - x, height - y, width=qr_code_width, height=qr_code_height)


def generate_resume_pdf(figma_config, job_config, export_location = "/content/", resume_version="v1"):

   # create folder for job
  job_folder_url = export_location + str(job_config["uuid"])

  # Get Designs from Figma and export to pdf
  get_designs_from_figma(figma_config, job_config, export_location=export_location, resume_version=resume_version)

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

  # Create Database Instance
  database = DB()

  # Create Callback
  def callback(result):
    pass

  # Create Database Entry
  database.create(data, callback)

  # Load Buffer
  buffer = BytesIO()

  # Set width and height
  width = A4[0]
  height = A4[1]

  # create a new Canvas with Reportlab
  p = canvas.Canvas(buffer, pagesize=A4)
  
  job_title = job_config["job_role"]

  set_job_title(
    job_title, 
    p, 
    width, 
    height, 
    designs[resume_version]["title_position"][0], 
    designs[resume_version]["title_position"][1]
    )

  # Set the Tracking QRcode

  generate_qrcode(
    job_config, 
    fill_color=designs[resume_version]["qr_fill_color"] or "#FFFFFF",
    back_color=designs[resume_version]["qr_back_color"] or "#000000",
    export_location=export_location)
  set_qr_code(job_folder_url, p, width, height, designs[resume_version]["qr_position"][0], designs[resume_version]["qr_position"][1])

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