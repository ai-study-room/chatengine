'''
-----------------------------------------------------------------------------
Copyright (c) 2023, ai-study-room. All rights reserved.

Authors: freesky-edward

This source code or documentation is under the license under the
LICENSE file in the root directory of this repository
-----------------------------------------------------------------------------
'''

import os
import yaml
import collections


class Attr(dict):

    def __init__(self, *args, **kwargs):
        super(Attr, self).__init__(*args, **kwargs)
        self.__dict__ = self
        for key, value in self.__dict__.items():
            if isinstance(value, dict):
                self.__dict__[key] = Attr(value)
            elif isinstance(value, (list, tuple)):
                if value and isinstance(value[0], dict):
                    self.__dict__[key] = [Attr(item) for item in value]
                else:
                    self.__dict__[key] = value


class Config(Attr):
    r'''
    Config represents a configuration of a model,
    which will provide the predict parameters, e.g.
    model_path, torch_dtpe, top_p,top_n,temperature...

    Every model can customize its own parameters.which
    can define in a yaml file or other format will be
    supported later.

    Args:
        filename(str): the configuration file path

    '''

    def __init__(self, filename=None):
        super(Config, self).__init__()
        self.file = filename

        cfg_dict = self.load_config(filename)
        recursive_update(self, cfg_dict)

    def load_config(self, filename: str):
        r'''
        load the parameters from the given file.
        return the configuration dict with Attr object.
        '''

        if not os.path.exists(filename):
            raise Exception(f'File "{filename}" not exist')

        try:
            with open(filename) as f:
                cfg_dict = yaml.load(f, Loader=yaml.SafeLoader)
                cfg_dict = Attr(cfg_dict)
                return cfg_dict
        except EnvironmentError:
            print(f'The config file "{filename}" parse error ')


def recursive_update(d, u):
    r'''
    recurse to update all the values.

    '''

    for key, value in u.items():
        if isinstance(value, collections.abc.Mapping):
            d.__dict__[key] = recursive_update(d.get(key, Attr({})), value)
        elif isinstance(value, (list, tuple)):
            if value and isinstance(value[0], dict):
                d.__dict__[key] = [Attr(item) for item in value]
            else:
                d.__dict__[key] = value
        else:
            d.__dict__[key] = value
    return d
