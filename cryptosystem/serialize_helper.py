def serialize(message):
    # Encode message into bytes using UTF-8 encoding
    byte_representation = message.encode('utf-8')
    # Convert bytes to an integer using big-endian interpretation
    number_representation = int.from_bytes(byte_representation, 'big')
    return number_representation

def deserialize(number):
    # Convert the integer to bytes
    byte_representation = number.to_bytes((number.bit_length() + 7) // 8, 'big')
    # Decode bytes back to string using UTF-8 encoding
    message = byte_representation.decode('utf-8')
    return message

