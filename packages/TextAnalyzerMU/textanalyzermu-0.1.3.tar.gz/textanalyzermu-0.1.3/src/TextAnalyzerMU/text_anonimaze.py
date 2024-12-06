def text_anonimaze(text):
    """Anonymize text by reversing the order of words or characters in the words.

    Args:
        text (str): Text to be anonymized.

    Returns:
        str: Anonymized text. The function either reverses the word order or each word's characters.
    
    Raises:
        TypeError: If the input is not a string.
        ValueError: If the input string is empty.
    """
    
    # Ensure input is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    # Ensure input is not an empty string
    if not text:
        raise ValueError("Input text cannot be empty.")

    # Split the text into words, reverse each word's characters, and join them back together
    words = text.split()
    
    # Check if there are words in the text
    if len(words) == 0:
        raise ValueError("Input text contains no words to anonymize.")

    # Reverse the characters in each word
    reversed_words = [word[::-1] for word in words]

    # Join the reversed words back into a single string
    reversed_text = ' '.join(reversed_words)
    
    return reversed_text



