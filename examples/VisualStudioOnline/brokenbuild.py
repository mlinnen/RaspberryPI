# uncomment the following lines to enable visual studio remote debugging
#import ptvsd
#ptvsd.enable_attach(secret = 'vs2013')

import vsconfig
import json
import urllib2, base64
from datetime import datetime

def GetFailedUrl(account, project, dateTime):
	sdate = "{0}-{1}-{2}%20{3}:{4}:00".format(dateTime.year,dateTime.month,dateTime.day,dateTime.hour,dateTime.minute)
	return "https://" + account + ".visualstudio.com/DefaultCollection/_apis/build/builds?projectName=" + project + "&status=failed&minFinishTime=" + sdate

# Read connection configuration from file
config = vsconfig.VSOnlineConfig()
config.read()

api_url = "https://" + config.VS_ONLINE_ACCOUNT + ".visualstudio.com/DefaultCollection/_apis/"
builds_url = api_url + "build/builds"
projectBrokenBuilds_url = builds_url + "?projectName=" + config.VS_ONLINE_PROJECT + "&status=failed&minFinishTime=08-19-2014%2020:05:00"

qDateTime = datetime(2014,8,19)
# Setup the request
request = urllib2.Request(GetFailedUrl(config.VS_ONLINE_ACCOUNT,config.VS_ONLINE_PROJECT,qDateTime))

#Do Basic Authentication
base64string = base64.encodestring('%s:%s' % (config.VS_ONLINE_USER_NAME, config.VS_ONLINE_PASSWORD)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)   

# Get the response
result = urllib2.urlopen(request)

data = json.loads(result.read())
#with open('data.txt', 'w') as outfile:
#  json.dump(data, outfile)

count = data["count"]
if count==0:
	print "no broken builds found"
else:
	i = count - 1
	displayName = data["value"][i]["requests"][0]["requestedFor"]["displayName"]
	status = data["value"][i]["status"]
	buildNumber = data["value"][i]["buildNumber"]
	finishTime = data["value"][i]["finishTime"]
	
	print buildNumber + " completed at " + finishTime + " " + status + " by " + displayName

