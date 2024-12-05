# Image2Text

Get descriptions of images using OpenAI's GPT models.

## Installation

```bash
pip install image2text-ai
```

## Usage
```bash
import image2text-ai

# Option 1: Set your OpenAI API key as an environment variable
import os
os.environ['OPENAI_API_KEY'] = 'your-api-key'

# Option 2: Provide your API key directly (not recommended for security reasons)
description = image2text-ai.get_description('https://example.com/image.jpg', api_key='your-api-key')

# Get a description of the image
description = image2text-ai.get_description('https://example.com/image.jpg')
print(description)
```

## Parameters

- image_url (str): The URL of the image.
- prompt (str, optional): The prompt for the description (default: "What's in this image?").
- model (str, optional): The OpenAI model to use (default: "gpt-4o").
- api_key (str, optional): Your OpenAI API key.