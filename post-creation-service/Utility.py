import re

def last_sentence(paragraph):
    # Use regex to split the paragraph into sentences based on common sentence-ending punctuation
    # (periods, question marks, exclamation points) followed by optional whitespace.
    sentences = re.split(r'[.!?]+\s*', paragraph)

    # Filter out any empty strings that might result from splitting
    sentences = [s.strip() for s in sentences if s.strip()]

    # Get the last sentence
    if sentences:
        last_sentence = sentences[-1]
    return last_sentence