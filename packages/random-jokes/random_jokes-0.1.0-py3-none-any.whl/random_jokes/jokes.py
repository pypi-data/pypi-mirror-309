import random

JOKES = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you get when you cross a snowman and a vampire? Frostbite.",
    "Why don’t eggs tell jokes? Because they might crack up.",
    "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats.",
    "What’s orange and sounds like a parrot? A carrot!",
]

def get_random_joke():
    """Returns a random joke from the list."""
    return random.choice(JOKES)
