import os
import base64
from mistralai import Mistral
import gradio as gr
from typing import Callable
from urllib.parse import urlparse

__version__ = "0.0.1"


def encode_image_file(image_path):
    """Encode an image file to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return None


def process_image(image):
    """Process image input to the format expected by Mistral API."""
    if isinstance(image, str):
        # Check if it's a URL or base64 string
        if image.startswith('data:'):
            return image  # Already in base64 format
        elif urlparse(image).scheme in ('http', 'https'):
            return image  # It's a URL
        else:
            # Assume it's a local file path
            encoded = encode_image_file(image)
            return f"data:image/jpeg;base64,{encoded}" if encoded else None
    return None


def get_fn(model_name: str, preprocess: Callable, postprocess: Callable, api_key: str):
    def fn(message, history):
        inputs = preprocess(message, history)
        client = Mistral(api_key=api_key)
        try:
            # Create the streaming chat completion
            stream_response = client.chat.stream(
                model=model_name,
                messages=inputs["messages"]
            )
            
            response_text = ""
            for chunk in stream_response:
                if chunk.data.choices[0].delta.content is not None:
                    delta = chunk.data.choices[0].delta.content
                    response_text += delta
                    yield postprocess(response_text)
                
        except Exception as e:
            print(f"Error during chat completion: {str(e)}")
            yield "Sorry, there was an error processing your request."

    return fn


def get_interface_args(pipeline):
    if pipeline == "chat":
        inputs = None
        outputs = None

        def preprocess(message, history):
            messages = []
            # Process history
            for user_msg, assistant_msg in history:
                if isinstance(user_msg, dict):
                    # Handle multimodal history messages
                    content = []
                    if user_msg.get("text"):
                        content.append({"type": "text", "text": user_msg["text"]})
                    for file in user_msg.get("files", []):
                        processed_image = process_image(file)
                        if processed_image:
                            content.append({"type": "image_url", "image_url": processed_image})
                    messages.append({"role": "user", "content": content})
                else:
                    # Handle text-only history messages
                    messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})
            
            # Process current message
            if isinstance(message, dict):
                # Handle multimodal input
                content = []
                if message.get("text"):
                    content.append({"type": "text", "text": message["text"]})
                for file in message.get("files", []):
                    processed_image = process_image(file)
                    if processed_image:
                        content.append({"type": "image_url", "image_url": processed_image})
                messages.append({"role": "user", "content": content})
            else:
                # Handle text-only input
                messages.append({"role": "user", "content": message})
            
            return {"messages": messages}

        postprocess = lambda x: x  # No post-processing needed
    else:
        raise ValueError(f"Unsupported pipeline type: {pipeline}")
    return inputs, outputs, preprocess, postprocess


def get_pipeline(model_name):
    # Determine the pipeline type based on the model name
    # For simplicity, assuming all models are chat models at the moment
    return "chat"


def registry(name: str, token: str | None = None, **kwargs):
    """
    Create a Gradio Interface for a model on Mistral AI.

    Parameters:
        - name (str): The name of the Mistral AI model.
        - token (str, optional): The API key for Mistral AI.
    """
    api_key = token or os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is not set.")

    pipeline = get_pipeline(name)
    inputs, outputs, preprocess, postprocess = get_interface_args(pipeline)
    fn = get_fn(name, preprocess, postprocess, api_key)

    if pipeline == "chat":
        # Always enable multimodal support
        interface = gr.ChatInterface(
            fn=fn,
            multimodal=True,
            **kwargs
        )
    else:
        # For other pipelines, create a standard Interface (not implemented yet)
        interface = gr.Interface(fn=fn, inputs=inputs, outputs=outputs, **kwargs)

    return interface
