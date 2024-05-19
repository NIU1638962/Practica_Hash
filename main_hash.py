# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:24:32 2024

@author: Joel Tapia Salvador
"""
import hashlib
from typing import Optional, Tuple


def string_to_binary_string(string: str) -> str:
    binary_string = ""

    for character in string:
        binary_string += bin(ord(character))[2:]

    return binary_string


def bit_padding(binary_string: str) -> str:
    if not isinstance(binary_string, str):
        raise TypeError("binary_string is not a string.")

    binary_string += "1"

    binary_string += "0" * (512 - ((len(binary_string) - 448) % (512)))

    if (len(binary_string) - 448) % (512) != 0:
        raise RuntimeWarning("Bit padding has not been done correctly.")

    return binary_string


def extension(binary_string: str, number: int):
    if not isinstance(binary_string, str):
        raise TypeError("binary_string is not a string.")

    if not isinstance(number, int):
        raise TypeError("number is not a integer.")

    binary_number = bin(number)[2:]

    bit_binary_number = ("0" * (64 - len(binary_number)) + binary_number)[-64:]

    if len(bit_binary_number) != 64:
        raise RuntimeWarning("Extension has not been done correctly.")

    return bit_binary_number


def funtion_F(palabra_X, palabra_Y, palabra_Z):



def uab_md5(message: str, num_bits: int) -> Optional[int]:
    message_binary = string_to_binary_string(message)

    message_padded = bit_padding(message_binary)

    message_extended = extension(message_padded, len(message_binary))

    buffer_A = int("0x67452301")
    buffer_B = int("0xefcdab89")
    buffer_C = int("0x98badcfe")
    buffer_D = int("0x10325476")




def second_preimage(message: str, num_bits: int) -> Optional[Tuple[str, int]]:
    pass


def collision(num_bits: int) -> Optional[Tuple[str, str, int]]:
    pass
