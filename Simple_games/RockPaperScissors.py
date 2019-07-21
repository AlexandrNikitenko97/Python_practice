# Rock, Paper, Scissors game
#
# Rock vs Paper = Paper
# Rock vs Scissors = Rock
# Paper vs Scissors = Scissors
# Paper vs Rock = Paper
# Scissors vs Rock = Rock
# Scissors vs Paper = Scissors
# If equals = Tie

from random import choice
import os

# global vars
choices = ["Rock", "Paper", "Scissors"] # array with possible choices

win_phrase = "You win!"                 # phrase to show in case of win
lose_phrase = "You Lose!"               # phrase to show in case of lose
tie_phrase = "It's a tie!"              # phrase to show in case of tie

# functions
def clear():
	"""Function to clear terminal screen"""
	os.system('cls' if os.name == 'nt' else 'clear')


def ask_choice():
	"""Function to ask user's choice and make it title()"""
	return input("Enter your choice (Rock/Paper/Scissors): ").title()


def random_choice(choices_array):
	"""Function to get a random choice from the coices array"""
	return choice(choices_array)


def check_choice(choice, choices_array):
	"""Function to check if choice is valid / or convert 1-letter choice to its long version and check it"""
	if len(choice) == 1:
		choice = convert_choice_to_long(choice)
	return choice if choice in choices_array else False


def convert_choice_to_long(choice):
	"""Function to convert 1-letter choice to its long version"""
	if choice == "R":
		return "Rock"
	elif choice == "P":
		return "Paper"
	elif choice == "S":
		return "Scissors"
	else:
		return "ERROR! UNKNOWN_CHOICE!"


def get_color_code(phrase):
	"""Function to get a color code for the terminal, in dependence on the phrase: win/lose/tie"""
	# color_code = 31 - Red
	# color_code = 32 - Green
	# color_code = 33 - Yellow
	global win_phrase
	global lose_phrase
	global tie_phrase

	if phrase == win_phrase:
		return 32
	elif phrase == lose_phrase:
		return 31
	else: 
		return 33


def check_winner(player_choice, computer_choice):
	"""Function to check the winner and print a result to the console"""
	if player_choice == computer_choice:
		result = tie_phrase
	elif player_choice == "Rock":
		if computer_choice == "Scissors":
			result = win_phrase
		elif computer_choice == "Paper":
			result = lose_phrase
	elif player_choice == "Paper":
		if computer_choice == "Rock":
			result = win_phrase
		elif computer_choice == "Scissors":
			result = lose_phrase
	elif player_choice == "Scissors":
		if computer_choice == "Paper":
			result = win_phrase
		elif computer_choice == "Rock":
			result = lose_phrase
	else:
		result = "SOME_UNEXPECTED_ERROR_OCCURED!PLS_TRY_AGAIN"
	color_code = get_color_code(result)
	print("Your choice - '{}', computer's choice - '{}'. "
		"Result:\033[1;{};40m {} \033[0m".format(player_choice, computer_choice, color_code ,result))


def play_rps():
	"""Function to play the game: combine ask/check choice, take computer's choice and check the winner"""
	global choices

	print(".: *Let's Play in RPS game* :.\n")
	print("\033[1;92;40mRock...\033[0m")
	print("\033[1;92;40mPaper...\033[0m")
	print("\033[1;92;40mScissors...\033[0m\n")
	player_choice = check_choice(ask_choice(), choices)
	if player_choice:
		computer_choice = random_choice(choices)
		#game
		check_winner(player_choice, computer_choice)
	else:
		print("\033[1;31;40mYour choice is invalid! Please choose one of the following: \033[1;32;40m(R)ock/(P)aper/(S)cissors\033[0m\n")


def play_next():
	"""Function to check if a new play needed"""
	allowed_y = ["y", "yes"]
	allowed_n = ["n", "no"]
	tries = 0
	while tries != 5:
		decision = input("Play again? (Y/N): ").lower()
		if decision in allowed_y:
			# clear console
			clear()
			return True
		elif decision in allowed_n:	
			clear()
			print("\n\033[1;35;40mThanks for the game! Bye! \033[0m")
			return False
		else:
			clear()
			print("\033[1;31;40mYour choice is invalid! Please choose one of the following: \033[1;32;40mY or N \033[0m\n")
			print("\033[1;31;50mInvalid input [{}/5]\033[0m".format(tries+1))
			tries += 1
	if tries == 5:
		clear()
		print("\033[1;31;50mInvalid input [{}/5]\033[0m".format(tries))
		print("\033[1;31;40mYour have entered invalid choice 5 times in row. Game is over, Bye! \033[0m\n")
		return False


# main
if __name__ == '__main__':
	# clear terminal
	clear()
	# run 1st time w/o asking 'play next'
	first_play = True
	# while play
	while first_play or play_next():
		play_rps()
		first_play = False
