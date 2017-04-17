from datetime import datetime
import caldav
from caldav.elements import dav, cdav

# Caldav url
#url = "https://user:pass@hostname/caldav.php/"
class Takvim:
	url = "http://kamu:kamu3333@" + "192.168.1.100/bulut/remote.php/caldav/calendars/kamu"  
	'''vcal = """BEGIN:VCALENDAR
	VERSION:2.0
	PRODID:-//Example Corp.//CalDAV Client//EN
	BEGIN:VEVENT
	UID:1234567890
	DTSTAMP:20150116T182145Z
	DTSTART:20150116T170000Z
	DTEND:20150116T180000Z
	SUMMARY:pythonla eklenen bir eventtir.
	END:VEVENT
	END:VCALENDAR
	"""
	'''
	vcal = """BEGIN:VCALENDAR
	BEGIN:VEVENT
	CREATED;VALUE=DATE-TIME:20141130T073450Z
	UID:12345aaa99
	LAST-MODIFIED;VALUE=DATE-TIME:20141130T073450Z
	DTSTAMP;VALUE=DATE-TIME:20141130T073450Z
	SUMMARY:BATI LASTIK 4250
	DTSTART;VALUE=DATE:20150121
	DTEND;VALUE=DATE:20150122
	CLASS:PUBLIC
	END:VEVENT
	END:VCALENDAR
	"""
	
	def olay_ekle(self,tarih,bilgi):
		client = caldav.DAVClient(url)
		principal = client.principal()
		calendars = principal.calendars()
		if len(calendars) > 0:
		    calendar = calendars[0]
		    print "Using calendar", calendar
		    event = calendar.add_event(vcal)
		    print "Event", event, "created"

	def olay_ara(self,tarihbas,tarihson):
		client = caldav.DAVClient(url)
		principal = client.principal()
		calendars = principal.calendars()
		if len(calendars) > 0:
		    calendar = calendars[0]	
		    print "Looking for events in 2015-01"
		    results = calendar.date_search(
		        datetime(2015, 1, 1), datetime(2015, 1, 1))
		    for event in results:
		        print "Found", event
