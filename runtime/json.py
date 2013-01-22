from __future__ import absolute_import
import json

import lupa

class LuaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, lupa._lupa._LuaTable):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)

def parse(str):
    return json.loads(str)

def stringify(obj):
    return json.dumps(obj, cls=LuaEncoder)
