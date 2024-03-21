import zlib

def serialize(message):
    # Encode message into bytes using UTF-8 encoding
    byte_representation = message.encode('utf-8')
    # Compress the byte representation
    compressed_representation = zlib.compress(byte_representation)
    # Convert compressed bytes to an integer using big-endian interpretation
    number_representation = int.from_bytes(compressed_representation, 'big')
    return number_representation

def deserialize(number):
    # Convert the integer to compressed bytes
    compressed_representation = number.to_bytes((number.bit_length() + 7) // 8, 'big')
    # Decompress bytes
    decompressed_representation = zlib.decompress(compressed_representation)
    # Decode bytes back to string using UTF-8 encoding
    message = decompressed_representation.decode('utf-8')
    return message
