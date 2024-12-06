from transformers import pipeline

# Load the Named Entity Recognition pipeline
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

def extract_entities(text):
    """
    Extracts the main entities (e.g., persons, locations, organizations) from a text,
    and returns them in a formatted string.

    Args:
        text (str): The text from which to extract entities.

    Returns:
        str: Formatted string with entities grouped by type and their accuracy.
        
    Raises:
        ValueError: If the input text is not a string.
        Exception: For issues with the NER pipeline or unexpected results.
    """

    try:
        # Validate input text type
        if not isinstance(text, str):
            raise ValueError("Input text must be a string.")

        entities = ner_pipeline(text)

        if not entities:
            return "No entities were extracted from the text."

        entity_groups = {
            "PER": [],
            "ORG": [],
            "LOC": [],
            "MISC": []
        }

        excluded_entities = ["Spanish"]  

        for entity in entities:
            entity_type = entity.get('entity_group', None)
            entity_name = entity.get('word', None)
            accuracy = round(entity.get('score', 0), 4)

            if not entity_type or not entity_name:
                continue  # Skip incomplete or malformed entities

            if entity_name not in excluded_entities:
                if entity_type in entity_groups:
                    entity_groups[entity_type].append(f"{entity_name} ({accuracy})")
                    
        result = ""
        for entity_type, entities_list in entity_groups.items():
            if entities_list: 
                result += f"{entity_type}: " + ", ".join(entities_list) + "\n"

        return result.strip() if result else "No relevant entities found."

    except ValueError as ve:
        return f"Error: {ve}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


