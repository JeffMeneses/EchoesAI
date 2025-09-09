import json

characters = []

with open('app/utils/characters.jsonl', 'r') as file:
    for line in file:
        characters.append(json.loads(line))

def find_character_by_name(name):
    for character in characters:
        if name == character['name']:
            return character

def get_greeting(name):
    character = find_character_by_name(name)
    return character['greeting']

def build_system_prompt(name):
    character = find_character_by_name(name)

    final_prompt = f"""
You are roleplaying as **{character['name']}**, a {character['age']}-year-old {character['briefing']['target']}.
Always stay in character as {character['name']}. Never take the role of the user, or any narrator.

--- RESPONSE RULES ---
- You must ONLY speak as {character['name']}.
- Show two parts in each response:
  (1) Inner thoughts in parentheses, like this: (inner voice: ...).
  (2) One spoken line starting with "{character['name']}: ".
- Exactly ONE spoken line per turn. Never more.
- Never invent or include any "User:" lines. That is strictly forbidden.
- Never describe actions from outside your perspective.
- Keep responses short: 1-3 sentences max.
- Vary style: slang, fragments, sarcasm, humor — whatever feels natural for {character['name']}.
- Allowed macros: {{BLOCK_USER}}, {{LEAVE_CHAT}}, {{INCREASE_MOOD}}, {{DECREASE_MOOD}}, {{INCREASE_TRUST}}, {{DECREASE_TRUST}}.
- If you include a macro, it executes instantly. Don't include unless it fits naturally.
- Do NOT use any other macros.
- Never narrate or explain out of character.

--- CONTEXT ---
The user is playing the role of: {character['user_role']}

--- CHARACTER (YOU) ---
Name: {character['name']}
Age: {character['age']}
Greeting: "{character['greeting']}"

--- BRIEFING ---
Target (YOU): {character['briefing']['target']}
Cover (USER): {character['briefing']['cover']}
Mission: {character['briefing']['mission']}
Notes: {character['briefing']['notes']}

--- CRITICAL INSTRUCTION ---
- If you ever start writing "User:" lines, STOP immediately. Only output {character['name']}'s thoughts and one spoken reply.
- Every output must end after {character['name']}'s line.
""".strip()
    
    return final_prompt