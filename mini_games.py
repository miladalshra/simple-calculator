import random


def guess_the_number():
    secret_number = random.randint(1, 10)
    print("\nGuess the Number")
    print("I chose a number from 1 to 10.")

    while True:
        try:
            guess = int(input("Your guess: "))
        except ValueError:
            print("Please enter a whole number.")
            continue

        if guess == secret_number:
            print("Correct! You win.")
            break
        elif guess < secret_number:
            print("Too low. Try again.")
        else:
            print("Too high. Try again.")


def rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)

    print("\nRock, Paper, Scissors")
    player_choice = input("Choose rock, paper, or scissors: ").lower()

    if player_choice not in choices:
        print("Invalid choice.")
        return

    print("Computer chose:", computer_choice)

    if player_choice == computer_choice:
        print("It is a draw.")
    elif (
        (player_choice == "rock" and computer_choice == "scissors")
        or (player_choice == "paper" and computer_choice == "rock")
        or (player_choice == "scissors" and computer_choice == "paper")
    ):
        print("You win!")
    else:
        print("Computer wins!")


while True:
    print("\nMini Games")
    print("1. Guess the Number")
    print("2. Rock, Paper, Scissors")
    print("3. Exit")

    choice = input("Choose a game: ")

    if choice == "1":
        guess_the_number()
    elif choice == "2":
        rock_paper_scissors()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")
