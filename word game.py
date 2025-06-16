store = []
try_p = 8
guessed_word = "python"  # Directly use a string
hint = guessed_word[0] + guessed_word[-1]  # First and last letter

a = input("Enter your name: ")
print("Welcome to the word game,", a)
print("You have 6 chances to guess the word.")

for guess in range(try_p):
    while True:
        letter = input("Enter a letter: ").lower()
        if len(letter) == 1:
            break
        else:
            print("Oops..! Please guess a single letter!")

    if letter in guessed_word:  # Only store correct letters
        if letter not in store:  # Avoid duplicate storage
            store.append(letter)
        print("Good guess!")
    else:
        print("Oops..! Try again!")

    if guess == 3:  # Giving clue after 3 attempts
        print()
        clue_req = input("Do you want a clue? (yes/no): ")
        if clue_req.lower().startswith('y'):
            print("\nClue: The first and last letter of the word is", hint)
        else:
            print("You are very confident!")

print("\nNow let's see what you have guessed so far.")
print("You have guessed", len(store), "correct letters.")
print("These letters are:", store)

word_guess = input("Now guess the word: ").lower()
if word_guess == guessed_word:  # Comparing correctly
    print("Congratulations! You have guessed the word correctly 🎉")
else:
    print("Sorry! The word was", guessed_word)

print("Thanks for playing the game,", a)
print("Hope you enjoyed the game!")
print("Goodbye!")
