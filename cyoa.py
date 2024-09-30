def start():
    print("You are in a dark forest. There are two paths in front of you.")
    print("1. Take the left path.")
    print("2. Take the right path.")
    choice = input("Which path do you choose? (1 or 2): ")
    if choice == "1":
        left_path()
    elif choice == "2":
        right_path()
    else:
        print("Invalid choice. Please choose 1 or 2.")
        start()

def left_path():
    print("You encounter a friendly elf who offers you a gift.")
    print("1. Accept the gift.")
    print("2. Politely decline.")
    choice = input("What do you do? (1 or 2): ")
    if choice == "1":
        print("The elf gives you a magical sword. You win!")
    elif choice == "2":
        print("The elf is offended and casts a spell on you. You lose!")
    else:
        print("Invalid choice. Please choose 1 or 2.")
        left_path()

def right_path():
    print("You find a treasure chest.")
    print("1. Open the chest.")
    print("2. Leave it alone.")
    choice = input("What do you do? (1 or 2): ")
    if choice == "1":
        print("The chest is filled with gold. You win!")
    elif choice == "2":
        print("You walk away and fall into a trap. You lose!")
    else:
        print("Invalid choice. Please choose 1 or 2.")
        right_path()

# Start the adventure
start()