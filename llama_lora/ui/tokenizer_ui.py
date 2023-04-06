import gradio as gr
import time
import json

from ..globals import Global
from ..models import get_tokenizer


def handle_decode(encoded_tokens_json):
    try:
        encoded_tokens = json.loads(encoded_tokens_json)
        if Global.ui_dev_mode:
            return f"Not actually decoding tokens in UI dev mode.", gr.Markdown.update("", visible=False)
        tokenizer = get_tokenizer()
        decoded_tokens = tokenizer.decode(encoded_tokens)
        return decoded_tokens, gr.Markdown.update("", visible=False)
    except Exception as e:
        return "", gr.Markdown.update("Error: " + str(e), visible=True)


def handle_encode(decoded_tokens):
    try:
        if Global.ui_dev_mode:
            return f"[\"Not actually encoding tokens in UI dev mode.\"]", gr.Markdown.update("", visible=False)
        tokenizer = get_tokenizer()
        result = tokenizer(decoded_tokens)
        encoded_tokens_json = json.dumps(result['input_ids'], indent=2)
        return encoded_tokens_json, gr.Markdown.update("", visible=False)
    except Exception as e:
        return "", gr.Markdown.update("Error: " + str(e), visible=True)


def tokenizer_ui():
    with gr.Blocks() as tokenizer_ui_blocks:
        with gr.Row():
            with gr.Column():
                encoded_tokens = gr.Code(
                    label="Encoded Tokens (JSON)",
                    language="json",
                    value=sample_encoded_tokens_value,
                    elem_id="tokenizer_encoded_tokens_input_textbox")
                decode_btn = gr.Button("Decode ➡️")
                encoded_tokens_error_message = gr.Markdown(
                    "", visible=False, elem_classes="error-message")
            with gr.Column():
                decoded_tokens = gr.Code(
                    label="Decoded Tokens",
                    value=sample_decoded_text_value,
                    elem_id="tokenizer_decoded_text_input_textbox")
                encode_btn = gr.Button("⬅️ Encode")
                decoded_tokens_error_message = gr.Markdown(
                    "", visible=False, elem_classes="error-message")
            stop_btn = gr.Button("Stop")

            decoding = decode_btn.click(
                fn=handle_decode,
                inputs=[encoded_tokens],
                outputs=[decoded_tokens, encoded_tokens_error_message],
            )
            encoding = encode_btn.click(
                fn=handle_encode,
                inputs=[decoded_tokens],
                outputs=[encoded_tokens, decoded_tokens_error_message],
            )
            stop_btn.click(fn=None, inputs=None, outputs=None, cancels=[decoding, encoding])

    tokenizer_ui_blocks.load(_js="""
    function tokenizer_ui_blocks_js() {
    }
    """)


sample_encoded_tokens_value = """
[
  15043,
  3186,
  29889
]
"""

sample_decoded_text_value = """
"""
