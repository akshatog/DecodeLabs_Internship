# Rule-Based AI Chatbot - Project 1 (Advanced Version)

Welcome to **Project 1** of the **DecodeLabs — Industrial Training Kit (Batch 2026)**.

This project implements an advanced rule-based chatbot using Python. It builds upon foundational concepts by utilizing Object-Oriented Programming (OOP) and introducing robust natural language handling techniques.

## Features Checklist

- **[x] Object-Oriented Architecture:** Encapsulates the chatbot's state, knowledge base, and logic within a reusable `RuleBot` class.
- **[x] Robust Sanitization:** Processes raw user input using `.lower().strip()` and strips all punctuation (using the `string` module) to ensure trailing commas or exclamation marks don't break the logic.
- **[x] Fuzzy Matching:** Utilizes Python's `difflib` to gracefully handle user typos (e.g., "helo" will correctly match "hello").
- **[x] Keyword Matching:** Checks for specific keyword combinations within a sentence rather than requiring exact full-string matches (e.g., matching "what is your name" even if phrased as "what is your bot name").
- **[x] Randomized Responses:** Maps intents to a list of potential replies, using `random.choice()` to make the bot feel more dynamic and less repetitive.
- **[x] Input Loop & Exit Strategy:** Runs a continuous `while` cycle with clean break commands (`exit`, `quit`, `bye`, `goodbye`).

## How It Works

1. **Initialization:** The `RuleBot` class is instantiated, loading its exact response dictionary and keyword response dictionary.
2. **User Input & Sanitization:** The bot awaits input, removes case variations, and strips all punctuation.
3. **Response Pipeline:**
   - **Step 1 (Exact Match):** Checks if the exact string matches a known intent.
   - **Step 2 (Fuzzy Match):** Uses `difflib.get_close_matches` to catch slight misspellings.
   - **Step 3 (Keyword Match):** Scans the input for specific keyword tuples.
   - **Step 4 (Fallback):** If all else fails, a default fallback message is returned.
4. **Loop:** The process repeats until an exit command is detected.

## How to Run

Ensure you have Python installed on your system. Run the script from your terminal:

```bash
python Project_1.py
```

## Example Interaction

```text
RuleBot: Hello! I'm an advanced rule-based chatbot. Type 'exit' to leave anytime.

You: helo! 
RuleBot: Hi there! How can I help you today?
You: what is your real name?
RuleBot: They call me RuleBot.
You: bye
RuleBot: Catch you later!
```
