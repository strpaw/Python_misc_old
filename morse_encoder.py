from winsound import Beep
from time import sleep
from sys import argv


MORSE_SYMBOLS = {
    "A": "._",   "B": "_...", "C": "_._.", "D": "_..", "E": ".",
    "F": ".._.", "G": "__.",  "H": "....", "I": "..",  "J": ".___",
    "K": "_._",  "L": "._..", "M": "__",   "N": "_.",  "O": "___",
    "P": ".__.", "Q": "__._", "R": "._.",  "S": "...", "T": "_",
    "U": ".._",  "V": "..._", "W": ".__", "X": "_.._", "Y": "_.__",
    "Z": "___.."
}


def encode_to_morse(text):
    encoded = ""
    for char in text.upper():
        if char == " ":
            encoded += " "  # Two spaces separates words
        else:
            encoded += MORSE_SYMBOLS[char] + " "
    return encoded


def beep_dot():
    Beep(400, 70)


def beep_dash():
    Beep(400, 210)


def beep_morse_symbol(symbol):
    for signal in symbol:
        if signal == '.':
            beep_dot()
        elif signal == "_":
            beep_dash()
        sleep(0.07)


def play_morse(encoded):
    for word in encoded.split("  "):
        for symbol in word.split():
            beep_morse_symbol(symbol)
            sleep(0.24)
        sleep(0.49)


def print_usage():
    print("""
Translate text to Morse code.
Usage:
    morse_encoder.py <text>
<text>  - text to translate, only latin alphabet and spaces, surrounded by double quotation marks
exampled: morse_encoder.py "PYTHON IS A COOL LANGUAGE" """)


def main(args):
    if len(args) == 1:
        encoded = encode_to_morse(args[0])
        print(encoded)
        play_morse(encoded)
    else:
        print_usage()


if __name__ == "__main__":
    main(argv[1:])
