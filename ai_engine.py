import difflib
import random

sentences = [
    "I would like to order a cup of coffee",
    "Artificial intelligence is changing the world",
    "Practice makes a person perfect",
    "Communication skills are very important",
    "I am learning software development"
]

def generate_sentence():
    return random.choice(sentences)


def evaluate_speech(original, spoken):

    original_words = original.lower().split()
    spoken_words = spoken.lower().split()

    wrong_words = []

    for word in original_words:
        if word not in spoken_words:
            wrong_words.append(word)

    similarity = difflib.SequenceMatcher(
        None,
        original.lower(),
        spoken.lower()
    ).ratio()

    accuracy = int(similarity * 100)

    fluency = max(50, accuracy - len(wrong_words)*5)

    if accuracy > 90:
        feedback = "Excellent pronunciation."
        level = "Advanced"
    elif accuracy > 70:
        feedback = "Good, but improve clarity."
        level = "Intermediate"
    else:
        feedback = "Try again carefully."
        level = "Beginner"

    retry = accuracy < 70

    return {
        "accuracy": accuracy,
        "fluency": fluency,
        "feedback": feedback,
        "wrong_words": wrong_words,
        "level": level,
        "retry": retry
    }