#!/usr/bin/python
import wolframalpha
import sys
#Get a free API key here http://products.wolframalpha.com/api/
#Put you App ID here
app_id=''

client = wolframalpha.Client(app_id)

query = ' '.join(sys.argv[1:])
res = client.query(query)

if len(res.pods) > 0:
    texts = ""
    pod = res.pods[1]
    if pod.text:
        texts = pod.text
    else:
        texts = "I have no answer for that"
    print texts
else:
    print "I am not sure"