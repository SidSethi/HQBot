# NOTES / REFERENCE:
	# - run it on android in bg, listening for screenshots
	# - OPTI wrap req in try-catch
	# - OPTI get links for each of top 10 results and also count occurences in those
	# 	- remember link you found which gives you algo to get all links on google res page?
	# - account for NOT questions
	# look at rahul optis
	# emulators
		# https://www.macworld.co.uk/how-to/iosapps/how-run-iphone-ipad-apps-games-on-mac-3512222/
		# https://drfone.wondershare.com/emulator/iphone-emulator.html
	# TEMPLATE
		# https://medium.com/@tobymellor/hq-trivia-using-bots-to-win-money-from-online-game-shows-ce2a1b11828b

try:
	import Image
except ImportError:
	from PIL import Image
import pytesseract						# https://pypi.python.org/pypi/pytesseract
import pyscreenshot as ImageGrab		# https://pypi.python.org/pypi/pyscreenshot
import requests
import time

# GLOBAL VARS
image_path = 'hq-trivia-screenshot.jpg'
search_uri = 'https://www.google.com/search'
api_uri = 'https://www.googleapis.com/customsearch/v1'

def main():
	
	image = getImage()
	text = str(pytesseract.image_to_string(image))
	
	lines = text.splitlines()

	screenshot_text = parseScreenshotText(lines)
	if (not screenshot_text):
		return

	question = screenshot_text['question']
	
	response_html = googleSearch(question)

	selectBestAnswer(response_html.lower(), screenshot_text['option1'].lower(), screenshot_text['option2'].lower(), screenshot_text['option3'].lower())
	return


def parseScreenshotText(lines):
	
	dataset1 = {
		'question': 'Which religion is the King of Thailand required to be by law?',
		'option1': 'Buddhist',
		'option2': 'Hindu',
		'option3': 'Muslim',
	}	# correct
	dataset2 = {
		'question': 'Which NBA player is known as "The Greek Freak"?',
		'option1': 'Lebron James',
		'option2': 'Stephen Curry',
		'option3': 'Giannis Antetokounmpo',
	}	# correct
	dataset3 = {
		'question': 'What was the most downloaded iPhone app of 2016',
		'option1': 'Snapchat',
		'option2': 'Messenger',
		'option3': 'Pokemon Go',
	}	# correct
	dataset4 = {
		'question': 'What are the Bildungsroman genre of stories about?',
		'option1': 'Roman empire',
		'option2': 'Coming of age',
		'option3': 'Unrequited love',
	} 	# FAILED
	dataset5 = {
		'question': 'Canon, Nikon, and Olympus all specialize in what products?',
		'option1': 'Can openers',
		'option2': 'Cameras',
		'option3': 'Candelabras',
	}	# correct
	# return dataset5

	lines = list(filter(bool, lines))
	num_lines = len(lines)
	
	option3 = lines[num_lines-1]
	option2 = lines[num_lines-2]
	option1 = lines[num_lines-3]

	if (not option3 or not option2 or not option1):
		print 'ERROR - Failed to detect all 3 options'
		return False

	question = ''
	for i in range(num_lines-3):
		question += lines[i] + ' '
	question = question.strip()

	if (not question):
		print 'ERROR - Failed to detect question'
		return False
	
	return {'question': question, 'option1': option1, 'option2': option2, 'option3': option3}


# investigate why dataset4 returned answer Roman empire
def selectBestAnswer(response_html, option1, option2, option3):

	count = -1
	answer = 'None'

	count1 = response_html.count(option1)
	if count1 > count:
		count = count1
		answer = option1
	
	count2 = response_html.count(option2)
	if count2 > count:
		count = count2
		answer = option2

	count3 = response_html.count(option3)
	if count3 > count:
		count = count3
		answer = option3

	# print answer
	print '[' + option1 + ': ' + str(count1) + ', ' + option2 + ': ' + str(count2) + ', ' + option3 + ': ' + str(count3) + ']'
	print 'ANSWER: ' + answer


def getImage():
	# return Image.open(image_path)

	# X1,Y1,X2,Y2
	coords=(120,200,480-120,530-200)
	im = ImageGrab.grab(bbox=coords)
	# im.show()
	return im


# REFERENCE
		# https://developers.google.com/custom-search/json-api/v1/using_rest
		# https://developers.google.com/custom-search/json-api/v1/reference/cse/list#response
		# https://stackoverflow.com/a/11206266/8414360
		# http://scriptsonscripts.blogspot.com/2015/02/python-google-search-api-requests.html
		# https://cse.google.com/cse/all
def googleSearch(question):
	
	# return requests.get(search_uri, params={'q': question}).text
	
	params = {
		'key': 'AIzaSyCfunU8i-QFBlKxi0PhVYpXjRmeVZPhXhU',
		'cx': '000945734874065329160:y9l8zmwkpds',
		'q': question,
	}

	# OPTI: use 'fields' param to only get partial response
	# OPTI: prettyPrint = false

	response = requests.get(api_uri, params=params).text
	print response.url
	return response
	# print r.content


start = time.time()
main()
print str(time.time() - start) + ' sec'

