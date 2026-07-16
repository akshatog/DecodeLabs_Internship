"""
Project 1: Rule-Based AI Chatbot
DecodeLabs — Industrial Training Kit (Batch 2026)

Goal: A simple rule-based chatbot that responds to predefined user inputs
using if-else / dictionary lookup logic, running in a continuous loop.

Spec checklist (from the brief):
  [x] INPUT LOOP      -> continuous while cycle
  [x] SANITIZATION    -> handle case & whitespace (.lower().strip())
  [x] KNOWLEDGE BASE  -> dictionary with 5+ intents
  [x] FALLBACK        -> default response for unknowns (dict.get())
  [x] EXIT STRATEGY   -> clean break command
"""

# ---------------------------------------------------------------
# PHASE 0: Knowledge Base
# Dictionary lookup = O(1) constant time, unlike an if-elif ladder
# which grows O(n) as you add more rules. This is the "Pivot to
# Hash Maps" the slides talk about.
# ---------------------------------------------------------------
responses = {
    "hello": "Hi there! How can I help you today?",
    "hi": "Hey! What's up?",
    "how are you": "I'm just a bunch of if-else logic, but I'm doing great!",
    "what is your name": "I'm RuleBot, DecodeLabs' Project 1 chatbot.",
    "what can you do": "Right now I can only respond to a few fixed phrases — "
                        "no learning, just pure logic.",
    "help": "Try greeting me, asking my name, or how I'm doing. Type 'exit' to quit.",
    "thank you": "You're welcome!",
    "thanks": "Anytime!",
}

EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye"}


def get_response(user_input: str) -> str:
    """
    Look up a cleaned user input in the knowledge base.
    Uses dict.get() for an atomic lookup + fallback in one line,
    instead of a long if-elif chain.
    """
    return responses.get(user_input, "I do not understand that yet. Type 'help' for options.")


def run_chatbot():
    print("RuleBot: Hello! I'm a rule-based chatbot. Type 'exit' to leave anytime.\n")

    # ---------------------------------------------------------------
    # PHASE 1: The Heartbeat — infinite loop until the kill command
    # ---------------------------------------------------------------
    while True:
        raw_input_text = input("You: ")

        # PHASE 1: Sanitization — normalize case & strip whitespace
        clean_input = raw_input_text.lower().strip()

        # Exit strategy — clean break out of the loop
        if clean_input in EXIT_COMMANDS:
            print("RuleBot: Goodbye! 👋")
            break

        # Skip empty input instead of matching it against the dict
        if not clean_input:
            continue

        reply = get_response(clean_input)
        print(f"RuleBot: {reply}")


if __name__ == "__main__":
    run_chatbot()