#!/usr/bin/env python
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient
import urllib2
from datetime import datetime

account_sid = '*********'
auth_token = '**********'

############################## BeautifulSoup ##############################
URL = 'http://www.meetup.com/ny-tech/'
hdr = {'User-Agent': 'Chrome/33.0'}  # Not a bot
req = urllib2.Request(URL, headers=hdr)  # Not a bot
html = urllib2.urlopen(req)  # Not a bot
soup = BeautifulSoup(html)

if soup.find('a', {'class': 'omnCamp omnrv_rv13'}):

	###Find link from NY Tech meetup and create new soup
	recent_link = str(soup.find('a', {'class': 'omnCamp omnrv_rv13'})['href'])
	req = urllib2.Request(recent_link, headers=hdr)
	html = urllib2.urlopen(req)
	soup = BeautifulSoup(html)

	###Find ticket release information in new soup
	body_text = soup.find('div', {'id': 'event-description-wrap'}).text
	start_length = body_text.find('The three ticket releases for this Meetup are:')
	text_length = len('The three ticket releases for this Meetup are:')
	start = start_length+text_length+1
	end_date_1 = body_text.find(',', start)
	end_date_2 = body_text.find(',', end_date_1+1)
	end_date_3 = body_text.find(' at', end_date_2+1)

	#Grab dates
	date_1 = body_text[start:end_date_1] #'April 4'
	date_2 = body_text[end_date_1+2:end_date_2]
	date_3 = body_text[end_date_2+6:end_date_3]

	#Turn dates into numbers for comparison
	month_dictionary = {'January': '01',
						'February': '02',
						'March': '03',
						'April': '04',
						'May': '05',
						'June': '06',
						'July': '07',
						'August': '08',
						'September': '09',
						'October': '10',
						'November': '11',
						'December': '12'}
	date_1_space = date_1.find(' ')
	date_1_month = date_1[:date_1_space]
	date_1_day = date_1[date_1_space+1:]
	date_2_space = date_2.find(' ')
	date_2_month = date_2[:date_2_space]
	date_2_day = date_2[date_2_space+1:]
	date_3_space = date_3.find(' ')
	date_3_month = date_3[:date_3_space]
	date_3_day = date_3[date_3_space+1:]

		#Dictionary month - from 'April' to '04'
	date_1_month = month_dictionary[date_1_month]
	date_2_month = month_dictionary[date_2_month]
	date_3_month = month_dictionary[date_3_month]
		#Day - from 3 to 03
	if len(date_1_day) == 1:
		date_1_day = '0'+date_1_day
	else:
		date_1_day = date_1_day
	if len(date_2_day) == 1:
		date_2_day = '0'+date_2_day
	else:
		date_2_day = date_2_day
	if len(date_3_day) == 1:
		date_3_day = '0'+date_3_day
	else:
		date_3_day = date_3_day

	ticket_releases = [[date_1_month, date_1_day], [date_2_month, date_2_day], [date_3_month, date_3_day]]

	#Check current date
	current_date = str(datetime.now())
	current_month = current_date[5:7] #'04'
	current_day = current_date[8:10] #'03'
	current_time = current_date[11:16] #'14:54'
	current_hour = current_time[:2]

	#If date is within 30 minutes (or less) AND not on google calendar send text reminder
	for ticket_release in ticket_releases:
		if ticket_release[0] == current_month:
			if ticket_release[1] == current_day:
				if current_hour == '12': #Only checking once per hour
					body_text = "Reminder that NY Tech Meetup ticket release is occuring today @1pm"
					client = TwilioRestClient(account_sid, auth_token)
					message = client.messages.create(to="+1*******", from_="+1*******", body=body_text)

############################## Twilio ##############################
#client = TwilioRestClient(account_sid, auth_token)
#message = client.messages.create(to="+15167327149", from_="+16313507401", body=body_text)

############################## Email ##############################

############################## Google calendar ##############################
