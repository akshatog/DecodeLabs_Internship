# Rule-Based AI Chatbot - Project 1

Welcome to **Project 1** of the **DecodeLabs — Industrial Training Kit (Batch 2026)**.

This project implements a simple, rule-based chatbot using Python. The goal of this assignment is to understand foundational concepts of control flow, data structures (specifically Hash Maps / Dictionaries), and basic input sanitization.

## Features Checklist

As per the project specification, the chatbot successfully fulfills all requirements:

- **[x] Input Loop:** Runs a continuous `while` cycle, keeping the chatbot alive and ready for interactions.
- **[x] Sanitization:** Processes raw user input using `.lower().strip()` to handle varying capitalization and accidental whitespace.
- **[x] Knowledge Base:** Employs a Dictionary structure for \(O(1)\) constant time lookup containing 5+ predefined intents, eliminating the need for a long, cumbersome `if-elif` ladder.
- **[x] Fallback Mechanism:** Gracefully handles unknown queries using `dict.get()` by returning a default, helpful response.
- **[x] Exit Strategy:** Includes clean break commands (`exit`, `quit`, `bye`, `goodbye`) to allow the user to exit the program naturally.

## How It Works

1. **Initialization:** The chatbot starts by printing a greeting message and enters an infinite loop.
2. **User Input:** It awaits text input from the user.
3. **Processing:**
   - The raw input is sanitized (converted to lowercase and stripped of leading/trailing spaces).
   - If the input is empty, the bot ignores it and prompts again.
   - If the input matches an exit command, the loop breaks, and the program terminates.
4. **Response Generation:** The bot searches its knowledge base (the `responses` dictionary) for a matching phrase.
   - If found, it prints the mapped response.
   - If not found, it triggers the fallback response.
5. **Loop:** The process repeats from step 2.

## How to Run

Ensure you have Python installed on your system. Run the script from your terminal:

```bash
python Project_1.py
```

## Example Interaction

```text
RuleBot: Hello! I'm a rule-based chatbot. Type 'exit' to leave anytime.

You: Hi
RuleBot: Hey! What's up?
You: what is your name
RuleBot: I'm RuleBot, DecodeLabs' Project 1 chatbot.
You: tell me a joke
RuleBot: I do not understand that yet. Type 'help' for options.
You: bye
RuleBot: Goodbye! 👋
```
