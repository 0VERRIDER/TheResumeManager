import os

def cleanupFunction(tempfile_path):
  #delete temps
  filesToDelte = os.listdir(tempfile_path)

  for file in filesToDelte:
    os.remove(tempfile_path + '/' + file)
  
  os.rmdir(tempfile_path)