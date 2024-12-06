# `mistral-gradio`

is a Python package that makes it very easy for developers to create machine learning apps that are powered by Mistral's API.

# Installation

You can install `mistral-gradio` directly using pip:

```bash
pip install mistral-gradio
```

That's it! 

# Basic Usage

Just like if you were to use the `mistralai` API, you should first save your Mistral API key to this environment variable:

```
export MISTRAL_API_KEY=<your token>
```

Then in a Python file, write:

```python
import gradio as gr
import mistral_gradio

gr.load(
    name='mistral-large-latest',
    src=mistral_gradio.registry,
).launch()
```

Run the Python file, and you should see a Gradio Interface connected to the model on Mistral!

![ChatInterface](chatinterface.png)

# Customization 

Once you can create a Gradio UI from an Mistral endpoint, you can customize it by setting your own input and output components, or any other arguments to `gr.Interface`. For example, the screenshot below was generated with:

```py
import gradio as gr
import mistral_gradio

gr.load(
    name='mistral-large-latest',
    src=mistral_gradio.registry,
    title='Mistral-Gradio Integration',
    description="Chat with Mistral's large model.",
    examples=["Explain quantum gravity to a 5-year old.", "How many R are there in the word Strawberry?"]
).launch()
```
![ChatInterface with customizations](mistral-gradio.png)

# Composition

Or use your loaded Interface within larger Gradio Web UIs, e.g.

```python
import gradio as gr
import mistral_gradio

with gr.Blocks() as demo:
    with gr.Tab("mistral-large"):
        gr.load('mistral-large-latest', src=mistral_gradio.registry)
    with gr.Tab("mistral-medium"):
        gr.load('mistral-medium-latest', src=mistral_gradio.registry)

demo.launch()
```

# Under the Hood

The `mistral-gradio` Python library has two dependencies: `mistralai` and `gradio`. It defines a "registry" function `mistral_gradio.registry`, which takes in a model name and returns a Gradio app.

# Supported Models in Mistral

All chat API models supported by Mistral are compatible with this integration. For a comprehensive list of available models and their specifications, please refer to the [Mistral Models documentation](https://docs.mistral.ai/models/).

-------

Note: if you are getting a 401 authentication error, then the Mistral API Client is not able to get the API token from the environment variable. This happened to me as well, in which case save it in your Python session, like this:

```python
import os

os.environ["MISTRAL_API_KEY"] = ...
```