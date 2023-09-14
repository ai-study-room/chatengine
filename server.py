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
from typing import Iterator


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

    server.queue()
    server.launch(server_name=server_address, server_port=server_port)


def _args_check(args):

    if args.model_path == "":
        raise ValueError


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

    def reply(
            chatbot, chatbot2) -> (Iterator[list[tuple[str, str]]], Iterator[list[tuple[str, str]]]):
        # inp = chatbot[-1][0]
        streamer = inference.generate(chatbot)
        try:
            bot_msg = next(streamer)

            chatbot[-1][1] = "" + bot_msg
            chatbot2[-1][1] = "" + bot_msg
            yield chatbot, chatbot2

            for resp in streamer:
                chatbot[-1][1] = resp
                chatbot2[-1][1] = resp
                yield chatbot, chatbot2

        except StopIteration as si:
            print(si)
            chatbot.append((inp, "error occur1"))
            chatbot2.append((inp, "error occur1"))
            yield chatbot, chatbot1

    def input_msg(inp, history_1, history_2):

        return "", history_1 + [(inp, None)], history_2 + [(inp, None)]

    with gr.Blocks() as bl:

        gr.Markdown(head)

        with gr.Group():
            with gr.Row():
                chatbot = gr.Chatbot(
                    label="Llama-2", show_label=True, container=True)
                chatbot2 = gr.Chatbot(label="Llama-2")
            with gr.Row():
                inp = gr.Textbox(
                    placeholder="welcome to chat engine...",
                    show_label=False)

        with gr.Row():
            submit_btn = gr.Button("Submit")
            clear_btn = gr.ClearButton([chatbot, chatbot2, inp])

        saved_input = gr.State()

        button_event_preprocess = (
            submit_btn.click(
                fn=input_msg,
                inputs=[inp, chatbot, chatbot2],
                outputs=[inp, chatbot, chatbot2],
                api_name=False,
                queue=False,
            ).then(
                fn=reply,
                inputs=[chatbot, chatbot2],
                outputs=[chatbot, chatbot2],
                api_name=False,
            )
        )

        inp.submit(
            fn=input_msg,
            inputs=[inp, chatbot, chatbot2],
            outputs=[inp, chatbot, chatbot2],
            api_name=False,
            queue=False,
        ).then(
            fn=reply,
            inputs=[chatbot, chatbot2],
            outputs=[chatbot, chatbot2],
            api_name=False,
        )

    _startServer(bl, server_address, server_port)


if __name__ == '__main__':
    main()
