# -*- coding: utf-8 -*-
import config


def rate_for(code):
    if not config.RATES.has_key(code):
        raise KeyError("unknown service code: %s" % code)
    return config.RATES[code]


def is_exempt(code):
    return code in config.TAX_EXEMPT
