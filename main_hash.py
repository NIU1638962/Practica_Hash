# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:24:32 2024

@author: Joel Tapia Salvador
"""
from typing import Optional, Tuple
from copy import deepcopy
from math import sin, floor
from itertools import product
from time import perf_counter
import matplotlib.pyplot as plt
from pandas import DataFrame

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
        String that is getting binarized.

    Raises
    ------
    TypeError
        Paremeters given are not the proper Type.
    RuntimeError
        If during the execution, the function (internally) get's a variable
        with values not expected, normally due to calculations going wrong and
        it cannot continue calculating because the result would be incorrect.

        If this error is recieved, it means a internal bug or unacounted
        behaviour occured, contact developer via bug report.

    Returns
    -------
    str
        Binary string, string full of only ones and zeros.

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
    Pads the messages adding at the end a one and then enough zeros so the
    message length is congruent to 448 module 512.

    Parameters
    ----------
    binary_string : str
        Binary string to pad, string containing only ones and zeros.

    Raises
    ------
    TypeError
        Paremeters given are not the proper Type.
    RuntimeError
        If during the execution, the function (internally) get's a variable
        with values not expected, normally due to calculations going wrong and
        it cannot continue calculating because the result would be incorrect.

        If this error is recieved, it means a internal bug or unacounted
        behaviour occured, contact developer via bug report.

    Returns
    -------
    str
        Padded binary string, string full of only ones and zeros.

    """
    if not isinstance(binary_string, str):
        raise TypeError("'binary_string' is not a string.")

    first_padded_binary_string = binary_string + "1"

    second_padded_binary_string = first_padded_binary_string + "0" * (
        448 - (len(first_padded_binary_string) % 512)
    )

    if (len(second_padded_binary_string)) % (512) != 448:
        raise RuntimeError("Bit padding has not been done correctly.")

    return second_padded_binary_string


def extension(binary_string: str, number: int) -> str:
    """
    Adds the 64 bits to the message that represent the least significant bits
    in little-endian of the number given.

    Parameters
    ----------
    binary_string : str
        Binarry string, string with ones and zeros, to add the 64 bits.
    number : int
        Number to add as a 64 bit little-endian.

    Raises
    ------
    TypeError
        Paremeters given are not the proper Type.
    ValueError
        Values passed onto the paramenters are not inside the exepcted values.
    RuntimeError
        If during the execution, the function (internally) get's a variable
        with values not expected, normally due to calculations going wrong and
        it cannot continue calculating because the result would be incorrect.

        If this error is recieved, it means a internal bug or unacounted
        behaviour occured, contact developer via bug report.

    Returns
    -------
    str
        Binary string, string with ones and zeros, with the 64-bit little
        endian representation added to the end.

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
        raise RuntimeError("Length bit has not been padded correctly.")

    extended_binary_string = binary_string + padded_binary_number

    if len(extended_binary_string) % 512 != 0:
        raise RuntimeError("Extension has not been done correctly.")

    return extended_binary_string


def functions(
    form: str, word_x: int, word_y: int, word_z: int, base: int = 32
) -> int:
    """
    Applies a function of the form chosen to the words given.

    Parameters
    ----------
    form : str
        Form of the funtion applied.
        - F: (X and Y) or (not X & Z)
        - G: (X and Z) or (Y & not Z)
        - H: X xor Y xor Z
        - I: Y xor (X or not Z)
    word_X : int
        Integer number, representation in binary must have equal or less bits
        length than the used base.
    word_Y : int
        Integer number, representation in binary must have equal or less bits
        length than the used base.
    word_Z : int
        Integer number, representation in binary must have equal or less bits
        length than the used base.
    base : int, optional
        Base, indicates the maximum length in bit the numbers can have,
        including the number resulting of applying the function. The default is
        32.

    Raises
    ------
    TypeError
        Paremeters given are not the proper Type.
    ValueError
        Values passed onto the paramenters are not inside the exepcted values.
    RuntimeError
        If during the execution, the function (internally) get's a variable
        with values not expected, normally due to calculations going wrong and
        it cannot continue calculating because the result would be incorrect.

        If this error is recieved, it means a internal bug or unacounted
        behaviour occured, contact developer via bug report.

    Returns
    -------
    int
        Integer number, representation in binary will have equal or less bits
        length than the given base.

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
        raise RuntimeError(
            "Funtion F hasn't been calculated correctly, length should "
            + f"be {base} and is {value.bit_length()}."
        )

    return value


def constant(radiant: int | float, base: int = 32) -> int:
    """
    Calculates the value of the constant used in a given iteration.

    Parameters
    ----------
    radiant : int | float
        Radiants to calculate the constant, since it comes from a sinusoidal.
    base : int, optional
        Base, indicates the maximum length in bit the numbers can have,
        including the number resulting of applying the function. The default is
        32.

    Raises
    ------
    TypeError
        Paremeters given are not the proper Type.
    ValueError
        Values passed onto the paramenters are not inside the exepcted values.
    RuntimeError
        If during the execution, the function (internally) get's a variable
        with values not expected, normally due to calculations going wrong and
        it cannot continue calculating because the result would be incorrect.

        If this error is recieved, it means a internal bug or unacounted
        behaviour occured, contact developer via bug report.

    Returns
    -------
    int
        Integer number, representation in binary will have equal or less bits
        length than the given base.


    """
    if not isinstance(radiant, (int, float)):
        raise TypeError("'radiant' is not an integer or a float.")

    if not isinstance(base, int):
        raise TypeError("'base' is not an integer.")

    if base < 1:
        raise ValueError("'base' is not a valid value for a base.")

    value = floor((2**base) * abs(sin(radiant + 1)))

    if value.bit_length() > base:
        raise RuntimeError(
            "Constant hasn't been calculated correctly, length should "
            + f"be {base} and is {value.bit_length()}."
        )

    return value


def circular_shift(number: int, shift_positions: int, base: int = 32) -> int:
    """
    Left-shifts (by the given amount) the bits of the given number and replaces
    the zeros to the right with the overflown numbers on the left.

    Parameters
    ----------
    number : int
        Number to shift. Integer number, if representation in binary bigger
        than the used base, only the first bits until reached the base amount
        will be used.
    shift_positions : int
        Number of positions to shift the number. Cannot be less than one nor
        equal or bigger than the given base.
    base : int, optional
        Base, indicates the length in bits the numbers has for the circular
        shift overflow. The default is 32.

    Raises
    ------
    TypeError
        Paremeters given are not the proper Type.
    ValueError
        Values passed onto the paramenters are not inside the exepcted values.
    RuntimeError
        If during the execution, the function (internally) get's a variable
        with values not expected, normally due to calculations going wrong and
        it cannot continue calculating because the result would be incorrect.

        If this error is recieved, it means a internal bug or unacounted
        behaviour occured, contact developer via bug report.

    Returns
    -------
    int
        Circular shifted number. Integer number, representation in binary will
        have equal or less bits length than the given base.

    """
    if not isinstance(number, int):
        raise TypeError("'number' is not an integer.")

    if not isinstance(shift_positions, int):
        raise TypeError("'shift_postions' is not an integer.")

    if not isinstance(base, int):
        raise TypeError("'base' is not an integer.")

    if base < 1:
        raise ValueError("'base' is not a valid value for a base.")

    if shift_positions < 1:
        raise ValueError("Cannot shift less than one position.")

    if shift_positions >= base:
        raise ValueError("Cannot shift equal or bigger than base.")

    number &= (2**base) - 1

    circular_shifted_number = (
        number << shift_positions | number >> (base - shift_positions)
    ) & ((2**base) - 1)

    if circular_shifted_number.bit_length() > base:
        raise RuntimeError(
            "Circular shift hasn't been done correctly, length should be "
            + f"{base} and is {circular_shifted_number.bit_length()}."
        )

    return circular_shifted_number


def number_to_binary_string(number: int, base=32, endian: str = "big") -> str:
    """
    Converts a number into a binary string. Can choose into what endian
    representation is done.

    Parameters
    ----------
    number : int
        Integer numeber to transform. Bit length must be less than base.
    base : TYPE, optional
        Base, indicates the maximum length in bit the numbers can have,
        including the number resulting of applying the function. The default is
        32.
    endian : str, optional
        ENdian of the number to pass to binary string. Can be little-endian or
        bif-endian. The default is "big".

    Raises
    ------
    TypeError
        Paremeters given are not the proper Type.
    ValueError
        Values passed onto the paramenters are not inside the exepcted values.
    RuntimeError
        If during the execution, the function (internally) get's a variable
        with values not expected, normally due to calculations going wrong and
        it cannot continue calculating because the result would be incorrect.

        If this error is recieved, it means a internal bug or unacounted
        behaviour occured, contact developer via bug report.

    Returns
    -------
    str
        Binary string, string full of only ones and zeros.

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
        raise ValueError("'base' is smaller than the given 'number'.")

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
    Calculates the hash of a given messages and returns the num_bits-frist bits
    of it.

    Parameters
    ----------
    message : str
        Message to apply the hash function to. It will be a string of
        characters of arbitrary size.
        length.
    num_bits : int
        Number of output bits that will be a value between 1 and 128.

    Raises
    ------
    TypeError
        Paremeters given are not the proper Type.
    ValueError
       Values passed onto the paramenters are not inside the exepcted values.
    RuntimeWarning
        If during the execution, the function (internally) get's a variable
        with values not expected, normally due to calculations going wrong and
        it cannot continue calculating because the result would be incorrect.

        If this error is recived, it means a internal bug or unacounted
        behaviour occured, contact developer via bug report.

    Returns
    -------
    Optional[int]
        Return the hash of the message as a decimal integer or None if an error
        occured.

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
                raise RuntimeError(
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
                    raise RuntimeError(
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
            raise RuntimeError(
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
    Given a message, calculates a new message with the same hash. Does this
    using brute forcing.

    Parameters
    ----------
    message : str
        Original message, which we want to find a collission in the hash.
    num_bits : int
        Number bits of the hash that we will try to collision with.

    Returns
    -------
    Optional[Tuple[str, int]]
        Tuple including the message we found that has the same hash and the
        number of iterations needed. If message not found or error occurred
        returns None.

    """
    to_match_hash = uab_md5(message, num_bits)
    iterations = 0
    obtained_hash = None
    limit = 10
    for i in range(1, limit + 1):
        new_messages = (
            "".join(x)
            for x in product("".join(chr(i) for i in range(256)), repeat=i)
        )

        for new_message in new_messages:
            iterations += 1
            obtained_hash = uab_md5(new_message, num_bits)
            if to_match_hash == obtained_hash and message != new_message:
                return new_message, iterations

    return None


def collision(num_bits: int) -> Optional[Tuple[str, str, int]]:
    """
    Given a number of bits of the hash to collision, searches two distinct
    messages with same hash. Does so using brute force.

    Parameters
    ----------
    num_bits : int
        Number bits of the hash that we will try to collision with.

    Returns
    -------
    Optional[Tuple[str, str, int]]
        Tuple including the messages we found that have the same hash and the
        number of iterations needed. If messages not found or error occurred
        returns None.

    """
    hash_dict = {}
    messages = []
    for i in range(10):
        messages = (
            "".join(x)
            for x in product("".join(chr(i) for i in range(256)), repeat=i)
        )

    iterations = 1

    for message in messages:
        hash_val = uab_md5(message, num_bits)

        if hash_val in hash_dict:
            return (hash_dict[hash_val], message, iterations)

        hash_dict[hash_val] = message
        iterations += 1
    return None


def graph_times(n_bits: int) -> DataFrame:
    """
    Graphs the time of the collison algorithms.

    Parameters
    ----------
    n_bits : int
        Number indicating the maximum number of bits to plot.

    Returns
    -------
    DataFrame
        Pandas dataframe with the iterations and times information gotten.

    """
    time_second_pre_image = []
    time_collision = []

    iterations_second_pre_image = []
    iterations_collision = []

    for i in range(1, n_bits + 1):
        start = perf_counter()
        _, iterations = second_preimage("This is a benchmark", i)
        end = perf_counter()
        time_second_pre_image.append(end - start)
        iterations_second_pre_image.append(iterations)

        start = perf_counter()
        _, _, iterations = collision(i)
        end = perf_counter()
        time_collision.append(end - start)
        iterations_collision.append(iterations)

    plt.figure(figsize=(10, 5))
    plt.plot(
        range(1, n_bits + 1),
        time_second_pre_image,
        label="Second Pre Image",
    )
    plt.xlabel("Num Bits")
    plt.ylabel("Time of executions (seconds)")
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(
        range(1, n_bits + 1),
        iterations_second_pre_image,
        label="Second Pre Image",
    )
    plt.xlabel("Num Bits")
    plt.ylabel("Number iterations")
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, n_bits + 1), time_collision, label="Collisions")
    plt.xlabel("Num Bits")
    plt.ylabel("Time of executions (seconds)")
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, n_bits + 1), iterations_collision, label="Collisions")
    plt.xlabel("Num Bits")
    plt.ylabel("Number iterations")
    plt.legend()
    plt.show()

    table = DataFrame(
        {
            "Num Bits": range(1, n_bits + 1),
            "Time Second Pre Image": time_second_pre_image,
            "Iterations Second Pre Image": iterations_second_pre_image,
            "Time Collisions": time_collision,
            "Iterations Collisons": iterations_collision,
        }
    )

    print(table)

    return table
