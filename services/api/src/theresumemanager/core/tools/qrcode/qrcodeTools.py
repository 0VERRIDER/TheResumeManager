import qrcode
import os

def generate_qrcode(
    job_config,
    fill_color,
    back_color,
    export_location = '/content/'
  ):
  qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
  )

  qr.add_data(f'https://resume.anshil.me/view/?uuid={job_config["uuid"]}')
  qr.make(fit=True)

  qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)

  job_folder_url = export_location + str(job_config.get("uuid"))

  if not os.path.exists(job_folder_url +'/temp'):
    # Create the directory
    os.makedirs(job_folder_url + '/temp')

  qr_image.save(job_folder_url +'/temp/qrcode.png')