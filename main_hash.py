# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:24:32 2024

@author: Joel Tapia Salvador
"""
from typing import Optional, Tuple
from copy import deepcopy
from math import sin, floor, log

SHIFT_ARRAY = [
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
]


def string_to_binary_string(string: str) -> str:
    """
    Transforms string into a string of ones and zeros.

    Parameters
    ----------
    string : str
        DESCRIPTION.

    Raises
    ------
    TypeError
        DESCRIPTION.
    RuntimeError
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    """
    if not isinstance(string, str):
        raise TypeError("'binary_string' is not a string.")

    binary_string = ""

    for character in string:
        binary_string += number_to_binary_string(ord(character), base=8)

    if len(binary_string) % 8 != 0:
        raise RuntimeError(
            "Binary conversion from string has not been done correctly."
        )

    return binary_string


def bit_padding(binary_string: str) -> str:
    """


    Parameters
    ----------
    binary_string : str
        DESCRIPTION.

    Raises
    ------
    TypeError
        DESCRIPTION.
    RuntimeWarning
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    """
    if not isinstance(binary_string, str):
        raise TypeError("'binary_string' is not a string.")

    first_padded_binary_string = binary_string + "1"

    second_padded_binary_string = first_padded_binary_string + "0" * (
        448 - (len(first_padded_binary_string) % 512)
    )

    if (len(second_padded_binary_string) - 448) % (512) != 0:
        raise RuntimeWarning("Bit padding has not been done correctly.")

    return second_padded_binary_string


def extension(binary_string: str, number: int) -> str:
    """


    Parameters
    ----------
    binary_string : str
        DESCRIPTION.
    number : int
        DESCRIPTION.

    Raises
    ------
    TypeError
        DESCRIPTION.
    ValueError
        DESCRIPTION.
    RuntimeWarning
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    """
    if not isinstance(binary_string, str):
        raise TypeError("'binary_string' is not a string.")

    if not isinstance(number, int):
        raise TypeError("'number' is not an integer.")

    if number < 0:
        raise ValueError("'number' is not a valid value for length.")

    padded_binary_number = number_to_binary_string(
        number, base=64, endian="little"
    )

    if len(padded_binary_number) != 64:
        raise RuntimeWarning("Length bit has not been padded correctly.")

    extended_binary_string = binary_string + padded_binary_number

    if len(extended_binary_string) % 512 != 0:
        raise RuntimeWarning("Extension has not been done correctly.")

    return extended_binary_string


def functions(
    form: str, word_x: int, word_y: int, word_z: int, base: int = 32
) -> int:
    """


    Parameters
    ----------
    form : str
        DESCRIPTION.
    word_X : int
        DESCRIPTION.
    word_Y : int
        DESCRIPTION.
    word_Z : int
        DESCRIPTION.
    base : int, optional
        DESCRIPTION. The default is 32.

    Raises
    ------
    TypeError
        DESCRIPTION.
    ValueError
        DESCRIPTION.
    RuntimeWarning
        DESCRIPTION.

    Returns
    -------
    int
        DESCRIPTION.

    """
    # pylint: disable=too-many-branches
    if not isinstance(form, str):
        raise TypeError("'form' is not a string.")

    if not isinstance(word_x, int):
        raise TypeError("'word_x' is not an integer.")

    if not isinstance(word_y, int):
        raise TypeError("'word_y' is not an integer.")

    if not isinstance(word_z, int):
        raise TypeError("'word_z' is not an integer.")

    if not isinstance(base, int):
        raise TypeError("'base' is not an integer.")

    if form not in ("F", "G", "H", "I"):
        raise ValueError("'form' is not a valid value.")

    if base < 1:
        raise ValueError("'base' is not a valid value for a base.")

    if word_x.bit_length() > base:
        raise ValueError(
            f"'word_x' is not withing the base, {base}, instead is "
            + f"{word_x.bit_length()}"
        )

    if word_y.bit_length() > base:
        raise ValueError(
            f"'word_y' is not withing the base, {base}, instead is "
            + f"{word_y.bit_length()}"
        )

    if word_z.bit_length() > base:
        raise ValueError(
            f"'word_z' is not withing the base, {base}, instead is "
            + f"{word_z.bit_length()}"
        )

    if form == "F":
        value = (word_x & word_y) | (~word_x & word_z)
    elif form == "G":
        value = (word_x & word_z) | (word_y & ~word_z)
    elif form == "H":
        value = word_x ^ word_y ^ word_z
    elif form == "I":
        value = word_y ^ (word_x | ~word_z)

    if value.bit_length() > base:
        raise RuntimeWarning(
            "Funtion F hasn't been calculated correctly, length should "
            + f"be {base} and is {value.bit_length()}."
        )

    return value


def constant(radiant: int | float, base: int = 32) -> int:
    """


    Parameters
    ----------
    radiant : int | float
        DESCRIPTION.
    base : int, optional
        DESCRIPTION. The default is 32.

    Raises
    ------
    TypeError
        DESCRIPTION.
    ValueError
        DESCRIPTION.
    RuntimeWarning
        DESCRIPTION.

    Returns
    -------
    int
        DESCRIPTION.

    """
    if not isinstance(radiant, (int, float)):
        raise TypeError("'radiant' is not an integer or a float.")

    if not isinstance(base, int):
        raise TypeError("'base' is not an integer.")

    if base < 1:
        raise ValueError("'base' is not a valid value for a base.")

    value = floor((2**base) * abs(sin(radiant + 1)))

    if value.bit_length() > base:
        raise RuntimeWarning(
            "Constant hasn't been calculated correctly, length should "
            + f"be {base} and is {value.bit_length()}."
        )

    return value


def circular_shift(number: int, shift_postions: int, base: int = 32) -> int:
    """


    Parameters
    ----------
    number : int
        DESCRIPTION.
    shift_postions : int
        DESCRIPTION.
    base : int, optional
        DESCRIPTION. The default is 32.

    Raises
    ------
    TypeError
        DESCRIPTION.
    ValueError
        DESCRIPTION.
    RuntimeWarning
        DESCRIPTION.

    Returns
    -------
    int
        DESCRIPTION.

    """
    if not isinstance(number, int):
        raise TypeError("'number' is not an integer.")

    if not isinstance(shift_postions, int):
        raise TypeError("'shift_postions' is not an integer.")

    if not isinstance(base, int):
        raise TypeError("'base' is not an integer.")

    if base < 1:
        raise ValueError("'base' is not a valid value for a base.")

    if shift_postions < 1:
        raise ValueError("Cannot shift less than one position.")

    number &= (2**base) - 1

    circular_shifted_number = (
        number << shift_postions | number >> (base - shift_postions)
    ) & ((2**base) - 1)

    if circular_shifted_number.bit_length() > base:
        raise RuntimeWarning(
            "Circular shift hasn't been done correctly, length should be "
            + f"{base} and is {circular_shifted_number.bit_length()}."
        )

    return circular_shifted_number


def number_to_binary_string(number: int, base=32, endian: str = "big") -> str:
    """


    Parameters
    ----------
    number : int
        DESCRIPTION.
    base : TYPE, optional
        DESCRIPTION. The default is 32.
    endian : str, optional
        DESCRIPTION. The default is "big".

    Raises
    ------
    TypeError
        DESCRIPTION.
    ValueError
        DESCRIPTION.
    OverflowError
        DESCRIPTION.
    RuntimeError
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    """
    if not isinstance(number, int):
        raise TypeError("'number' is not an integer.")

    if not isinstance(endian, str):
        raise TypeError("'endian' is not a string.")

    if not isinstance(base, int):
        raise TypeError("'base' is not an integer.")

    if base < 1:
        raise ValueError("'base' is not a valid value for a base.")

    if endian not in ("big", "little"):
        raise ValueError("'endian' is not a valid value.")

    if number.bit_length() > base:
        raise OverflowError("'number' is bigger than the given 'base'.")

    binary_string = "".join(
        format(byte, "08b")
        for byte in number.to_bytes(base // 8, byteorder=endian)
    )

    if len(binary_string) % 8 != 0:
        raise RuntimeError(
            "Binary conversion from number has not been done correctly."
        )

    return binary_string


def uab_md5(message: str, num_bits: int) -> Optional[int]:
    """


    Parameters
    ----------
    message : str
        DESCRIPTION.
    num_bits : int
        DESCRIPTION.

    Raises
    ------
    TypeError
        DESCRIPTION.
    ValueError
        DESCRIPTION.
    RuntimeWarning
        DESCRIPTION.

    Returns
    -------
    Optional[int]
        DESCRIPTION.

    """
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    try:
        if not isinstance(message, str):
            raise TypeError("'message' is not a string.")

        if not isinstance(num_bits, int):
            raise TypeError("'num_bits' is not an integer.")

        if not 1 <= num_bits <= 128:
            raise ValueError("Num bits isn't insede the scope of md5.")

        # Convert the message to a string of binary numbers
        message_binary = string_to_binary_string(message)

        # Add the 1 at the end plus the enough number of 0 so the lenght is
        # correct
        message_padded = bit_padding(message_binary)

        # Add the 64 less significant bits (little-endian) of the lenght of the
        # message at the end.
        message_extended = extension(message_padded, len(message_binary))

        # Initiate buffers
        buffer_a = 0x67452301
        buffer_b = 0xEFCDAB89
        buffer_c = 0x98BADCFE
        buffer_d = 0x10325476

        # Process every 512-bit sized chunks of the message
        for chunk_number in range(len(message_extended) // 512):
            chunk = deepcopy(
                message_extended[
                    (512 * (chunk_number)) : (512 * (chunk_number + 1))
                ]
            )

            if len(chunk) != 512:
                raise RuntimeWarning(
                    f"Chunk size is not 512 bits, is {len(chunk)}"
                )

            # Initiate the buffers of every iteration
            sub_buffer_a = deepcopy(buffer_a)
            sub_buffer_b = deepcopy(buffer_b)
            sub_buffer_c = deepcopy(buffer_c)
            sub_buffer_d = deepcopy(buffer_d)

            # Main loop
            for iteration_number in range(64):
                if iteration_number < 16:
                    function_value = functions(
                        "F", sub_buffer_b, sub_buffer_c, sub_buffer_d
                    )

                    word_number = deepcopy(iteration_number)

                elif iteration_number < 32:
                    function_value = functions(
                        "G", sub_buffer_b, sub_buffer_c, sub_buffer_d
                    )

                    word_number = (5 * iteration_number + 1) % 16

                elif iteration_number < 48:
                    function_value = functions(
                        "H", sub_buffer_b, sub_buffer_c, sub_buffer_d
                    )

                    word_number = (3 * iteration_number + 5) % 16

                else:
                    function_value = functions(
                        "I", sub_buffer_b, sub_buffer_c, sub_buffer_d
                    )

                    word_number = (7 * iteration_number) % 16

                word = int(
                    number_to_binary_string(
                        int(
                            chunk[32 * (word_number) : 32 * (word_number + 1)],
                            2,
                        ),
                        endian="little",
                    ),
                    2,
                )

                if word.bit_length() > 32:
                    raise RuntimeWarning(
                        f"Word size is not 32 bits, is {word.bit_length()}."
                    )

                f_value = (
                    function_value
                    + sub_buffer_a
                    + constant(iteration_number)
                    + word
                )

                sub_buffer_a = deepcopy(sub_buffer_d)
                sub_buffer_d = deepcopy(sub_buffer_c)
                sub_buffer_c = deepcopy(sub_buffer_b)
                sub_buffer_b = (
                    sub_buffer_b
                    + circular_shift(f_value, SHIFT_ARRAY[iteration_number])
                ) & 0xFFFFFFFF

                # Clean variables to assure clean state in every round.
                del function_value
                del word_number
                del word
                del f_value

            buffer_a = (buffer_a + sub_buffer_a) & 0xFFFFFFFF
            buffer_b = (buffer_b + sub_buffer_b) & 0xFFFFFFFF
            buffer_c = (buffer_c + sub_buffer_c) & 0xFFFFFFFF
            buffer_d = (buffer_d + sub_buffer_d) & 0xFFFFFFFF

            # Clean variables to assure clean state in every digest iteration.
            del chunk
            del sub_buffer_a
            del sub_buffer_b
            del sub_buffer_c
            del sub_buffer_d
            del iteration_number

        numerical_hash_sum = (
            (buffer_d << 96) + (buffer_c << 64) + (buffer_b << 32) + buffer_a
        )

        if numerical_hash_sum.bit_length() > 128:
            raise RuntimeWarning(
                "Hash size is not 128 bits, is "
                + f"{numerical_hash_sum.bit_length()}."
            )

        binary_string_hashed_message = number_to_binary_string(
            numerical_hash_sum, base=128, endian="little"
        )

        return int(binary_string_hashed_message[:num_bits], 2)
    except:  # pylint: disable=bare-except
        return None


def numerical_hash_to_hexadecimal_hash(numerical_hash: int) -> hex:
    """


    Parameters
    ----------
    numerical_hash : int
        DESCRIPTION.

    Raises
    ------
    TypeError
        DESCRIPTION.

    Returns
    -------
    hex
        DESCRIPTION.

    """
    if not isinstance(numerical_hash, int):
        raise TypeError("'numerical_hash' is not an integer.")
    return f"{numerical_hash:032x}"


def second_preimage(message: str, num_bits: int) -> Optional[Tuple[str, int]]:
    """


    Parameters
    ----------
    message : str
        DESCRIPTION.
    num_bits : int
        DESCRIPTION.

    Returns
    -------
    Optional[Tuple[str, int]]
        DESCRIPTION.

    """
    to_match_hash = uab_md5(message, num_bits)
    iterations = 0
    obtained_hash = None
    new_message = ""
    limit = 256**2
    while True:
        auxi = deepcopy(iterations)
        iterations += 1
        new_message = ""
        for num_characters in range(floor(log(iterations, 256)) + 1):
            new_message += chr(auxi % 256)
            auxi = auxi // 256
        obtained_hash = uab_md5(new_message, num_bits)
        if to_match_hash == obtained_hash and message != new_message:
            return new_message, iterations

        if iterations > limit:
            return None


def collision(num_bits: int) -> Optional[Tuple[str, str, int]]:
    pass
