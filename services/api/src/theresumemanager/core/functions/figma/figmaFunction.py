import requests
import os
from src.theresumemanager.core.tools.pdf.PdfTools import merge_pdfs, resize_pdf
from reportlab.lib.pagesizes import A4
from src.theresumemanager.resources.config import designs

def get_designs_from_figma(figma_config, job_config, export_location, resume_version):

  # figma API request data
  figma_api_base = "https://api.figma.com/v1/images/"
  figma_file_id = figma_config.get("file_id")
  figma_access_token = figma_config.get("personal_access_token")
  figma_design_ids = ",".join(designs[resume_version]["ids"])
  figma_resume_size = designs[resume_version]["page_size"]

  print("Figma Designs: ", figma_design_ids, "and resume_version: ", resume_version)
  # figma API request headers
  user_agent = "Mozilla/5.0"

  # figma API request headers
  headers = {
    "X-Figma-Token": figma_access_token,
    'User-Agent': user_agent,
  }

  # figma API request address
  request_address = figma_api_base + figma_file_id + '?' + "format=" + figma_config["export_format"] + "&ids=" + figma_design_ids

  #Figma API response handling
  response = requests.get(request_address, headers = headers)
  response = response.json()
  
  # get thumbnails of pages
  if 'images' in response and response["err"] == None:
    page_urls = response["images"]
  else:
    raise Exception("Error while fetching designs from figma")

  # get pages
  pages = {}

  for key, page in page_urls.items():
    data = requests.get(page, stream=True)
    page_name = "page-" + key
    pages[page_name] = data

  # create folder for job
  job_folder_url = export_location + str(job_config["uuid"])

  if not os.path.exists(job_folder_url + "/temp"):
    # Create the directory
    os.makedirs(job_folder_url + "/temp")

  # export pages to pdf
  exported_pages = []
  for page_name, page_content in pages.items():
    uri_to_pdf = job_folder_url + "/temp/" + page_name + ".pdf"
    with open(uri_to_pdf, 'wb') as fd:
      exported_pages.append(uri_to_pdf)
      for chunk in page_content:
          fd.write(chunk)

  # merge pdf
  merge_pdfs(exported_pages, job_folder_url + "/temp/Resume_Merged.pdf")

  # resize pdf
  resize_pdf(job_folder_url + "/temp/Resume_Merged.pdf", job_folder_url + "/temp/Resume_Merged.pdf", A4[0], A4[1])