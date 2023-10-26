import json

def generate_json_file(file_path, data):
  """Generates a JSON file from the given data.

  Args:
    file_path: The name of the JSON file.
    data: The data to serialize to JSON.
  """

  with open(file_path, "wb") as f:
    json_string = json.dumps(data, indent=4)
    f.write(json_string.encode("utf-8"))