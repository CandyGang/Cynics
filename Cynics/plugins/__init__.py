# Copyright (C) 2020-2021 by CandyGang@Github, < https://github.com/CandyGang >.
#
# This file is part of < https://github.com/CandyGang/Cynics > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/CandyGang/Cynics/blob/master/LICENSE >
#
# All rights reserved.

from Cynics import LOGGER


def __list_all_plugins():
    from os.path import dirname, basename, isfile
    import glob

    # This generates a list of plugins in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_plugins = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return all_plugins


ALL_PLUGINS = sorted(__list_all_plugins())
__all__ = ALL_PLUGINS + ["ALL_PLUGINS"]
