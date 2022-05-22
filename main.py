# Import necessary modules
import turtle as trtl
import random as rand

# five_letter_words.txt is a list of common five letter words pulled from https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt
word_list_file = open("wordle/five_letter_words.txt", "r")
# Returns list with each line being a string in the list though includes \n with each string
unformatted_word_list = word_list_file.readlines()
# Create new list with the \n removed from each string
word_list = []
for word in unformatted_word_list:
    word_list.append(word.strip())

# Close the word list file
word_list_file.close()

# Select a random word from the word list
word_answer = rand.choice(word_list)
letter_amount = len(word_answer)

# Intialize a list of all the letters in the alphabet
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Initialize letter and row order for entering input
letter_order = 0
row_order = 0
word_guess = []

# Initialize Turtle Screen
wn = trtl.Screen()
wn.tracer(False)
wn.setup(width=1.0, height=1.0)

drawer = trtl.Turtle()
drawer.hideturtle()

#---Function definitions---
# Define function to draw a single square
def draw_square():
    drawer.pendown()
    sides = 0
    while sides < 4:
        drawer.forward(50)
        drawer.right(90)
        sides += 1

# Define function to draw the game board by utilizing the draw square function and creating 6 rows with 5 columns
def draw_board():
    squares = 0
    x_coordinate = -187.5
    y_coordinate = 200
    while squares < 30:
        drawer.penup()
        drawer.goto(x_coordinate, y_coordinate)
        draw_square()
        x_coordinate += 75
        squares += 1
        if squares % 5 == 0:
            y_coordinate -= 75
            x_coordinate = -187.5

# Define function that writes the title of the game and directions on the turtle screen
def write_text():
    drawer.penup()
    drawer.goto(0, 225)
    drawer.write("Guess Words with Words", font = ("Times", 42, "bold"), align = 'center')
    drawer.goto(-425, 25)
    drawer.write("Type letter keys through your keyboard to input your guesses", font = ("Times", 16, "bold"), align = 'center')
    drawer.goto(-425, -25)
    drawer.write("Press the Enter key to submit a word guess", font = ("Times", 16, "bold"), align = 'center')
    drawer.goto(400, 50)
    drawer.color("gray")
    drawer.write("Gray - Letter is not in word", font = ("Times", 16, "bold"), align = 'center')
    drawer.goto(400, 0)
    drawer.color("gold")
    drawer.write("Yellow - Letter is in word but not in the correct location", font = ("Times", 16, "bold"), align = 'center')
    drawer.goto(400, -50)
    drawer.color("green")
    drawer.write("Green - Letter is in word and in the correct location", font = ("Times", 16, "bold"), align = 'center')
    # Change pen color back to black for all other output
    drawer.color("black")

# Define function that can color a box at any row and column within the game and then redraw the letter over it
def color_box(color, letter_order, row_order, letter):
    # Color box
    square_x_coordinate = ((letter_order*50) + (letter_order*25)) + -187.5
    square_y_coordinate = ((row_order) * -75) + 200
    drawer.penup()
    drawer.goto(square_x_coordinate, square_y_coordinate)
    drawer.color(color)
    drawer.pendown()
    drawer.begin_fill()
    draw_square()
    drawer.end_fill()
    # Redraw letter
    letter_x_coordinate = ((letter_order*50) + (letter_order*25)) + -162.5
    letter_y_coordinate = ((row_order) * -75) + 145
    drawer.color("black")
    drawer.penup()
    drawer.goto(letter_x_coordinate, letter_y_coordinate)
    drawer.write(letter.upper(), font = ("Times", 48, "bold"), align = 'center')

# Define function to display a congratulations to the screen
def display_win():
    drawer.penup()
    drawer.goto(0, -300)
    drawer.write("Congrats! You guessed the word correctly.", font = ("Times", 32, "bold"), align = 'center')

# Define function to display the word_answer to the user
def display_word():
    drawer.penup()
    drawer.goto(0, -300)
    drawer.write(f"The correct word was {word_answer.title()}.", font = ("Times", 32, "bold"), align = 'center')

# Check if user inputted word is an english word
def is_word(word_guess):
    global english_word_list
    word_guess_string = ''.join(word_guess)
    appearances_in_list = english_word_list.count(word_guess_string)
    if appearances_in_list > 0:
        return True
    else:
        return False

# Define function to be called whenever a key is pressed
def handle_letter_entry(key):
    global letter_order
    global row_order
    letter_order += 1
    word_guess.append(key)
    letter_x_coordinate = (((letter_order-1)*50) + ((letter_order-1)*25)) + -162.5
    letter_y_coordinate = (row_order * -75) + 145
    if letter_order >= 5:
        letter_order = letter_order % 5
    drawer.penup()
    drawer.goto(letter_x_coordinate, letter_y_coordinate)
    drawer.write(key.upper(), font = ("Times", 48, "bold"), align = 'center')

# Define function to handle guesses of words to be called when the return key is pressed
def handle_word_guess():
    # Recall global variables
    global word_guess
    global row_order
    check_word_guess(word_guess, row_order)
    # Reset list of letters in guess and increment row order
    row_order += 1
    word_guess = []


# Evaluate the word guess and output the appropriate colors to the screen
def check_word_guess(word_guess, row_order):
    guess_letter_order = 0
    correct_guesses = 0
    for letter in word_guess:
        # Determine if letter is in the word then display box as yellow if it is
        if letter in word_answer:
            letter_index_guess = word_guess.index(letter, guess_letter_order)
            color_box("yellow", letter_index_guess, row_order, word_guess[letter_index_guess])
         # Color box gray if letter is not in word
        else:
            letter_index_guess = word_guess.index(letter, guess_letter_order)
            color_box("gray", letter_index_guess, row_order, word_guess[letter_index_guess])
        # Determine if the guess corresponds with a letter in the word that is in the exact same order
        if letter == word_answer[guess_letter_order]:
            letter_index_guess = word_guess.index(letter, guess_letter_order)
            color_box("green", letter_index_guess, row_order, word_guess[letter_index_guess])
            correct_guesses += 1
        guess_letter_order += 1
    # Display to the user that they guessed correctly.
    if correct_guesses == 5:
        display_win()
    # Display to the user the word answer signaling that they lost the game
    if correct_guesses != 5 and row_order == 5:
        display_word()
    


# Call function to draw the board
draw_board()
# Call function to write text
write_text()

# Update the screen when program has been fully interpreted
wn.update()

# Listen for events
wn.listen()

# Listen for keypresses by making instances of an onkeypress handler for each letter in the alphabet through using a for loop that iterates through a list of the letters in the alphabet
for letter in alphabet:
    # Use a lambda so that we can pass the key to the function the handler is calling
    wn.onkeypress(lambda key = letter: handle_letter_entry(key), letter)

# Creake key listener for the enter key to submit a guess
wn.onkeypress(handle_word_guess, "Return")

# Allow window to persist
wn.mainloop()