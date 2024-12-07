# Text language identifier

This package serves as a wrapper for the most performant text language identifier.

Currently it wraps fasttext (NLLB version).

Before detecting the language, it preprocesses the text to improve results.

## Usage

`lang = textlangid.detect("This is some text.")`

The language is returned in a FLORES-200 language code.
Full list available [here](https://github.com/facebookresearch/flores/blob/main/flores200/README.md#languages-in-flores-200).
