import fasttext
from huggingface_hub import hf_hub_download
from processors import TextProcessor

# Download and load the FastText model
model_path = hf_hub_download(
    repo_id="facebook/fasttext-language-identification", filename="model.bin"
)
model = fasttext.load_model(model_path)


class TextLanguageIdentifier:
    @staticmethod
    def detect(text, top_k=1, return_confidence=False, confidence_threshold=0.0):
        """
        Predict the language(s) of the given text.

        Args:
            text (str): The input text to analyze.
            top_k (int, optional): The number of top predictions to return. Defaults to 1.
            return_confidence (bool, optional): Whether to include confidence scores in the result. Defaults to False.
            confidence_threshold (float, optional): Minimum confidence score for predictions to be included. Defaults to 0.0.

        Returns:
            str, list, or list of dict: A single language code if top_k is 1 and return_confidence is False.
            A list of language codes if top_k > 1 and return_confidence is False.
            A list of dict with languages and their confidence scores if return_confidence is True.
        """
        # Preprocess the text
        text = TextProcessor.preprocess_for_lang_id(text)

        # If the text is too short, return "unknown"
        if len(text) <= 3:
            return "unknown"

        # Predict the language(s) of the text
        prediction = model.predict(text, k=top_k)
        languages = [label.replace("__label__", "") for label in prediction[0]]
        confidences = prediction[1]

        # Filter results based on the confidence threshold
        filtered_results = [
            (lang, conf)
            for lang, conf in zip(languages, confidences)
            if conf >= confidence_threshold
        ]

        # Handle case when no results pass the threshold
        if not filtered_results:
            return "unknown" if top_k == 1 and not return_confidence else []

        # If return_confidence is True, return a list of dicts
        if return_confidence:
            return [{lang: conf} for lang, conf in filtered_results]

        # Otherwise, extract languages and handle top_k
        filtered_languages = [lang for lang, _ in filtered_results]
        if top_k == 1:
            return filtered_languages[0] if filtered_languages else "unknown"
        return filtered_languages


# Example usage
if __name__ == "__main__":
    text = "Ceci est un texte en français.%20  ✏️"

    # Get the top 1 language
    lang = TextLanguageIdentifier.detect(text)
    print(lang)

    # Get the top 3 languages
    top_languages = TextLanguageIdentifier.detect(text, top_k=5)
    print(top_languages)

    # Get the top 3 languages with confidence scores
    top_languages_with_confidence = TextLanguageIdentifier.detect(
        text, top_k=3, return_confidence=True
    )
    print(top_languages_with_confidence)

    # Get the top 3 languages with confidence scores and a threshold
    top_languages_with_threshold = TextLanguageIdentifier.detect(
        text, top_k=5, return_confidence=True, confidence_threshold=0.2
    )
    print(top_languages_with_threshold)
