
import gradio as gr
from gradio_sandboxcomponent import SandboxComponent


example = SandboxComponent().example_value()

with gr.Blocks() as demo:
    with gr.Tab("Example"):
        with gr.Row():
            gr.Markdown("## Example")
        with gr.Row():
            SandboxComponent(
                label="Example",
                value=("https://www.baidu.com/", "Hello World"),
                show_label=True
            )


if __name__ == "__main__":
    demo.launch()
