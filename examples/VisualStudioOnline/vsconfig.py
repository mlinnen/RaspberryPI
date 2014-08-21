import ConfigParser

class VSOnlineConfig:
	def __init__(self):
		self.VS_ONLINE_ACCOUNT = None
		self.VS_ONLINE_USER_NAME = None
		self.VS_ONLINE_PASSWORD = None
		self.VS_ONLINE_PROJECT = None
	def read(self):
		config = ConfigParser.ConfigParser()
		config.read("vsconfig.ini")

		if not config.has_section("vsonline"):
			# Adds the section and options to the file since they are missing
			config.add_section("vsonline")
			config.set("vsonline","VSONLINE_ACCOUNT","yourAccount")
			config.set("vsonline","VSONLINE_USERNAME","username")
			config.set("vsonline","VSONLINE_PASSWORD","password")
			config.set("vsonline","VSONLINE_PROJECT","project")
			config.set("vsonline","VSONLINE_DEFINITION","buildDefinition")

		self.VS_ONLINE_ACCOUNT=config.get("vsonline","VSONLINE_ACCOUNT")
		self.VS_ONLINE_USER_NAME=config.get("vsonline","VSONLINE_USERNAME")
		self.VS_ONLINE_PASSWORD=config.get("vsonline","VSONLINE_PASSWORD")
		self.VS_ONLINE_PROJECT=config.get("vsonline","VSONLINE_PROJECT")
		self.VS_ONLINE_DEFINITION=config.get("vsonline","VSONLINE_DEFINITION")

		# Write out the configuration file
		with open('vsconfig.ini', 'wb') as configfile:
			config.write(configfile)
