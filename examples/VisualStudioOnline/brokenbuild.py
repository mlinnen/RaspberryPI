#
# This python script runs on a raspberry pi and requests Visual Studio Online build status for the given
#	account and project.
# Run the script one time and edit the vsconfig.ini file with the following:
#	account
#	project
#	username
#	password
# The Visual Studio Online user account must have the alternate credentials enabled. This allows
# the script to use basic authentication to make the REST api call.


import vsconfig
import os, json, urllib2, base64, ConfigParser, time
from datetime import datetime

def GetFailedUrl(account, project,definition, dateTime):
	sdate = "{0}-{1}-{2}%20{3}:{4}:00".format(dateTime.year,dateTime.month,dateTime.day,dateTime.hour,dateTime.minute)
	return "https://" + account.replace(" ","%20") + ".visualstudio.com/DefaultCollection/_apis/build/builds?projectName=" + \
				project.replace(" ","%20") + "&definition=" + definition.replace(" ","%20") + "&status=failed&minFinishTime=" + sdate

def Say(message):
	# Use Google Translate Text To Speech
	tts_text = message.replace(" ","+")
	tts_url = "'http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q="+tts_text + "'"
	cmd_line = "wget -q -U Mozilla -O texttospeech.mp3 " + tts_url 
	os.system(cmd_line)
	os.system("mplayer texttospeech.mp3")

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

def GetLatestBrokenBuildData(dateTime):
	# Setup the request
	request = urllib2.Request(GetFailedUrl(config.VS_ONLINE_ACCOUNT,config.VS_ONLINE_PROJECT,config.VS_ONLINE_DEFINITION,qDateTime))

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

	# get the datetime the last time we queried the broken build status
	qDateTime = GetLastDateTime()

	# look for any new broken builds
	data = GetLatestBrokenBuildData(qDateTime)

	count = data["count"]
	if count==0:
		print "no broken builds found"
	else:
		print count
		i = 0
		row = data["value"][i]
		displayName = row["requests"][0]["requestedFor"]["displayName"]
		status = row["status"]
		buildNumber = row["buildNumber"]
		finishTime = row["finishTime"]
		definition = row["definition"]
		
		print buildNumber + " completed at " + finishTime + " " + status + " by " + displayName

		message = "I blame " + displayName + " for breaking the build called " + config.VS_ONLINE_DEFINITION
		Say(message)

	time.sleep(30)

	# timestamp
	dateTimeNow = datetime.utcnow()

	# save the timestamp so that we know how to query the next time
	SaveLastDateTime(dateTimeNow)

