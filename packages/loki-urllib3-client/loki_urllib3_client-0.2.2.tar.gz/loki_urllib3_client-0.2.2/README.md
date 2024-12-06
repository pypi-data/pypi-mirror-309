# loki-urllib3-client

A simple Python Loki client using urllib3

This is a modified version of [loki-client](https://github.com/hack-han/loki-client)

# Quickstart

## Install : 
```bash
pip3 install loki-urllib3-client
```

## Usage
```python
from loki_urllib3_client import LokiClient

loki_url = 'http://localhost:3100'
loki_client = LokiClient(url=loki_url)

# test ready()
loki_ready = loki_client.ready()
if not loki_ready:
    print('Loki is not ready.')
    exit(1)

# test labels()
result = loki_client.labels()
print(result)

# test post()
label_dic = {'host': 'windows', 'env': 'test'}
logs_lst = ['This is line 1', 'This is line 2', 'This is line 3', 'This is line 4']
result = loki_client.post(label_dic, logs_lst)
if not result[0]:
    print(result[1])

# test query_range()
query = r'{host="ubuntu"}|~"error"'
result = loki_client.query_range(query, direction=LokiClient.Direction.backward, limit=10)
print(result)

if result[0]:
    print(result[1]['status'])
    print(result[1]['data']['resultType'])

# test query()
result = loki_client.query(query, direction=LokiClient.Direction.backward, limit=10)
print(result)
```
