from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein

def text_similarity(text1, text2, method):
    """ Measuring text similarity using different methods.
    Args:
        text1 (str): First text
        text2 (str): Second text
        method (str): Method to use for measuring similarity. Options are: 'TF-IDF', 'Jaccard Similarity', 'Levenshtein'

    Raises:
        ValueError: If method is not recognized

    Returns:
        str: A phrase indicating the similarity between the two texts
    """

    text1 = text1.lower()
    text2 = text2.lower()

    # Method 1: TF-IDF (Cosine Similarity)
    if method == "TF-IDF":   
        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        similarity_value = similarity[0][0]
        if similarity_value > 0.8:
            similarity_description = "high"
        elif similarity_value > 0.5:
            similarity_description = "medium"
        else:
            similarity_description = "low"

        return f"The texts have a {similarity_description} similarity of {similarity_value:.2f}"

    # Method 2: Jaccard Similarity
    elif method == "Jaccard Similarity":
        set1 = set(text1.split())
        set2 = set(text2.split())

        common_set = set1 & set2
        unique_set = set1 | set2

        if len(unique_set) == 0:
            jaccard_index = 1.0  
        else:
            jaccard_index = len(common_set) / len(unique_set)

        if jaccard_index > 0.8:
            similarity_description = "high"
        elif jaccard_index > 0.5:
            similarity_description = "medium"
        else:
            similarity_description = "low"

        return f"The texts have a {similarity_description} Jaccard similarity of {jaccard_index:.2f}"

    # Method 3: Levenshtein Distance
    elif method == "Levenshtein":
        distance = Levenshtein.distance(text1, text2)
        max_length = max(len(text1), len(text2))

        if max_length == 0:  
            similarity = 1.0
        else:
            similarity = 1 - (distance / max_length)

        if similarity > 0.8:
            similarity_description = "high"
        elif similarity > 0.5:
            similarity_description = "medium"
        else:
            similarity_description = "low"

        return f"The texts have a {similarity_description} Levenshtein similarity of {similarity:.2f}"

    # If the method is not recognized, raise an error
    else:
        raise ValueError("Unrecognized method. Use 'TF-IDF', 'Jaccard Similarity', or 'Levenshtein'.")
