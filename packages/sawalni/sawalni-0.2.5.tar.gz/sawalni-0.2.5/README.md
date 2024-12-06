# Sawalni Python SDK

This is the official Python SDK for the Sawalni API, providing easy access to language-related services such as embedding generation, language identification, and translation. Sawalni API is developed by [Omneity Labs](https://sawalni.com/developers), and provides unique multilingual models and NLP capabilities, including pioneering Moroccan Darija support.

## Installation

Install the package using pip:

```bash
pip install sawalni
```

## Quick Start

To use the Sawalni SDK, you'll need an API key. You can set it as an environment variable or pass it directly to the client:

```py
from sawalni import Sawalni

client = Sawalni(api_key='your_api_key_here') 
# or specify the key via SAWALNI_API_KEY in the environment
```

## Features

The SDK supports both synchronous and asynchronous operations for the following services:

1. **Chat**: Generate chat completions using our `Sawalni` multilingual models, supporting Moroccan Darija, English, French, Arabic and many other languages.
2. **Search**: Perform internet searches in multiple languages with a single query.
3. **Generate Embeddings**: Create embeddings for text in multiple languages using `Madmon`.
4. **Identify Language**: Detect the language of a given text with `Gherbal`, supporting up to 33 languages.
5. **Translate Text**: Translate text between 13 supported languages with `Tarjamli`.
6. **Transliterate Text**: Convert Moroccan Arabic script to Moroccan Latin script with `Daktilo`.

The Sawalni SDK includes an OpenAI compatible client, which can be accessed via the `chat` and `embeddings` properties, or direct use via the OpenAI client as detailed below.

### Chat

```py
# Available models: sawalni-micro, sawalni-mini, sawalni-small
chat = client.chat.completions.create(messages=[{"role": "user", "content": "Hello, how are you?"}], model="sawalni-small")

# Stream
stream = client.chat.completions.create(messages=[{"role": "user", "content": "Hello, how are you?"}], model="sawalni-small", stream=True)
for chunk in stream:
    print(chunk.choices[0].delta.content)
```

### Search

```py
search = client.search("Hello, how are you?")
```

### Generate Embeddings

```py
embeddings = client.embed("Hello, world!")
```

### Identify Language

```py
language = client.identify("Bonjour le monde")
```

### Translate Text

```py
# You can specify a source language or let the model detect it automatically
translation = client.translate("Hello", source="auto", target="ary_Latn")
```

### Transliterate Text

```py
transliteration = client.transliterate("اهلا بيك", model="daktilo-mini", to="latn", temperature=0.1)

# {"text": "ahlane bik"}
```

## Asynchronous Usage

For asynchronous operations, use the SawalniAsync client:

```py
from sawalni import SawalniAsync

async_client = SawalniAsync(api_key='your_api_key_here')
embeddings = await async_client.embed("Hello, world!")
```

## OpenAI compatible client

The SDK also includes an OpenAI compatible client, which can be accessed via the `chat` and `embeddings` properties:

```py
chat = client.chat
embeddings = client.embeddings
```

You can also use the OpenAI client directly with the base URL set to `https://api.sawalni.com/v1` and the API key set to your Sawalni API key.

```py
import openai
client = openai.OpenAI(base_url="https://api.sawalni.com/v1", api_key="your_api_key_here")
```

Only the `chat` and `embeddings` properties are supported with this approach.

## Documentation

For detailed information about available models, parameters, languages and and response formats, please refer to the complete API documentation at https://api.sawalni.com.

## Support

If you encounter any issues or have questions, please contact api@sawalni.com.