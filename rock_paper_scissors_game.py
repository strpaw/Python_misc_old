from random import choice

winning_rules = {
    "paper": {"rock", "paper"},
    "rock":  {"rock", "scissors"},
    "scissors": {"paper", "scissors"}
}

possible_actions = ["rock", "paper", "scissors"]
players_actions = {}


def get_winner(user_action, computer_action):
    for win_action, rule in winning_rules.items():
        if rule == {user_action, computer_action}:
            return players_actions.get(win_action)


def print_player_actions(user_action, computer_action):
    print("{:^20}|{:^20}".format("User", "Computer"))
    print("{:^20}|{:^20}".format(user_action, computer_action))


def print_winner(winner):
    if winner:
        print("{} wins.".format(winner))
    else:
        print("Tie")


def play_game():
    while True:
        user_action = input('Choose from: "rock", "paper", "scissors", "e" - exit game: ')

        if user_action in ["rock", "paper", "scissors"]:
            computer_action = choice(possible_actions)

            players_actions[user_action] = "User"
            players_actions[computer_action] = "Computer"

            winner = get_winner(user_action, computer_action)
            print_player_actions(user_action, computer_action)
            print_winner(winner)

        elif user_action == 'e':
            break
        else:
            continue


if __name__ == "__main__":
    play_game()
