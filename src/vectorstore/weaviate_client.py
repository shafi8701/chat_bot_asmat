import weaviate
import time

_CLIENTS = {}

def get_weaviate_client(url: str):
    if url in _CLIENTS:
        return _CLIENTS[url]

    for _ in range(10):
        try:
            client = weaviate.Client(url)
            if client.is_ready():
                _CLIENTS[url] = client
                return client
        except Exception:
            time.sleep(2)

    raise RuntimeError("Weaviate not ready")
