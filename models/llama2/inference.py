'''
-----------------------------------------------------------------------------
Copyright (c) 2023, ai-study-room. All rights reserved.

Authors: freesky-edward

This source code or documentation is under the license under the
LICENSE file in the root directory of this repository
-----------------------------------------------------------------------------
'''
from threading import Thread
from inference.base import BaseInference
import torch
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from transformers import TextIteratorStreamer
from typing import Iterator


class Inference(BaseInference):
    r"""

    The llama Inference is a inference for llama models.


    Args:
        cfg(Config): the configuration load from the config.yaml

    """

    def __init__(self, cfg):
        super().__init__(cfg)

        device_map = "auto"
        if cfg.device_map != "":
            device_map = cfg.device_map

        self.model = Inference.create_model(
            cfg.model_path, device_map, cfg.torch_dtype, cfg.load_in_8bit)

        self.tokenizer = Inference.create_tokenizer(cfg.model_path)

    @classmethod
    def create_model(cls, model_path, device_map, torch_dtype, load_in_8bit):
        r'''
        return the huggingface model via transformer lib

        Args:
            model_path(str): can be either the model id on huggingface website
                or the local system path. which default value can be update in
                config.yaml
            device_map(str): the GPU device id, "auto" for default value.
            torch_dtype(torch.dtype): the value of float type. the value canbe
                be torch.float16, torch.float32, torch.float8, currently, only
                torch.float16 fixed value set.
            load_in_8bit(bool): the float8 weights will be loaded if true.

        '''
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype=torch.float16,
            load_in_8bit=load_in_8bit,
        )
        return model

    @classmethod
    def create_tokenizer(cls, model_path):
        r'''
        retrun the tokenizer via transformer lib

        Args:
            model_path(str):can be either the model id on huggingface website
                or the local system path. which default value can be update in
                config.yaml

        '''

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        return tokenizer

    def generate(self, context: list[tuple[str, str]],
                 kwargs=None) -> Iterator[str]:
        r'''
        inherited from BaseInference which generate the result
        according to the msg(prompt)

        Args:
            msg(str): the prompt as the model input.
        '''

        max_new_tokens = self.cfg.max_new_token
        if max_new_tokens == 0:
            max_new_tokens = 1024

        history = context[0:len(context) - 1]
        prompt = context[-1][0]
        msg = self.compo_prompt(prompt, history)

        print(f"prompt='{prompt}'; instruction='{msg}'")

        inp = self.tokenizer([msg], return_tensors="pt").to("cuda")

        streamer = TextIteratorStreamer(
            self.tokenizer,
            timeout=10.0,
            skip_prompt=True,
            skip_special_tokens=True,
        )

        kwargs = dict(
            inp,
            streamer=streamer,
            max_new_tokens=max_new_tokens,
            temperature=self.cfg.temperature,
            top_p=self.cfg.top_p,
            top_k=self.cfg.top_k,
        )

        thread = Thread(target=self.model.generate, kwargs=kwargs)
        thread.start()

        outs = []
        for text in streamer:
            outs.append(text)
            yield "".join(outs)

    def compo_prompt(self, msg: str, msg_history: list[tuple[str, str]] = [
    ], system_prompt: str = ""):
        r'''
        Combine the chat history to generate the llama prompt.

        Args:
            msg(str): the chat message to generate text
            msg_history(List): a tuple list contains the chat hisotry.


        '''
        texts = [f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n"]
        for req, rep in msg_history:
            texts.append(
                f"{req.strip()} [/INST] {rep.strip()} </s><s> [INST] ")
        texts.append(f"{msg.strip()} [/INST]")
        return "".join(texts)
