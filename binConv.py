

def binary_to_string(b):
    binary_values = b.split()  # On suppose que les valeurs binaires sont séparées par des espaces
    ascii_chars = [chr(int(bv, 2)) for bv in binary_values]
    return ''.join(ascii_chars)

def string_to_binary(s):
    return ' '.join(format(ord(c), '08b') for c in s)