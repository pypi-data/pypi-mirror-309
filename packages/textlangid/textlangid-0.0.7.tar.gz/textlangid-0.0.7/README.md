# Text language identifier

This package serves as a wrapper for the most performant text language identifier.

Currently it wraps fasttext (NLLB version).

Before detecting the language, it preprocesses the text to improve results.

## Usage

```python
%pip install textlangid

import textlangid

lang = textlangid.detect("This is some text.")

top_languages = TextLanguageIdentifier.detect(text, top_k=3)

top_languages_with_confidence = TextLanguageIdentifier.detect(
        text, top_k=3, return_confidence=True
    )

top_languages_with_threshold = TextLanguageIdentifier.detect(
        text, top_k=3, return_confidence=True, confidence_threshold=0.2
    )

```

The language is returned in a FLORES-200 language code.
Full list available [here](https://github.com/facebookresearch/flores/blob/main/flores200/README.md#languages-in-flores-200).
