"""
Temperature conversion among Celsius and Fahrenheit degrees.
"""

import argparse


def celsius_to_fahrenheit(celsius):
    return 32 + 9 / 5 * celsius


def fahrenheit_to_celsius(fahrenheit):
    return 5 / 9 * (fahrenheit - 32)


def print_conversion_table():
    print("Celsius | Fahrenheit")
    for celsius in range(-50, 51):
        fahrenheit = celsius_to_fahrenheit(celsius)
        print("{:>8.1f}|{:>8.1f} ".format(celsius, fahrenheit))


ap = argparse.ArgumentParser()

ap.add_argument("-c", "--to-celsius", type=float, required=False, help="Temperature in Fahrenheit")
ap.add_argument("-f", "--to-fahrenheit", type=float, required=False, help="Temperature in Celsius")
ap.add_argument("-t", "--table-conversion", required=False, action='store_true',
                help="Print conversion table in range <-50, 50> Celsius to Fahrenheit")


if __name__ == "__main__":
    args = ap.parse_args()
    if args.to_celsius:
        print(fahrenheit_to_celsius(args.to_celsius))
    if args.to_fahrenheit:
        print(celsius_to_fahrenheit(args.to_fahrenheit))
    if args.table_conversion:
        print_conversion_table()
