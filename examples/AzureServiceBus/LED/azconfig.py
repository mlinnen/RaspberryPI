import ConfigParser

class AzureConfig:
	def __init__(self):
		self.AZURE_SERVICEBUS_NAMESPACE = None
		self.AZURE_SERVICEBUS_ISSUER = None
		self.AZURE_SERVICEBUS_ACCESS_KEY = None
	def read(self):
		config = ConfigParser.ConfigParser()
		config.read("azconfig.ini")

		if not config.has_section("servicebus"):
			# Adds the section and options to the file since they are missing
			config.add_section("servicebus")
			config.set("servicebus","SERVICEBUS_NAMESPACE","yourNamespace")
			config.set("servicebus","SERVICEBUS_ISSUER","owner")
			config.set("servicebus","SERVICEBUS_ACCESS_KEY","yourKey")

		self.AZURE_SERVICEBUS_NAMESPACE=config.get("servicebus","SERVICEBUS_NAMESPACE")
		# Note: this user should have manage rights
		self.AZURE_SERVICEBUS_ISSUER=config.get("servicebus","SERVICEBUS_ISSUER")
		self.AZURE_SERVICEBUS_ACCESS_KEY=config.get("servicebus","SERVICEBUS_ACCESS_KEY")

		# Write out the configuration file
		with open('azconfig.ini', 'wb') as configfile:
			config.write(configfile)
