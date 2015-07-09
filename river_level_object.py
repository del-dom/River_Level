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

	def floodCheck(self,partFlood,fullFlood):
		flooded = ''
		if self.depth_float > partFlood:
			if self.depth_float > fullFlood:
				flooded = 'Flooded'
			else: flooded = 'Partially Flooded'
		else:
			flooded = 'Clear'
		return flooded


rc = Rivers(url_RC)

rc.kal_under = rc.floodCheck(4,4.5)
rc.rail_under = rc.floodCheck(5,5.5)
rc.zoo = rc.floodCheck(5,5.5)
rc.low_areas = rc.floodCheck(5.75,6.25)

gr= Rivers(url_GR)

gr.rail_under = gr.floodCheck(7,7.5)
gr.sag_under = gr.floodCheck(8.5,9)
gr.low_areas = gr.floodCheck(10,10.5)

sy= Rivers(url_SY)

sy.I_under = sy.floodCheck(3.5,4)

addresses = ['##########']

def send_emails():
	msg = MIMEMultipart('alternative')
	FROM = 'RedCedarFlood@gmail.com'
	msg['From'] = 'RedCedarFlood@gmail.com'
	msg['SUBJECT'] = "FloodAlert" + ' ' + time.strftime("%d/%m/%Y") + ' ' + time.strftime("%I:%M")
	TEXT = """<html><head></head><body><h3>Flood prediction accuracy may be effected by distance from the gauge.</h3><h2>Red Cedar Locations:</h2><h4> Measurements taken at Farm Lane on MSU campus.</h4><table><tr><th>Location</th><th>Flooded</th><th>Floods At</th><th>Current</th></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.729283&lon=-84.506378" id="various3">Kalamazoo St Underpass</a></td><td>"""+rc.kal_under+"""</td><td>4 ft</td><td>"""+rc.depth_text+"""</td></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.722711&lon=-84.516352" id="various4">Railroad Underpass (between Clippert & Aurelius)</a></td><td>"""+rc.rail_under+"""</td><td>5 ft</td><td>"""+rc.depth_text+"""</td></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.716246&lon=-84.524855" id="various5">Potter Park near Aurelius</a></td><td>"""+rc.zoo+"""</td><td>5 ft</td><td>"""+rc.depth_text+"""</td></tr><tr><td>Most Lower Areas</td><td>"""+rc.low_areas+"""</td><td>5.75 ft</td><td>"""+rc.depth_text+"""</td></tr></table><h2>Grand River Locations:</h2><h4> Measurements taken at N Grand River Ave</h4><table><tr><th>Location</th><th>Flooded</th><th>Floods At</th><th>Current</th></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.719010&lon=-84.554509" id="various6">Railroad Underpass by Island Ave</a></td><td>"""+gr.rail_under+"""</td><td>7 ft</td><td>"""+gr.depth_text+"""</td></tr><tr><td><a  href="http://lansingrivertrail.org/map-1.php?lat=42.740819&lon=-84.548959" id="various7">Saginaw Underpass</a></td><td>"""+gr.sag_under+"""</td><td>8.5 ft</td><td>"""+gr.depth_text+"""</td></tr><tr><td>Most Lower Areas</td><td>"""+gr.low_areas+"""</td><td>10 ft</td><td>"""+gr.depth_text+"""</td></tr></table><h2>Sycamore Creek Locations:</h2><h4> Measurements taken at Holt Rd</h4><table><tr><th>Location</th><th>Flooded</th><th>Floods At</th><th>Current</th></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.668133&lon=-84.511688" id="various8">I-96 Underpass</a></td><td>"""+sy.I_under+"""</td><td>3.5 ft</td><td>"""+sy.depth_text+"""</td></tr></table></body></html>"""
	mimetext = MIMEText(TEXT, 'html')
	msg.attach(mimetext)
	username = 'RedCedarFlood@gmail.com'
	password = '######'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)

	for i in range(len(addresses)):
		#print len(addresses)
		#print addresses[i]
		TO = addresses[i]
		msg['To'] = addresses[i]
		server.sendmail(FROM, TO, msg.as_string())
	server.quit()


if rc.depth_float > 4 or gr.depth_float > 7:
	send_emails()
	print 'E-mail sent'
else:
	print 'No flooding'


'''
print 'red cedar' + rc.date_time,rc.depth_text, rc.kal_under,rc.rail_under,rc.zoo,rc.low_areas
print 'grand river' + gr.rail_under,gr.sag_under,gr.low_areas
print 'sycamore' + sy.I_under
print 'grand river' +gr.date_time,gr.depth_text
print 'sycamore' + sy.date_time,sy.depth_text'''
