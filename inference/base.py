'''
-----------------------------------------------------------------------------
Copyright (c) 2023, ai-study-room. All rights reserved.

Authors: freesky-edward

This source code or documentation is under the license under the
LICENSE file in the root directory of this repository
-----------------------------------------------------------------------------
'''


class BaseInference(object):
    r"""
    BaseInference is the abstract class that all model inherit this
    to predict or generate the new text or image.

    Args:
        cfg(obj): The configuration of the inference. see Config object in config.py

    """

    def __init__(self, cfg):

        super().__init__()
        self.cfg = cfg

    def generate(self, msg: list[tuple[str, str]], kwargs):
        r'''
        Provide the basic interface that return the generative text by a given model

        Args:
            msg(str): The prompt under a context dialog.


        '''

        pass
