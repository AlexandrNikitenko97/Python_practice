from random import randint
import os
from time import sleep
# min size - 2!
# size 2, max ships - 1, tries - 2
# size 3, max ships - 2, tries - 3
# size 4, max ships - 3, tries - 4
# size 5, max ships - 4, tries - 5
# etc.

# global vars
cells_destroyed = []
ships_hit =[]

# functions
def clear():
	"""Function to clear terminal screen"""
	os.system('cls' if os.name == 'nt' else 'clear')


def generate_field(size):
	return [["O"]*size for i in range(size)]


def show_field(field):
	print(" "*4 + ''.join(str([i+1 for i in range(len(field[0]))]).strip('[]').split(',')))
	for j,i in enumerate(field):
		print(str(j+1).ljust(3, " ") + "|" + ' '.join(i) + "|")


def check_existence(array, coord1, coord2):
	if not [coord1, coord2] in array:
		array.append([coord1, coord2])
	return array
	

def generate_ships(ships, size):
	size -= 1
	ships_created = 0
	blocked_cells = []
	ships_array = []
	while ships_created < ships:
		row = randint(0, size)
		sleep(0.2)
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


def main():
	clear()
	print(".: Let's play simple BattleShip game :.\n")
	print("Rules are simply:\n1) You have a field [NxN].")
	print("2) There are N-1 ships located randomly on the field.")
	print("3) You have N attempts to destroy all ships (if you destroy a ship, attempts won't change).")
	print("\nNow, please choose field size (min 2x2):")

	size = ask_size()
	ships_qty = size-1
	attempts = 0
	# destroyed = 0
	field = generate_field(size)
	ships = generate_ships(ships_qty, size)
	clear()

	print("Let's start!")
	print(f"Generated field: [{size}x{size}].")
	print(f"Field has {ships_qty} ship(s) hidden.")
	print(f"You have {size} attempts!")
	print("Good luck!\n")
	while attempts < size:
		print(f"Ships left: {ships_qty}")
		print(f"Attempts: {attempts}/{size}")
		show_field(field)
		field, destroyed = check_hit(size, field, ships)
		if destroyed == 1:
			ships_qty -= 1
		else:
			attempts += 1
		clear()
		if ships_qty == 0:
			break

	if ships_qty == 0:
		show_field(field)
		print(f"\nCongratulations! You win! All {size-1} ship(s) destroyed! Good job!")
	else:
		show_field(field)
		print(f"\nSorry! You lose. Your attempts are over. {ships_qty} ship(s) left! Game is over!")


if __name__ == '__main__':
	main()
