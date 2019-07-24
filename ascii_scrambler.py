# simple encrypter / decrypter
import os


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


def get_key():
	while True:
		key = input("Enter encrypt key (digit): ")
		try:
			key = int(key)
		except ValueError:
			clear()
			print("Invalid value! Please enter a number!")
		else:
			if key == 0:
				clear()
				print("The key can't be a 0!")
			elif key < -1000000 or key > 1000000:
				clear()
				print("Invalid number! Max value is reached!")
			else:
				return key 


def get_phrase(mode):
	phrase = ""
	while not phrase:
		phrase = input(f"Enter a phrase which you want to {mode} (at least one char): ")
		if not phrase:
			print("Error! You have to enter at least one char!")
	return phrase


def encrypt():
	encrypted_string = ""
	clear()
	phrase = get_phrase("encrypt")
	clear()
	key = get_key()
	clear()
	print(".: Encrypt mode :.")
	print(f"Encrypt phrase: {phrase}")
	print(f"Key: {key}")
	temp_storage = [symbol for symbol in phrase]
	for element in temp_storage:
		encrypted_string += chr(ord(element)+key)
	return encrypted_string 


def decrypt():
	decrypted_string = ""
	clear()
	phrase = get_phrase("decrypt")
	clear()
	key = get_key()
	clear()
	print(".: Decrypt mode :.")
	print(f"Decrypt phrase: {phrase}")
	print(f"Key: {key}")
	temp_storage = [symbol for symbol in phrase]
	for element in temp_storage:
		decrypted_string += chr(ord(element)-key)
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
