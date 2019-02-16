# Flask-Inflate
A simple flask extension to automatically decompress gzipped (compressed) request data sent by clients.
This doesn't read the whole data into memory, it just allows reading from the original data stream as it was never compressed.

If the content is not gzipped, it will remain intact.

## Install
`pip install flask-inflate`

## How to use
If you want to enable it for all requests, application wide:
```python
from flask import Flask
from flask_inflate import Inflate

app = Flask(__name__)
Inflate(app) 
# or 
inf = Inflate()
inf.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'
```

If you want to enable decompressing only for certain views:
```python

from flask import Flask
from flask_inflate import inflate

app = Flask(__name__)

@app.route('/a')
@inflate
def possibly_gzipped_content_function():
    return 'I can deal with both gzipped and regular content!'
    
@app.route('/a')
def regular_function():
    return 'I can deal only with non gzipped content!'
```

Feature requests, issues and PRs are welcome!