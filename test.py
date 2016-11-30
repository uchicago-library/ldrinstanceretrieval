from ldrinstanceretriever.webretrieveritem import WebRetrieverItem

link = "https://y2.lib.uchicago.edu/processor/7p38vp9ts2n5z/74a96748972811e69cd9ac87a336bfd3/content"
arkid, objid = link.split("/content")[0].split("/processor/")[1].split("/")
w = WebRetrieverItem(arkid, objid)
print(w)

print(w.find_out_related_objects())
print(w.find_out_technical_metadata())
