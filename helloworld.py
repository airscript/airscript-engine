import os
from flask import Flask
app = Flask(__name__)

import lupa

@app.route("/")
def hello():
    lua = lupa.LuaRuntime()
    return str(lua.eval("return \"Hello, World!\""))

if __name__ == "__main__":
    app.run('0.0.0.0', int(os.environ.get("PORT", 5000)))
