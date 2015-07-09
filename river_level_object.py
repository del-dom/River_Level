import BeautifulSoup as bs
import requests
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

url_RC = "http://water.weather.gov/ahps2/river.php?wfo=grr&wfoid=18702&riverid=203629&pt%5B%5D=144470&allpoints=144537%2C144470&data%5B%5D=obs"
url_GR = "http://water.weather.gov/ahps2/river.php?wfo=grr&wfoid=18702&riverid=204044&pt%5B%5D=143200&allpoints=141637%2C142381%2C142230%2C143200%2C143202%2C141240%2C144751%2C142883%2C142191%2C144291%2C143112%2C150294%2C142790&data%5B%5D=obs"
url_SY = "http://water.weather.gov/ahps2/river.php?wfo=grr&wfoid=18702&riverid=204503&pt%5B%5D=141848&allpoints=141848&data%5B%5D=obs"

class Rivers():
	def __init__(self,url):
		self.url=url
		self.req = requests.get(self.url)
		self.soup=bs.BeautifulSoup(self.req.content)
		self.most_recent = self.soup.findAll('div', {'class':'names_infos'},recursive=True,limit=2)
		self.measurements = ''
		for index in self.most_recent:
			for text in index:
				for a in text:
					self.measurements = self.measurements + a 
		self.date_time = str(self.measurements[0:11])
		self.depth_text = str(self.measurements[11:])
		self.depth_float = float(self.depth_text.rstrip(' ft'))

rc = Rivers(url_RC)
gr= Rivers(url_GR)
sy=Rivers(url_SY)


print 'red cedar' + rc.date_time,rc.depth_text
print 'grand river' +gr.date_time,gr.depth_text
print 'sycamore' + sy.date_time,sy.depth_text
