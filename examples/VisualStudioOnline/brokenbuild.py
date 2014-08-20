# uncomment the following lines to enable visual studio remote debugging
#import ptvsd
#ptvsd.enable_attach(secret = 'vs2013')

import vsconfig
import json, urllib2, base64, ConfigParser, time
from datetime import datetime

def GetFailedUrl(account, project, dateTime):
	sdate = "{0}-{1}-{2}%20{3}:{4}:00".format(dateTime.year,dateTime.month,dateTime.day,dateTime.hour,dateTime.minute)
	return "https://" + account + ".visualstudio.com/DefaultCollection/_apis/build/builds?projectName=" + project + "&status=failed&minFinishTime=" + sdate

def GetLastDateTime():
	config = ConfigParser.ConfigParser()
	config.read("data.ini")

	if config.has_section("last"):
		return datetime.strptime(config.get("last","datetime"),"%Y-%m-%d %H:%M:%S.%f")

	return datetime.now()

def SaveLastDateTime(dateTime):
	config = ConfigParser.ConfigParser()
	config.read("data.ini")

	if not config.has_section("last"):
		# Adds the section and options to the file since they are missing
		config.add_section("last")

	config.set("last","datetime",dateTime.isoformat(' '))

	# Write out the configuration file
	with open('data.ini', 'wb') as configfile:
		config.write(configfile)
	return

def GetLastBuildData(dateTime):
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
	return data


# Read connection configuration from file
config = vsconfig.VSOnlineConfig()
config.read()

while True:
	qDateTime = GetLastDateTime()

	data = GetLastBuildData(qDateTime)

	dateTimeNow = datetime.utcnow()

	SaveLastDateTime(dateTimeNow)

	count = data["count"]
	if count==0:
		print "no broken builds found"
	else:
		print count
		i = 0
		displayName = data["value"][i]["requests"][0]["requestedFor"]["displayName"]
		status = data["value"][i]["status"]
		buildNumber = data["value"][i]["buildNumber"]
		finishTime = data["value"][i]["finishTime"]
		
		print buildNumber + " completed at " + finishTime + " " + status + " by " + displayName

	time.sleep(30)