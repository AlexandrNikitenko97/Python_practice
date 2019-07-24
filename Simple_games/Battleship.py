from random import randint
import os
from time import sleep
# min size - 2!
# size 2, max ships - 1, tries - 2
# size 3, max ships - 2, tries - 3
# size 4, max ships - 3, tries - 4
# size 5, max ships - 4, tries - 5
# etc.

# Global vars
cells_destroyed = []
ships_hit = []

# functions
def clear():
	"""Function to clear terminal screen"""
	os.system('cls' if os.name == 'nt' else 'clear')


def generate_field(size):
	"""Function to generate field"""
	return [["O"]*size for i in range(size)]


def show_field(field):
	"""Function to print field"""
	print(" "*4 + ''.join(str([i+1 for i in range(len(field[0]))]).strip('[]').split(',')))
	for j,i in enumerate(field):
		print(str(j+1).ljust(3, " ") + "|" + ' '.join(i) + "|")


def check_existence(array, coord1, coord2):
	"""Function to check if coords exist in array, if no append to array"""
	if not [coord1, coord2] in array:
		array.append([coord1, coord2])
	return array
	

def generate_ships(ships, size):
	"""Function to generate ships randomly not close to each other"""
	size -= 1
	ships_created = 0
	blocked_cells = []
	ships_array = []
	while ships_created < ships:
		row = randint(0, size)
		sleep(0.1)
		col = randint(0, size)
		ship = [row, col]
		if (ship in ships_array) or (ship in blocked_cells):
			if len(blocked_cells) == (size+1)**2:
				ships_array = []
			continue
		else:
			ships_array.append(ship)
			blocked_cells.append(ship)
			# row-1, col-1   +
			# row-1, col     +
			# row-1, col+1   +
			# row+1, col-1   +
			# row+1, col     +
			# row+1, col+1   +
			# row, col-1     +
			# row, col+1     +
			if col-1 >= 0:
				blocked_cells = check_existence(blocked_cells, row, col-1)
			if col+1 <= size:
				blocked_cells = check_existence(blocked_cells, row, col+1)
			if row-1 >= 0:
				blocked_cells = check_existence(blocked_cells, row-1, col)
			if row+1 <= size:
				blocked_cells = check_existence(blocked_cells, row+1, col)
			if row+1 <= size and col+1 <= size:
				blocked_cells = check_existence(blocked_cells, row+1, col+1)
			if row-1 >= 0 and col-1 >= 0:
				blocked_cells = check_existence(blocked_cells, row-1, col-1)
			if row-1 >= 0 and col+1 <= size:
				blocked_cells = check_existence(blocked_cells, row-1, col+1)
			if row+1 <= size and col-1 >= 0:
				blocked_cells = check_existence(blocked_cells, row+1, col-1)
			ships_created += 1
	return ships_array


def ask_axis(size, axis):
	"""Function to check if axis is correct"""
	# axis can be row or col
	while True:
		pin = input(f"Enter {axis} (1-{size}): ")
		if not pin.isdigit():
			print(f"Invalid value! Please choose one digit of the following - 1-{size}!")
		else:
			pin = int(pin)
			if (pin < 1) or (pin > size):
				print(f"Invalid {axis}! Please choose one from the following range - 1-{size}!")
			else:
				break
	return pin - 1


def make_hit(size):
	"""Function ask coords to hit and validate"""
	global cells_destroyed
	global ships_hit
	while True:
		row = ask_axis(size, "row")
		col = ask_axis(size, "column")
		if [row, col] in cells_destroyed or [row, col] in ships_hit:
			print(f"These coordinates already used! Please choose another ones!")
			continue
		return [row, col]


def check_hit(size, field, ships):
	"""Function to check if player hit or not, return hit and field"""
	global cells_destroyed
	global ships_hit

	hit = make_hit(size)
	size -= 1 # decrease size by one (to start from zero) 
	row = hit[0]
	col = hit[1]
	destroyed = 0
	if hit in ships:
		field[row][col] = "X"
		destroyed += 1
		ships_hit.append([row, col])
		# mark cells around as hitted
		if col-1 >= 0:
			field[row][col-1] = "-"
			cells_destroyed = check_existence(cells_destroyed, row, col-1)
		if col+1 <= size:
			field[row][col+1] = "-"
			cells_destroyed = check_existence(cells_destroyed, row, col+1)
		if row-1 >= 0:
			field[row-1][col] = "-"
			cells_destroyed = check_existence(cells_destroyed, row-1, col)
		if row+1 <= size:
			field[row+1][col] = "-"
			cells_destroyed = check_existence(cells_destroyed, row+1, col)
		if row+1 <= size and col+1 <= size:
			field[row+1][col+1] = "-"
			cells_destroyed = check_existence(cells_destroyed, row+1, col+1)
		if row-1 >= 0 and col-1 >= 0:
			field[row-1][col-1] = "-"
			cells_destroyed = check_existence(cells_destroyed, row-1, col-1)
		if row-1 >= 0 and col+1 <= size:
			field[row-1][col+1] = "-"
			cells_destroyed = check_existence(cells_destroyed, row-1, col+1)
		if row+1 <= size and col-1 >= 0:
			field[row+1][col-1] = "-"
			cells_destroyed = check_existence(cells_destroyed, row+1, col-1)
	else:
		# if miss
		field[row][col] = "-"
		cells_destroyed = check_existence(cells_destroyed, row, col)
	return field, destroyed


def ask_size():
	"""Function to ask and check field size"""
	while True:
		size = input("Enter size: ")
		if size.isdigit():
			size = int(size)
			if size < 2:
				print("Invalid size! Min value = 2.")
				continue
			return size
		else:
			print("Invalid value! Please enter the number! (Min value = 2) ")


def play_again():
	"""Function to check if a new play needed"""
	allowed_y = ["y", "yes"]
	allowed_n = ["n", "no"]
	tries = 0
	while tries != 5:
		decision = input("Do you want to play one more game? (Y/N): ").lower()
		if decision in allowed_y:
			# clear console
			clear()
			return True
		elif decision in allowed_n:	
			clear()
			print("Thanks for the game! Bye!")
			return False
		else:
			clear()
			print("Your choice is invalid! Please choose one of the following: Y or N\n")
			print("Invalid input [{}/5]".format(tries+1))
			tries += 1
	if tries == 5:
		clear()
		print("Invalid input [{}/5]".format(tries))
		print("Your have entered invalid choice 5 times in row. Game is over, Bye!")
		return False


def main():
	game = True
	while game:
		global cells_destroyed 
		global ships_hit 
		cells_destroyed = []
		ships_hit = []
		clear()
		print(".: Let's play simple BattleShip game :.\n")
		print("Rules are simply:\n1) You have a field [NxN].")
		print("2) There are N-1 ships located randomly on the field.")
		print("3) You have N(in case of size < 4, else N*1.5) attempts to destroy all the ships (if you destroy a ship, attempts won't change).")
		print("\nNow, please choose field size (min 2x2):")

		size = ask_size()
		ships_qty = size-1
		attempts = 0
		max_attempts = size if size < 4 else int(size*1.5)
		# destroyed = 0
		field = generate_field(size)
		ships = generate_ships(ships_qty, size)
		clear()

		print("Let's start!")
		print(f"Generated field: [{size}x{size}].")
		print(f"Field has {ships_qty} ship(s) hidden.")
		print(f"You have {max_attempts} attempts!")
		print("Good luck!\n")
		first_shot = True
		while attempts < max_attempts:
			if not first_shot:
				if destroyed == 1 :
					ships_qty -= 1
					print("Good shot! One ship destroyed!")
				else:
					print("You miss!")
				if ships_qty == 0:
					break
			print(f"Ships left: {ships_qty}")
			print(f"Attempts: {attempts}/{max_attempts}")
			show_field(field)
			field, destroyed = check_hit(size, field, ships)
			first_shot = False
			if destroyed != 1:
				attempts += 1
			clear()

		if ships_qty == 0:
			show_field(field)
			print(f"\nCongratulations! You win! All {size-1} ship(s) destroyed! Good job!")
		else:
			show_field(field)
			print(f"\nSorry! You lose. Your attempts are over. {ships_qty} ship(s) left! Game is over!")
		game = play_again()



if __name__ == '__main__':
	main()
