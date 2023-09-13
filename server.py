'''
-----------------------------------------------------------------------------
Copyright (c) 2023, ai-study-room. All rights reserved.

Authors: freesky-edward

This source code or documentation is under the license under the
LICENSE file in the root directory of this repository
-----------------------------------------------------------------------------
'''

import gradio as gr
import argparse
import os
from inference import *
from inference.config import *
from inference.get_inference import *


def chatbot(input):

    return input


def _init_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--server_name",
        type=str,
        default="127.0.0.1",
        help="The chatbot bind address")
    parser.add_argument(
        "--server_port",
        type=int,
        default="8089",
        help="The chatbot listen port")
    parser.add_argument(
        "--model_path",
        type=str,
        default="",
        help="The running model path which should contain the model and config.json")

    args = parser.parse_args()
    return args


def _startServer(server, server_address: str, server_port: str):

    server.queue().launch(server_name=server_address, server_port=server_port)


def _args_check(args):

    if args.model_path == "":
        raise ValueError


def chatbot(inp):

    return inp


def main():

    args = _init_args()
    _args_check(args)

    configfile = './models/llama2/config.yaml'
    cfg = Config(configfile)
    cfg.model_path = args.model_path
    inference = get_inference(cfg)

    server_address = os.getenv("SERVER_ADDRESS", "")
    server_port = os.getenv("SERVER_PORT")
    head = """
      This is a chat-engine
      Source: https://github.com/ai-study-room/chatengine
      Contact: freesky.edward@gmail.com

    """

    if args.server_name != "":
        server_address = args.server_name

    if args.server_port != 8090:
        server_port = args.server_port

    def clear_before_submit(inp, chatbot, chatbot2):
        generator = inference.generate(inp)
        try:
            bot_msg = next(generator)

            print(f'response msg "{bot_msg}"')
            chatbot.append((inp, bot_msg))
            chatbot2.append((inp, bot_msg))
            return inp, chatbot, chatbot2
        except StopIteration:
            chatbot.append((inp,"error occur"))
            chatbot2.append((inp,"error occur"))
            return inp,chatbot,chatbot2

    def display_result(inp):
        return ""

    with gr.Blocks() as bl:

        gr.Markdown(head)

        with gr.Group():
            with gr.Row():
                chatbot = gr.Chatbot(
                    label="chatbot", show_lable=True, container=True)
                chatbot2 = gr.Chatbot(label="chatbot2")
            with gr.Row():
                inp = gr.Textbox(placeholder="welcome to chat engine...")

        with gr.Row():
            submit_btn = gr.Button("Submit")
            clear_btn = gr.ClearButton([chatbot, chatbot2, inp])

        saved_input = gr.State()

        submit_btn.click(
            fn=clear_before_submit,
            inputs=[inp, chatbot, chatbot2],
            outputs=[inp, chatbot, chatbot2],
            api_name=False,
            queue=False,
        ).then(
            fn=display_result,
            inputs=inp,
            outputs=inp,
            api_name=False,
            queue=False,
        )

    _startServer(bl, server_address, server_port)


if __name__ == '__main__':
    main()
