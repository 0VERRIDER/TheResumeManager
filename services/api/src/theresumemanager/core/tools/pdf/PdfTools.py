from PyPDF2 import PdfReader, PdfWriter, PdfMerger

def merge_pdfs(pdf_files, output_file):
  """Merges an array of PDF files into a single PDF file.

  Args:
    pdf_files: An array of the paths to the PDF files to be merged.
    output_file: The path to the merged PDF file.
  """

  # Create a new PdfFileMerger object.
  pdf_merger = PdfMerger()

  # Iterate over the array of PDF files and add each file to the merger object.
  for pdf_file in pdf_files:
    pdf_merger.append(pdf_file)

  # Write the merged PDF file to the output file.
  pdf_merger.write(output_file)


def compressPdf(file_path):
  """Compresses a PDF file.

  Args:
    file_path: The path to the PDF file to compress.

  Returns:
    None. The compressed PDF file will be saved to the same location as the original PDF file.
  """

  reader = PdfReader(file_path)
  writer = PdfWriter()

  for page in reader.pages:
      page.compress_content_streams()  # This is CPU intensive!
      writer.add_page(page)

  with open(file_path, "wb") as f:
      writer.write(f)

