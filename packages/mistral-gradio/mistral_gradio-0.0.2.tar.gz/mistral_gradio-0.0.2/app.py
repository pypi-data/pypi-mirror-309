import gradio as gr
import mistral_gradio

gr.load(
    name='mistral-large-latest',
    src=mistral_gradio.registry,
).launch()