import hashlib

def generate_hash_function(algorithm):
  """Generates a hash function for the given algorithm.

  Args:
    algorithm: The name of the hashing algorithm.

  Returns:
    A hash function.
  """

  hash_function = hashlib.new(algorithm)

  def hash_string(string, length = 12):
    """Hashes a string using the given hash function.

    Args:
      string: The string to hash.

    Returns:
      The hashed string.
    """

    hash_function.update(string.encode())
    return hash_function.hexdigest()[:length]

  return hash_string