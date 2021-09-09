# Copyright (C) 2020-2021 by CandyGang@Github, < https://github.com/CandyGang >.
#
# This file is part of < https://github.com/CandyGang/Cynics > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/CandyGang/Cynics/blob/master/LICENSE >
#
# All rights reserved.

import re


def clear_string(msg: str):
    msg = re.sub(r"\<code\>(.*)\<\/code\>", "\g<1>", msg)
    msg = re.sub(r"\<i\>(.*)\<\/i\>", "\g<1>", msg)
    msg = re.sub(r"\<b\>(.*)\<\/b\>", "\g<1>", msg)
    msg = re.sub(r"\<u\>(.*)\<\/u\>", "\g<1>", msg)
    msg = re.sub(r"\*\*(.*)\*\*", "\g<1>", msg)
    msg = re.sub(r"\_\_(.*)\_\_", "\g<1>", msg)
    msg = re.sub(r"\`(.*)\`", "\g<1>", msg)
    return msg
