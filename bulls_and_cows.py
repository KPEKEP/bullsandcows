from itertools import permutations
import random
import os

def generate_candidates():
    """Generates a list of candidates of all possible digits combinations."""
    return [''.join(item) for item in permutations('0123456789', 4)]

def safe_input(message):
    """Reads the number of cows or bulls safely."""
    while True:
        try:
            number = int(input(message))
            if 0 <= number <= 4:
                return number
        except ValueError:
            pass
        print("Wrong input. Let's try again.")

def get_human_feedback(turn, guess):
    """Reads human feedback and returns as tuple (bulls, cows)."""
    print(f"AI turn {turn}. AI guess is: {guess}")
    bulls = safe_input("How many bulls? ")
    if bulls >= 4:
        return (4, 0)
    cows = safe_input("How many cows? ")
    return (bulls, cows)

def get_guess_response(guess, secret):
    """Return (bulls, cows) tuple for the given guess and the secret number."""
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(min(guess.count(x), secret.count(x)) for x in set(secret)) - bulls
    return (bulls, cows)

def filter_by_guess(guess, response, candidates):
    """Filter given candidates by guess."""
    return [candidate for candidate in candidates if get_guess_response(guess, candidate) == response]

def player_guess(turn):
    """Player makes a guess and inputs it."""
    print(f"Your turn {turn}. Make your guess of 4 different digits:")
    while True:
        guess = input()
        if len(set(guess)) == 4 and guess.isdigit() and len(guess) == 4:
            return guess
        print("Invalid guess. Ensure it is a 4-digit number with unique digits.")

def clear_screen():
    """Clears the command line screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_turn_tables(human_turns, ai_turns):
    """Displays the turns of both human and AI side by side."""
    print(f"{'Human Turns':<20}{'AI Turns':>20}")
    print("="*40)
    for i in range(max(len(human_turns), len(ai_turns))):
        human_turn = (f"{i+1}) "+ human_turns[i]) if i < len(human_turns) else ""
        ai_turn = (f"{i+1}) "+ ai_turns[i]) if i < len(ai_turns) else ""
        print(f"{human_turn:<20}|{ai_turn:>20}")

def main():
    # Game setup
    candidates = generate_candidates()
    player_secret = ''.join(random.sample('0123456789', 4))  # Ensure player's secret is unique digits
    
    human_turns = []
    ai_turns = []
    
    turn = 1
    ai_response = (0, 0)
    player_response = (0, 0)
    
    while ai_response != (4, 0) and player_response != (4, 0):
        clear_screen()
        
        # Display turns
        display_turn_tables(human_turns, ai_turns)
        
        if len(candidates) < 1:
            print("It looks like you have provided incorrect feedback to the AI guess at some point. Game Over.")
            return
        
        print(f"\nTurn {turn} starts:")
    
        # AI makes a guess
        ai_guess = random.choice(candidates)
        ai_response = get_human_feedback(turn, ai_guess)
        candidates = filter_by_guess(ai_guess, ai_response, candidates)
        ai_turns.append(f"{ai_guess}: {ai_response[0]}B {ai_response[1]}C")
    
        # Player makes a guess
        player_guess_input = player_guess(turn)
        player_response = get_guess_response(player_guess_input, player_secret)
        human_turns.append(f"{player_guess_input}: {player_response[0]}B {player_response[1]}C")
    
        if ai_response == (4, 0):
            print(f"AI won in {turn} turns!")
        elif player_response == (4, 0):
            print(f"Congratulations! You won in {turn} turns!")
        
        turn += 1
    
    if ai_response == (4, 0) and player_response == (4, 0):
        print("It's a tie!")
    elif ai_response == (4, 0):
        print(f"AI wins the game! AI's secret number was: {player_secret}")
    elif player_response == (4, 0):
        print("You win the game!")

if __name__ == '__main__':
    main()