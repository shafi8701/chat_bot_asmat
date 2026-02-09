import weaviate
from weaviate.connect import ConnectionParams

_client = None
_current_url = None

def get_weaviate_client(url: str):
    global _client, _current_url

    # Reuse client if same URL
    if _client is not None and _current_url == url:
        return _client

    # Close old client if URL changed
    if _client is not None:
        _client.close()

    _client = weaviate.WeaviateClient(
        connection_params=ConnectionParams.from_url(
            url=url,
            grpc_port=50051,
        )
    )
    _client.connect()
    _current_url = url

    return _client


def close_weaviate_client():
    global _client, _current_url
    if _client is not None:
        _client.close()
        _client = None
        _current_url = None
