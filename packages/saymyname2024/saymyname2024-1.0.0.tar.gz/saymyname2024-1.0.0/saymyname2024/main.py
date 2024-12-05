import re

def say(name=""):
    _name = re.sub(r'[^a-zA-Z]', '', name.strip().lower())
    if _name == 'heisenberg':
        return "You're goddamn right!"
    return "🔫"