from __future__ import absolute_import
import base64

def encode(str):
    return base64.b64encode(str)

def decode(str):
    return base64.b64decode(str)
