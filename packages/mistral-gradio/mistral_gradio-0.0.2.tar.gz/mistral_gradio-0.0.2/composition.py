import gradio as gr
import mistral_gradio

with gr.Blocks() as demo:
    with gr.Tab("mistral-large-latest"):
        gr.load('mistral-large-latest', src=mistral_gradio.registry)
    with gr.Tab("ministral-3b-latest"):
        gr.load('ministral-3b-latest', src=mistral_gradio.registry)

demo.launch()