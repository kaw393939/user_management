import nltk
from nltk.corpus import wordnet as wn
import random

nltk.download('wordnet')
nltk.download('omw-1.4')

def get_words_by_pos(pos_tag):
    """Retrieve words by part of speech (POS) tag from WordNet and filter out multi-word expressions."""
    words = {x.name().split('.', 1)[0] for x in wn.all_synsets(pos_tag)}
    return {word for word in words if '_' not in word}

def generate_nickname() -> str:
    """Generate a URL-safe nickname using verbs and animal names."""
    verbs = list(get_words_by_pos('v'))  # 'v' for verb
    nouns = list(get_words_by_pos('n'))  # 'n' for noun  # 'n' for noun (using nouns to represent animals here)
    number = random.randint(0, 999)
    return f"{random.choice(verbs)}_{random.choice(nouns)}_{number}"