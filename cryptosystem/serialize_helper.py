import base64
import json

def serialize(json_data):
    # Serialize the JSON data to a byte sequence
    serialized_bytes = json.dumps(json_data).encode('utf-8')
    # Base64 encode the byte sequence to ensure compatibility
    encoded_bytes = base64.b64encode(serialized_bytes)
    # Convert the encoded bytes to a string and ensure padding
    encoded_string = encoded_bytes.decode('utf-8') + '=' * (4 - len(encoded_bytes) % 4)
    # Convert the padded string back to bytes
    padded_bytes = encoded_string.encode('utf-8')
    # Convert the bytes to an integer
    number = int.from_bytes(padded_bytes, byteorder='big')
    return number

def deserialize(number):
     # Convert the integer to bytes
    padded_bytes = number.to_bytes((number.bit_length() + 7) // 8, byteorder='big')
    # Convert the padded bytes to a string
    encoded_string = padded_bytes.decode('utf-8')
    # Remove any padding characters
    encoded_string = encoded_string.rstrip('=')
    # Base64 decode the encoded string
    serialized_bytes = base64.b64decode(encoded_string)
    # Deserialize the byte sequence to JSON data
    json_data = json.loads(serialized_bytes.decode('utf-8'))
    return json_data
