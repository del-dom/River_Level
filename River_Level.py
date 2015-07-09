import BeautifulSoup as bs
import requests
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



url_RC = "http://water.weather.gov/ahps2/river.php?wfo=grr&wfoid=18702&riverid=203629&pt%5B%5D=144470&allpoints=144537%2C144470&data%5B%5D=obs"

rc = requests.get(url_RC)
rc_soup = bs.BeautifulSoup(rc.content)
rc_most_recent = rc_soup.findAll('div', {'class':'names_infos'},recursive=True,limit=2)
rc_Measurements =''
for index in rc_most_recent:
	for text in index:
		for a in text:
			rc_Measurements = rc_Measurements + a 
rc_date_time = str(rc_Measurements[0:11])
rc_depth_text = str(rc_Measurements[11:])
rc_depth_float = float(rc_depth_text.rstrip(' ft'))

url_GR = "http://water.weather.gov/ahps2/river.php?wfo=grr&wfoid=18702&riverid=204044&pt%5B%5D=143200&allpoints=141637%2C142381%2C142230%2C143200%2C143202%2C141240%2C144751%2C142883%2C142191%2C144291%2C143112%2C150294%2C142790&data%5B%5D=obs"
gr = requests.get(url_GR)
gr_soup = bs.BeautifulSoup(gr.content)
gr_most_recent = gr_soup.findAll('div', {'class':'names_infos'},recursive=True,limit=2)
gr_Measurements =''
for index in gr_most_recent:
	for text in index:
		for a in text:
			gr_Measurements = gr_Measurements + a 		
gr_date_time = str(gr_Measurements[0:11])
gr_depth_text = str(gr_Measurements[11:])
gr_depth_float = float(gr_depth_text.rstrip(' ft'))

url_SC = "http://water.weather.gov/ahps2/river.php?wfo=grr&wfoid=18702&riverid=204503&pt%5B%5D=141848&allpoints=141848&data%5B%5D=obs"
SC = requests.get(url_SC)
SC_soup = bs.BeautifulSoup(SC.content)
SC_most_recent = SC_soup.findAll('div', {'class':'names_infos'},recursive=True,limit=2)
SC_Measurements =''
for index in SC_most_recent:
	for text in index:
		for a in text:
			SC_Measurements = SC_Measurements + a 
		
SC_date_time = str(SC_Measurements[0:11])
SC_depth_text = str(SC_Measurements[11:])
SC_depth_float = float(SC_depth_text.rstrip(' ft'))

'''Red cedar text'''
if rc_depth_float > 4:
	if rc_depth_float > 4.5:
		kal_under = 'Flooded'
	else:
		kal_under = 'Partially Flooded'
else: 
	kal_under = 'Clear'

if rc_depth_float > 5:
	if rc_depth_float > 5.5:
		RC_Rail_under = 'Flooded'
		Zoo = 'Flooded'
	else:
		RC_Rail_under = 'Partially Flooded'
		Zoo = 'Partially Flooded'
else: 
	RC_Rail_under = 'Clear'
	Zoo = 'Clear'
if rc_depth_float > 5.75:
	if rc_depth_float > 6.25:
		rc_lowareas = 'Flooded'
	else:
		rc_lowareas = 'Partially Flooded'
else:
	rc_lowareas = 'Clear'

'''grand river text'''

if gr_depth_float > 7:
	if gr_depth_float > 7.5:
		gr_rail_under = 'Flooded'
	else: gr_rail_under = 'Partially Flooded'
else:
	gr_rail_under = 'Clear'

if gr_depth_float > 8.5:
	if gr_depth_float > 9:
		sag_under = 'Flooded'
	else: sag_under = 'Partially Flooded'
else:
	sag_under = 'Clear'

if gr_depth_float > 10:
	if gr_depth_float > 10.5:
		gr_lowareas = 'Flooded'
	else: gr_lowareas = 'Partially Flooded'
else:
	gr_lowareas = 'Clear'

'''Sycamore Text'''

if SC_depth_float > 3.5:
	if SC_depth_float > 4:
		I_under = 'Flooded'
	else:
		I_under = 'Partially Flooded'
else:
	I_under = 'Clear'

'''Emailer'''

addresses = ['!!!!!!!!!', '###########','$$$$$$$']


if rc_depth_float > 4 or gr_depth_float > 7: 
	msg = MIMEMultipart('alternative')
	FROM = 'RedCedarFlood@gmail.com'
	msg['From'] = 'RedCedarFlood@gmail.com'
	msg['SUBJECT'] = "FloodAlert" + ' ' + time.strftime("%d/%m/%Y") + ' ' + time.strftime("%I:%M")
	TEXT = """<html><head></head><body><h3>Flood prediction accuracy may be effected by distance from the gauge.</h3><h2>Red Cedar Locations:</h2><h4> Measurements taken at Farm Lane on MSU campus.</h4><table><tr><th>Location</th><th>Flooded</th><th>Floods At</th><th>Current</th></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.729283&lon=-84.506378" id="various3">Kalamazoo St Underpass</a></td><td>"""+kal_under+"""</td><td>4 ft</td><td>"""+rc_depth_text+"""</td></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.722711&lon=-84.516352" id="various4">Railroad Underpass (between Clippert & Aurelius)</a></td><td>"""+RC_Rail_under+"""</td><td>5 ft</td><td>"""+rc_depth_text+"""</td></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.716246&lon=-84.524855" id="various5">Potter Park near Aurelius</a></td><td>"""+Zoo+"""</td><td>5 ft</td><td>"""+rc_depth_text+"""</td></tr><tr><td>Most Lower Areas</td><td>"""+rc_lowareas+"""</td><td>5.75 ft</td><td>"""+rc_depth_text+"""</td></tr></table><h2>Grand River Locations:</h2><h4> Measurements taken at N Grand River Ave</h4><table><tr><th>Location</th><th>Flooded</th><th>Floods At</th><th>Current</th></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.719010&lon=-84.554509" id="various6">Railroad Underpass by Island Ave</a></td><td>"""+gr_rail_under+"""</td><td>7 ft</td><td>"""+gr_depth_text+"""</td></tr><tr><td><a  href="http://lansingrivertrail.org/map-1.php?lat=42.740819&lon=-84.548959" id="various7">Saginaw Underpass</a></td><td>"""+sag_under+"""</td><td>8.5 ft</td><td>"""+gr_depth_text+"""</td></tr><tr><td>Most Lower Areas</td><td>"""+gr_lowareas+"""</td><td>10 ft</td><td>"""+gr_depth_text+"""</td></tr></table><h2>Sycamore Creek Locations:</h2><h4> Measurements taken at Holt Rd</h4><table><tr><th>Location</th><th>Flooded</th><th>Floods At</th><th>Current</th></tr><tr><td><a href="http://lansingrivertrail.org/map-1.php?lat=42.668133&lon=-84.511688" id="various8">I-96 Underpass</a></td><td>"""+I_under+"""</td><td>3.5 ft</td><td>"""+SC_depth_text+"""</td></tr></table></body></html>"""
	mimetext = MIMEText(TEXT, 'html')
	msg.attach(mimetext)
	username = 'RedCedarFlood@gmail.com'
	password = '##########'
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

	print 'E-mail sent'
else:
	print 'No flooding'

