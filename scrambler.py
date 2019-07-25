# simple encrypter / decrypter
import os
from random import choice, randint

# global vars
separators = [";", "!", ".", "@", "~", ":", "-", "=", "+", "-", "(", ")", "[", "]", "%", "{", "}", "?", "*", "'", "#"]

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def select_mode():
	while True:
		mode = input("Select mode. Encrypt - 1, Decrypt - 2: ")
		if not mode.isdigit():
			clear()
			print("Invalid value! Please select one of the following: 1 (Encrypt) or 2 (Decrypt)")
		else:
			mode = int(mode)
			if not mode in (1,2):
				clear()
				print("Invalid number! Please select one of the following: 1 (Encrypt) or 2 (Decrypt)")
			else:
				return mode


def get_phrase(mode):
	phrase = ""
	while not phrase:
		phrase = input(f"Enter a phrase which you want to {mode} (at least one char): ")
		if not phrase:
			print("Error! You have to enter at least one char!")
	return phrase


def encrypt():
	global separators

	encrypted_string = ""
	letters_range = list(range(65,91)) + list(range(97, 123))
	shift = randint(1, 100)
	shift_letter = chr(choice(letters_range))
	clear()
	phrase = get_phrase("encrypt")
	clear()
	print(".: Encrypt mode :.")
	print(f"Phrase to encrypt: {phrase}")
	temp_storage = [symbol for symbol in phrase]
	for element in temp_storage:
		encrypted_string += (choice(separators) + hex(ord(element)+shift).lstrip("0x"))
	return encrypted_string + shift_letter + str(shift)


def decrypt():
	global separators

	clear()
	phrase = get_phrase("decrypt")
	clear()
	print(".: Decrypt mode :.")
	print(f"Phrase to decrypt: {phrase}")
	for symbol in separators:
		if symbol in phrase:
			phrase = phrase.split(symbol)
			phrase = '|'.join(phrase)
	phrase = phrase.split("|")
	index = 0
	for char in phrase[-1][::-1]:
		if char.isalpha():
			break
		index += 1

	shift = int(phrase[-1][len(phrase[-1])-index:])
	phrase[-1] = phrase[-1][:len(phrase[-1])-(index+1)] # len[-1] - index and - 1 extra letter (separator)

	decrypted_string = ''.join([chr(int(("0x" + char), 16)-shift) for char in phrase if char != ""])
	return decrypted_string


def main():
	clear()
	mode = select_mode()
	if mode == 1:
		result = encrypt()
	else:
		result = decrypt()
	print(f"Result is:\n\033[1;32;40m{result}\033[0m")


if __name__ == '__main__':
	main()
