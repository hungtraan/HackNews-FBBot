import requests, json
from flask import url_for

def get_user_fb(token, user_id):
	r = requests.get("https://graph.facebook.com/v2.6/" + user_id,
					params={"fields": "first_name,last_name,profile_pic,locale,timezone,gender"
						,"access_token": token
					})
	if r.status_code != requests.codes.ok:
		print r.text
		return
	user = json.loads(r.content)
	return user

def show_typing(token, user_id, action='typing_on'):
	r = requests.post("https://graph.facebook.com/v2.6/me/messages",
						params={"access_token": token},
						data=json.dumps({
							"recipient": {"id": user_id},
							"sender_action": action
						}),
						headers={'Content-type': 'application/json'})
	if r.status_code != requests.codes.ok:
		print r.text

def send_message(token, user_id, text):
	"""Send the message text to recipient with id recipient.
	"""
	r = requests.post("https://graph.facebook.com/v2.6/me/messages",
						params={"access_token": token},
						data=json.dumps({
							"recipient": {"id": user_id},
							"message": {"text": text.decode('unicode_escape')}
						}),
						headers={'Content-type': 'application/json'})
	if r.status_code != requests.codes.ok:
		print r.text

def send_picture(token, user_id, imageUrl, title="", subtitle=""):
	if title != "":
		data = {"recipient": {"id": user_id},
					"message":{
						"attachment": {
							"type": "template",
							"payload": {
								"template_type": "generic",
								"elements": [{
									"title": title,
									"subtitle": subtitle,
									"image_url": imageUrl
								}]
							}
						}
					}
				}
	else:
		data = { "recipient": {"id": user_id},
				"message":{
					"attachment": {
						"type": "image",
						"payload": {
							"url": imageUrl
						}
					}
				}
			}
	r = requests.post("https://graph.facebook.com/v2.6/me/messages",
						params={"access_token": token},
						data=json.dumps(data),
						headers={'Content-type': 'application/json'})
	if r.status_code != requests.codes.ok:
		print r.text	

def send_quick_replies_yelp_search(token, user_id):
	# options = [Object {name:value, url:value}, Object {name:value, url:value}]
	quickRepliesOptions = [
		{"content_type":"text",
		 "title": "Get more suggestions",
		 "payload": 'yelp-more-yes'
		},
		{"content_type":"text",
		 "title": "That's good for me",
		 "payload": 'yelp-more-no'
		}
	]
	data = json.dumps({
			"recipient":{ "id": user_id },
			"message":{
				"text":"Do you want to find more results? :D",
				"quick_replies": quickRepliesOptions
				}
			})
	data = data.encode('utf-8')
	r = requests.post("https://graph.facebook.com/v2.6/me/messages",
		params={"access_token": token},
		data=data,
		headers={'Content-type':'application/json'})

	if r.status_code != requests.codes.ok:
		print r.text

def send_url(token, user_id, text, title, url):
	r = requests.post("https://graph.facebook.com/v2.6/me/messages",
						params={"access_token": token},
						data=json.dumps({
							"recipient": {"id": user_id},
							"message":{
								"attachment":{
									"type":"template",
									"payload":{
										"template_type":"button",
										"text": text,
										"buttons":[
											{
											"type":"web_url",
											"url": url,
											"title": title
											}
										]
									}
								}
							}
						}),
						headers={'Content-type': 'application/json'})
	if r.status_code != requests.codes.ok:
		print r.text

def send_intro_screenshots(app, token, user_id):
	print "Send intro screenshot"
	return

	chat_speak = {
		"title": 'You can both chat and speak to me',
		"image_url": url_for('static', filename="assets/img/intro/1-voice-and-text.jpg", _external=True),
		"subtitle": 'I understand voice and natural language (I try to be smarter everyday :D)'
	}
	location_text = {
		"title": "Find a restaurant/shop for you",
		"image_url": url_for('static', filename="assets/img/intro/2-yelp-gps-location.jpg", _external=True),
		"subtitle": "Tell me what you want, then your location name, address or GPS"
	}
	location_gps = {
		"title": "In case you've never sent location in Messenger",
		"image_url": url_for('static', filename="assets/img/intro/3-how-to-send-location.jpg", _external=True),
		"subtitle": "GPS will be the best option, but just a distinctive name would do",
	}
	location_save = {
		"title": "Save your favorite locations",
		"image_url": url_for('static', filename="assets/img/intro/4-save-location.jpg", _external=True),
		"subtitle": "Make it convenient for you"
	}
	memo1 = {
		"title": "Say \"Memorize\" or \"Memorize this for me\"",
		"image_url": url_for('static', filename="assets/img/intro/5-memo.jpg", _external=True),
		"subtitle": "Then your memo in the same/separate message"
	}
	news = {
		"title": "Keep you updated",
		"image_url": url_for('static', filename="assets/img/intro/6-news.jpg", _external=True),
		"subtitle": "With the most trending news"
	}

	options = [chat_speak, location_text, location_gps, location_save, memo1, news]

	r = requests.post("https://graph.facebook.com/v2.6/me/messages",
			params={"access_token": token},
			data=json.dumps({
				"recipient": {"id": user_id},
				"message":{
					"attachment":{
						"type":"template",
						"payload":{
							"template_type":"generic",
							"elements": options
						}
					}
				}
			}),
			headers={'Content-type': 'application/json'})
	if r.status_code != requests.codes.ok:
		print r.text


def send_story(token, user_id, story):
	send_url(token, user_id, 'Link', story['title'], story['url'])

def send_stories(token, user_id, posts):
	options = []
	for post in posts:
		img_url = post['image_url'] if 'image_url' in post and post['image_url'] != "" else url_for('static', filename='assets/img/empty-placeholder.jpg', _external=True)
		votes = post['score'] if 'score' in post else post['points']
		comments = post['descendants'] if 'descendants' in post else post['num_comments']
		datetime = post['datetime']
		obj = {
			"title": post['title'],
			"image_url": img_url,
			"subtitle": "%s\n%s votes, %s comments"%(datetime, votes, comments),
			"default_action": {
				"type": "web_url",
				"url": post['url'],
			},
			"buttons":[
				{
					"type":"web_url",
					"url": post['hn_url'],
					"title":"Comments"
				}
			]
		}
		options.append(obj) 
	read_more = {
			"title": "Load more stories",
			"image_url": url_for('static', filename='assets/img/empty-placeholder.jpg', _external=True),
			"subtitle": "",
			"default_action": {
				"type": "web_url",
				"url": "https://news.ycombinator.com/",
			},
			"buttons":[
				{
					"type":"web_url",
					"url": "https://news.ycombinator.com/",
					"title":"Load more"
				}
			]
		}
	options.append(read_more)
	print len(options)

	r = requests.post("https://graph.facebook.com/v2.6/me/messages",
						params={"access_token": token},
						data=json.dumps({
							"recipient": {"id": user_id},
							"message":{
								"attachment":{
									"type":"template",
									"payload":{
									   # "template_type": "list",
										# "top_element_style": "compact",
										"template_type":"generic",
										"elements": options
									}
								}
							}
						}),
						headers={'Content-type': 'application/json'})
	if r.status_code != requests.codes.ok:
		print r.text