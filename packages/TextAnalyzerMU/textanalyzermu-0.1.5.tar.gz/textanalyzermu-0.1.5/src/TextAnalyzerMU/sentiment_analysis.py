from transformers import pipeline

emotion_pipeline = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=1)

def emotion_analysis(text):
    """
    Detects the specific emotion in a text.
    
    Args:
        text (str): Text to analyze.

    Returns:
        str: Descriptive sentence with the predicted emotion and confidence score.
    
    Raises:
        TypeError: If the input text is not a string.
        ValueError: If the text is empty.
        Exception: For any other unexpected errors.
    """
    try:
        if not isinstance(text, str):
            raise TypeError("The input must be a string.")
        
        if not text.strip():
            raise ValueError("The text cannot be empty.")
        
        result = emotion_pipeline(text)
        
        return result
    
    except TypeError as te:
        return f"Error: {te}"
    except ValueError as ve:
        return f"Error: {ve}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"



# texto2 = 'Happiness often hides in the simple things: the sound of leaves rustling in the wind, the warm embrace of someone you love, or that song that makes you dance without realizing it. It’s a state we create with the little details, a spark that lights up our hearts when we allow ourselves to savor the present moment. '
# print(emotion_analysis(texto2))