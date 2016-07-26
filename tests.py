import requests
import json
from os.path import join

url = 'http://localhost:5000'
headers = {'Content-Type': 'application/json'}

def test_stats():
    """
    test that single operators and visitors can be posted with accurate numbers
    """
    v1 = {
      "id":"unique_id23451",
      "from":"visitor5",
      "type":"message",
      "site_id":"123",
      "data_message":"Hello",
      "timestamp":1429026445,
    }

    o1 = {
      "id":"unique_id26234",
      "from":"operator1",
      "site_id":"123",
      "type":"status",
      "data_status":"online",
      "timestamp":1429026448,
    }

    r = requests.post(join(url, 'events'), data=json.dumps(v1), headers=headers)
    assert r.ok

    r = requests.post(join(url, 'events'), data=json.dumps(o1), headers=headers)
    assert r.ok

    r = requests.get(join(url, 'stats.json'), headers=headers)
    assert r.ok
    stats = r.json()
    assert stats[0]['operators'] == 1
    assert stats[0]['messages'] == 0
    assert stats[0]['visitors'] == 1
    assert stats[0]['active'] == 1
    assert stats[0]['emails'] == 1

def test_stats_no_dupes():
    """
    test that sending messages with the same ids will not increase count in stats.json
    """
    v1 = {
      "id":"unique_id234521",
      "from":"visitor5",
      "type":"message",
      "site_id":"123",
      "data_message":"Hello",
      "timestamp":1429026445,
    }

    o1 = {
      "id":"unique_id216234",
      "from":"operator1",
      "site_id":"123",
      "type":"status",
      "data_status":"offline",
      "timestamp":1429026448,
    }

    r = requests.post(join(url, 'events'), data=json.dumps(v1), headers=headers)
    assert r.ok

    r = requests.post(join(url, 'events'), data=json.dumps(o1), headers=headers)
    assert r.ok

    r = requests.get(join(url, 'stats.json'), headers=headers)
    assert r.ok
    stats = r.json()
    assert stats[0]['operators'] == 1
    assert stats[0]['messages'] == 1
    assert stats[0]['visitors'] == 1
    assert stats[0]['active'] == 0
    assert stats[0]['emails'] == 1


def test_stats_counts():
    """
    test batch post and total counts
    """
    v1 = [
        {
          "id":"unique_id23345664521",
          "from":"visitor52",
          "type":"message",
          "site_id":"123",
          "data_message":"Hello",
          "timestamp":1429026445,
        },
        {
          "id":"unique_id234865521",
          "from":"visitor15",
          "type":"message",
          "site_id":"123",
          "data_message":"Hello",
          "timestamp":1429026445,
        }
    ]

    o1 = [
        {
          "id":"unique_id216231114",
          "from":"operator11",
          "site_id":"123",
          "type":"status",
          "data_status":"online",
          "timestamp":1429026448,
        },
        {
          "id":"unique_id2162311hhfg14",
          "from":"operator121",
          "site_id":"123",
          "type":"status",
          "data_status":"online",
          "timestamp":1429026448,
        },
    ]

    r = requests.post(join(url, 'events'), data=json.dumps(v1), headers=headers)
    assert r.ok

    r = requests.post(join(url, 'events'), data=json.dumps(o1), headers=headers)
    assert r.ok

    r = requests.get(join(url, 'stats.json'), headers=headers)
    assert r.ok
    stats = r.json()
    assert stats[0]['operators'] == 3
    assert stats[0]['messages'] == 1
    assert stats[0]['visitors'] == 3
    assert stats[0]['active'] == 2
    assert stats[0]['emails'] == 3


def test_cleanup():
    """
    delete events and sites
    """
    r = requests.delete(join(url, 'events'), headers=headers)
    assert r.ok
    r = requests.delete(join(url, 'sites'), headers=headers)
    assert r.ok
