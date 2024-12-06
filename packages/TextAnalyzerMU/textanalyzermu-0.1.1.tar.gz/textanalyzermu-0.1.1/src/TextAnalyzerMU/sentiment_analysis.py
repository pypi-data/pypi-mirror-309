from transformers import pipeline, PipelineException

# Load the emotion detection model
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
        PipelineException: If there is an issue with the emotion classification pipeline.
        Exception: For any other unexpected errors.
    """
    try:
        # Check if the input is a string
        if not isinstance(text, str):
            raise TypeError("The input must be a string.")
        
        # Check if the input is not empty
        if not text.strip():
            raise ValueError("The text cannot be empty.")
        
        # Run the emotion analysis
        result = emotion_pipeline(text) 
        
        # Validate the structure of the result
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
            emotion = result[0].get('label', 'Unknown')
            score = result[0].get('score', 0)
        else:
            raise ValueError("Unexpected result format received from the emotion pipeline.")
        
        return f"The model predicted that this text expresses '{emotion}' with a confidence of {score:.2%}."

    except TypeError as te:
        return f"Error: {te}"
    except ValueError as ve:
        return f"Error: {ve}"
    except PipelineException as pe:
        return f"Error with the emotion classification pipeline: {pe}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


