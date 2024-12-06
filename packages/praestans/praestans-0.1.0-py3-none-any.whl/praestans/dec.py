from praestans.err import error_handling

# Decimal -> (binary, octal, hexadecimal)


@error_handling
def decimal_to_binray(number):
    binary_str = ""
    number = int(number)
    while (number > 0):
        left = number % 2
        number = number // 2
        binary_str += str(left)
    return (binary_str[::-1])


@error_handling
def decimal_to_octal(number):
    octal_str = ""
    number = int(number)
    while (number > 0):
        left = number % 8
        number = number // 8
        octal_str += str(left)
    return (int(octal_str[::-1]))


@error_handling
def decimal_to_hexa(number, size):
    hex_str = ""
    hexadecimal = 16
    hex_chrs = "0123456789abcdef"
    hex_chrs = hex_chrs.upper() if size == "X" else hex_chrs
    number = int(number)
    while (number > 0):
        left = number % hexadecimal
        number = number // hexadecimal
        hex_str += hex_chrs[left]
    return (hex_str[::-1])
