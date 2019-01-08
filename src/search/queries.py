import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

def es_result_to_list(res: dict):
    res_list = []
    for r in res["hits"]["hits"]:
        res_list.append(r["_source"])
    
    return res_list

def get_feed(offset: int = 0, limit: int = 10):
    body = {"query": {"match_all": {}},
            "sort": [
                {"unixtime": "desc" }
            ],
            "from" : offset,
            "size" : limit
            }
    res = es.search(index="news", body=body)
    return es_result_to_list(res)
