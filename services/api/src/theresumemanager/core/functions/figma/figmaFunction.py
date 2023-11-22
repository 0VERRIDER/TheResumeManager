import requests
import os
from src.theresumemanager.core.tools.pdf.PdfTools import merge_pdfs, resize_pdf
from reportlab.lib.pagesizes import A4
from src.theresumemanager.resources.config import designs, env
import re

def is_valid_format(text):
    pattern = r"v\d+:\d+"
    return re.match(pattern, text) is not None

def resumes_by_version(pages):
    resumes = {}

    for page in pages:
        version = page['name'].split(':')[0]
        if version not in resumes:
            resumes[version] = []

        resumes[version].append(page["id"])
        resumes[version].sort(key=lambda x: int(x.split(':')[1]))

    return resumes

# get file from figma
def get_file_from_figma():
  # figma API request data
  figma_api_base = env.FIGMA_BASE_URL
  query_url = "files/"
  figma_file_id = env.FIGMA_PROJECT_ID
  figma_access_token = env.FIGMA_ACCESS_KEY

  # figma API request headers
  user_agent = "Mozilla/5.0"

  # figma API request headers
  headers = {
    "X-Figma-Token": figma_access_token,
    'User-Agent': user_agent,
  }

  # figma API request address
  request_address = figma_api_base + query_url + figma_file_id

  #Figma API response handling
  response = requests.get(request_address, headers = headers)
  response = response.json()

  # get file
  if 'document' in response:
    file = response["document"]
  else:
    raise Exception("Error while fetching file from figma")

  return file

#get the resume page from figma
def get_resume_page_from_figma(page_name = "Resumes"):
  file = get_file_from_figma()
  # get resume page
  if 'children' in file:
    return [data for data in file.get("children") if data["name"] == page_name]
  else:
    raise Exception("Error while fetching file from figma")
  
#get the resume page from figma
def get_resume_ids_from_figma():
  page = get_resume_page_from_figma()
  # get resume ids
  if len(page) > 0:
    page_content = page[0]["children"]
    resume_pages = [{"id": resume["id"], "name": resume["name"]} for resume in page_content if resume["type"]=="FRAME" and is_valid_format(resume["name"])]
    return resumes_by_version(resume_pages)
  else:
    raise Exception("Error while fetching file from figma")


def get_designs_from_figma(figma_config, job_config, export_location, resume_version):

  # figma API request data
  figma_api_base = env.FIGMA_BASE_URL
  query_url = "images/"
  figma_file_id = env.FIGMA_PROJECT_ID
  figma_access_token = env.FIGMA_ACCESS_KEY
  figma_design_ids = ",".join(get_resume_ids_from_figma().get(resume_version))

  print("Figma Designs: ", figma_design_ids, "and resume_version: ", resume_version)
  # figma API request headers
  user_agent = "Mozilla/5.0"

  # figma API request headers
  headers = {
    "X-Figma-Token": figma_access_token,
    'User-Agent': user_agent,
  }

  # figma API request address
  request_address = figma_api_base + query_url + figma_file_id + '?' + "format=" + figma_config["export_format"] + "&ids=" + figma_design_ids

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