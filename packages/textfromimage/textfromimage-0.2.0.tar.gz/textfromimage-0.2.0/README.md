# TextFromImage

Get descriptions of images using OpenAI's GPT models on easy way.

## Installation
You can install the textfromimage package via PyPI using pip:
```bash
pip install textfromimage
```

## Usage
The textfromimage package is now class-based, allowing you to initialize the TextFromImage class with your desired configurations and use its methods to obtain image descriptions.
```bash
from textfromimage import TextFromImage

# Option 1: Set your OpenAI API key as an environment variable
import os
os.environ['OPENAI_API_KEY'] = 'your-api-key'

# Initialize the TextFromImage class
text_from_image = TextFromImage()

# Get a description of the image
image_url = 'https://example.com/image.jpg'
description = text_from_image.get_description(image_url)
print(description)
```
**Specifying a Different Model**

You can specify a different OpenAI model if needed. By default, the model is set to "gpt-4o".
```bash
from textfromimage import TextFromImage

# Initialize with a specific model
text_from_image = TextFromImage(model='gpt-4o-mini')

# Get a description of the image
image_url = 'https://example.com/image.jpg'
description = text_from_image.get_description(image_url)
print(description)
```

## Parameters

- image_url (str): The URL of the image.
- prompt (str, optional): The prompt for the description (default: "What's in this image?").
- model (str, optional): The OpenAI model to use (default: "gpt-4o").
- api_key (str, optional): Your OpenAI API key.


## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/YourFeature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.