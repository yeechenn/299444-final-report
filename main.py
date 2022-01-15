from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import pandas as pd


es_ip = "http://127.0.0.1:9200"
es = Elasticsearch(es_ip)
res = es.get(index="winlogbeat", id="IM3k130BMs_nTerjgcWJ")
print(res['_source'])

query_str = {"size": 0,"aggregations": {"result": { "terms": {"field": "host.name.keyword","order": [{"_count": "desc"}]}}}}
res = es.search(index="winlogbeat", body=query_str)
result = res["aggregations"]["result"]["buckets"]

event_pd = pd.DataFrame(result, columns=["key", "doc_count"], index = ["DESKTOP-T3V8EOP","LAPTOP-O5NUGDHI","DESKTOP-PKB0K93","DESKTOP-K9J5624","DESKTOP-QLB0CEN"])
print(event_pd)
ax = event_pd.plot(x="key", y="doc_count", kind="bar",figsize=(8,4))

for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
plt.xlabel("host.name")
plt.ylabel("Log Counts")
plt.xticks(rotation=0)
plt.tick_params(axis='x', labelsize=8)
plt.legend()

plt.show()