import requests
import os
from src.theresumemanager.core.tools.pdf.PdfTools import merge_pdfs

def get_designs_from_figma(figma_config, job_config, export_location):
  figma_api_base = "https://api.figma.com/v1/images/"
  figma_file_id = figma_config.get("file_id")
  figma_access_token = figma_config.get("personal_access_token")
  figma_design_ids = ",".join(figma_config["design_ids"])

  user_agent = "Mozilla/5.0"

  headers = {
    "X-Figma-Token": figma_access_token,
    'User-Agent': user_agent,
  }

  request_address = figma_api_base + figma_file_id + '?' + "format=" + figma_config["export_format"] + "&ids=" + figma_design_ids

  response = requests.get(request_address, headers = headers)
  response = response.json()
  
  print(response)

  if 'images' in response and response["err"] == None:
    page_urls = response["images"]
  else:
    raise Exception("Error while fetching designs from figma")

  pages = {}

  for key, page in page_urls.items():
    data = requests.get(page, stream=True)
    page_name = "page-" + key
    pages[page_name] = data

  job_folder_url = export_location + str(job_config["uuid"])

  if not os.path.exists(job_folder_url + "/temp"):
    # Create the directory
    os.makedirs(job_folder_url + "/temp")

  exported_pages = []
  for page_name, page_content in pages.items():
    uri_to_pdf = job_folder_url + "/temp/" + page_name + ".pdf"
    with open(uri_to_pdf, 'wb') as fd:
      exported_pages.append(uri_to_pdf)
      for chunk in page_content:
          fd.write(chunk)

  # merge pdf
  merge_pdfs(exported_pages, job_folder_url + "/temp/Resume_Merged.pdf")