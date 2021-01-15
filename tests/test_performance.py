import gzip
import json
import random

import pytest
from flask import Flask, request, jsonify
from flask_inflate import inflate

app = Flask(__name__)


@app.route('/naive', methods=["POST"])
def without_inflate():
    json_payload = gzip.decompress(request.get_data()).decode() if request.content_encoding == "gzip" else request.get_data(as_text=True)
    json.loads(json_payload)
    return jsonify("OK")


@app.route('/inflate', methods=["POST"])
@inflate
def with_inflate():
    # I could've used .get_json() or .json here but just to be explicit about the fact it's doing the same
    # as the naive route
    json_payload = request.get_data(as_text=True)
    json.loads(json_payload)
    return jsonify("OK")


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def generate_compressed_payload(n_keys):
    random_json = {
        "random_text{}".format(i): ' '.join(random.choice(["some", "repeating", "words"]) for _ in range(150))
        for i in range(n_keys)
    }

    raw_json = json.dumps(random_json).encode("utf-8")
    return gzip.compress(raw_json)


@pytest.fixture
def gzipped_payload():
    yield generate_compressed_payload(1000)


@pytest.mark.benchmark(
    disable_gc=True,
)
def test_inflate(gzipped_payload, client, benchmark):
    result = benchmark.pedantic(send_request, args=(client, gzipped_payload), kwargs={"naive": False, "compressed": True}, iterations=100, rounds=10, warmup_rounds=10)
    assert result == "OK"


@pytest.mark.benchmark(
    disable_gc=True,
)
def test_naive(gzipped_payload, client, benchmark):
    result = benchmark.pedantic(send_request, args=(client, gzipped_payload), kwargs={"naive": True, "compressed": True}, iterations=100, rounds=10, warmup_rounds=10)
    assert result == "OK"


def send_request(_client, payload, naive=False, compressed=True):
    headers = {"Content-Type": "application/json"}
    if compressed:
        headers["Content-Encoding"] = "gzip"

    path = 'naive' if naive else 'inflate'
    return _client.post('http://localhost:5000/{}'.format(path), data=payload, headers=headers).json


if __name__ == '__main__':
    import cProfile

    with app.test_client() as client:
        payload = generate_compressed_payload(1000)

        send_request(client, payload, True, True) # warmup
        send_request(client, payload, False, True) # warmup
        cProfile.run('send_request(client, payload, True, True)', sort='cumtime')
        cProfile.run('send_request(client, payload, False, True)', sort='cumtime')
