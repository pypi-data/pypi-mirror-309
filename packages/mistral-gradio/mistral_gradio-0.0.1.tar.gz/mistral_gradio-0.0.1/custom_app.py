import gradio as gr
import mistral_gradio

gr.load(
    name='mistral-large-latest',
    src=mistral_gradio.registry,
    title='Mistral-Gradio Integration',
    description="Chat with mistral-large-latest model.",
    examples=["Explain quantum gravity to a 5-year old.", "How many R are there in the word Strawberry?"]
).launch()