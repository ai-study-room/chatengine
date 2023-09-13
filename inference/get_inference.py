'''
-----------------------------------------------------------------------------
Copyright (c) 2023, ai-study-room. All rights reserved.

Authors: freesky-edward

This source code or documentation is under the license under the
LICENSE file in the root directory of this repository
-----------------------------------------------------------------------------
'''

import importlib


def get_inference(cfg):
    r"""
    load the give inference base on the configuration.

    the default inferences locats under models directory
    and each model will:

    1). inhirted from BaseInference
    2). provide a config file under its own root directory.


    """

    inference_lib = importlib.import_module(cfg.inference.type)
    inference = inference_lib.Inference(cfg)

    return inference
