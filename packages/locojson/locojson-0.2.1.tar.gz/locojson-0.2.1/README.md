# LocoJSON

LocoJSON is a brand new library for multilingual support in Python programs, designed to be the lightest possible. It uses only the standard library and has no external dependencies.

However, LocoJSON depends on a core library called [LocoCore](https://github.com/drago-suzuki58/LocoCore). LocoCore provides common multilingual support features, and LocoJSON adds JSON-based translation functionality on top of it.

Other Language LEADME (GitHub)
[Japanese](https://github.com/drago-suzuki58/LocoJSON/blob/main/README.ja.md)

## Features

- **Easy Calls**:

  You can easily call translations by writing `loc.key1.key2.key3()`, improving code readability. For more details, please refer to the documentation.

- **Flexible Calls**:

  If you want to output in English just this time, you can temporarily change the language by writing `loc.key1("en")`.

- **Easy-to-understand JSON Translations**:

  Translations are in JSON format, making it easy to load files corresponding to each language.

- **Hierarchical Translation Structure**:

  You can handle multiple keys hierarchically, such as `key1.key2.key3`, making it comfortable to use even when the data grows.

- **Detailed Log Output**:

  When translation keys are incomplete or errors occur, detailed logs including the file name and line number of the relevant part are output, making troubleshooting easy.

- **Fallback**:

  If a translation corresponding to the language is not found, it automatically falls back to the default language set. If there is no translation at all, the translation ID is output as is, clearly notifying the developer.

## Installation

Install from PyPI

```sh
pip install locojson
```

Alternatively, you can install it from the GitHub repository:

```sh
python -m pip install git+https://github.com/drago-suzuki58/LocoJSON
```

## Sample Code

Basic Usage

`main.py`
```python
from locojson import LocoJSON

# Set the default language to Japanese and the fallback language to English
loc = LocoJSON(locale="ja", fallback_locale="en", locale_dir="loc")

# こんにちは
print(loc.greeting.hello())

# こんにちは！太郎さん
print(loc.greeting.hello_to_user(user="太郎"))
```

Temporarily Specify Language for Translation

`main.py`
```python
# Hello
print(loc.greeting.hello("en"))

# Hello! John
print(loc.greeting.hello_to_user("en", user="John"))
```

Fallback Example
t notifies the relevant line and file name where it was called, supporting development.

`main.py`
```python
# Log: 2024-11-17 20:23:03 | WARNING    | main.py:18 - Missing translation: greeting.hello in: fr, return key name
# Hello
print(loc.greeting.hello("fr")) # Non-existent translation language

# Log: 2024-11-17 20:23:03 | WARNING    | main.py:23 - Missing translation: greeting.goodbye in: ja, falling back to en
# Log: 2024-11-17 20:23:03 | WARNING    | main.py:25 - Missing translation: greeting.goodbye in: en, return key name
# greeting.goodbye
print(loc.greeting.goodbye())
```

Unused Arguments Example
It notifies the relevant line and file name in the log, similar to fallback.

`main.py`
```python
# Log: 2024-11-17 20:23:03 | WARNING    | main.py:29 - Unused keys: {'message': 'hogehoge'}
# こんにちは
print(loc.greeting.hello(message="hogehoge"))
```

Translation Files Used in `main.py`

`loc/ja.json`
```json
{
    "greeting" : {
        "hello" : "こんにちは",
        "hello_to_user" : "こんにちは！{user}さん"
    },
    "sample" : "サンプル"
}
```

`loc/en.json`
```json
{
    "greeting" : {
        "hello" : "Hello",
        "hello_to_user" : "Hello! {user}"
    },
    "sample" : "Sample"
}
```

In addition to the above sample code, practical examples are available in the [example](https://github.com/drago-suzuki58/LocoJSON/tree/main/examples) folder. Please take a look.

## Q&A

### What language codes should I use for translations?

Basically, you are free to use any language code as long as it matches the JSON file name. (Even `UwU.json` will be recognized correctly!) However, for readability, we recommend using standard formats such as ISO 639-1 (`en`, etc.) or ISO-3166 (`US`).

### Are default and fallback languages required?

The default language is required, but the fallback language is not. If not set, `en` will be automatically set as the fallback language.

### Can I use formats other than JSON (e.g., YAML)?

No, currently only JSON is supported. If there is high demand, we may develop a separate library like LocoYAML.

## Contribution

LocoJSON is an open-source project! Bug reports and feature suggestions are welcome.
TOML is currently available at [LocoTOML](https://github.com/drago-suzuki58/LocoTOML).

## Update Info

<details>
<summary>Click to show update information</summary>

### v0.1.0

- Initial release

### v0.2.0

- Separating the core code for greater flexibility

</details>
