"""
Project 1: Rule-Based AI Chatbot (Advanced Version)
DecodeLabs — Industrial Training Kit (Batch 2026)

Goal: A rule-based chatbot featuring OOP, fuzzy matching, keyword matching,
randomized responses, and robust sanitization.
"""

import string
import random
import difflib

class RuleBot:
    def __init__(self):
        # Intents mapped to lists of possible responses for variety
        self.exact_responses = {
            "hello": ["Hi there! How can I help you today?", "Hello! What's on your mind?", "Greetings!"],
            "hi": ["Hey! What's up?", "Hi!", "Hello there!"],
            "thank you": ["You're welcome!", "Glad to help!", "Anytime!"],
            "thanks": ["Anytime!", "No problem!", "You got it!"],
            "help": ["Try greeting me, asking my name, or how I'm doing. Type 'exit' to quit."]
        }
        
        # Keyword tuple mapped to list of responses
        self.keyword_responses = {
            ("how", "are", "you"): ["I'm just a bunch of if-else logic, but I'm doing great!", "Doing well, thanks!"],
            ("what", "is", "name"): ["I'm RuleBot, DecodeLabs' Project 1 chatbot.", "They call me RuleBot."],
            ("what", "can", "do"): ["Right now I can only respond to a few fixed phrases — no learning, just pure logic."]
        }

        self.exit_commands = {"exit", "quit", "bye", "goodbye"}

    def sanitize_input(self, text: str) -> str:
        """Lowercases, strips whitespace, and removes punctuation."""
        clean_text = text.lower().strip()
        return clean_text.translate(str.maketrans('', '', string.punctuation))

    def get_response(self, user_input: str) -> str:
        """Pipeline: Exact Match -> Fuzzy Match -> Keyword Match -> Fallback"""
        # 1. Try an exact match first
        if user_input in self.exact_responses:
            return random.choice(self.exact_responses[user_input])
        
        # 2. Try Fuzzy Matching for exact intents (handles typos)
        close_matches = difflib.get_close_matches(user_input, self.exact_responses.keys(), n=1, cutoff=0.7)
        if close_matches:
            best_match = close_matches[0]
            return random.choice(self.exact_responses[best_match])

        # 3. Try Keyword Matching
        words = set(user_input.split())
        for keywords, replies in self.keyword_responses.items():
            # If all keywords in a tuple are in the user's input
            if all(kw in words for kw in keywords):
                return random.choice(replies)

        # 4. Fallback
        return "I do not understand that yet. Type 'help' for options."

    def run(self):
        print("RuleBot: Hello! I'm an advanced rule-based chatbot. Type 'exit' to leave anytime.\n")
        
        while True:
            raw_input_text = input("You: ")
            clean_input = self.sanitize_input(raw_input_text)
            
            # Skip empty inputs
            if not clean_input:
                continue
                
            # Exit strategy
            if clean_input in self.exit_commands:
                bye_messages = ["Goodbye! 👋", "See ya!", "Catch you later!"]
                print(f"RuleBot: {random.choice(bye_messages)}")
                break

            # Fetch and print response
            reply = self.get_response(clean_input)
            print(f"RuleBot: {reply}")


if __name__ == "__main__":
    bot = RuleBot()
    bot.run()