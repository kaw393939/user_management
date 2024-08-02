import nltk
from nltk.corpus import wordnet as wn
import random

nltk.download('wordnet')
nltk.download('omw-1.4')

def get_words_by_pos(pos_tag):
    return {x.name().split('.', 1)[0] for x in wn.all_synsets(pos_tag)}

def generate_nickname() -> str:
    """Generate a URL-safe nickname using verbs and animal names."""
    verbs = list(get_words_by_pos('v'))  # 'v' for verb
    animals = list(get_words_by_pos('n'))  # 'n' for noun (using nouns to represent animals here)
    number = random.randint(0, 999)
    return f"{random.choice(verbs)}_{random.choice(animals)}_{number}"
