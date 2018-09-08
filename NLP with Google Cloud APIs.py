# to use Google cloud API service, need to create an API key
API_Key ="AIzaSyB4NLTI4SkOuQQikzzVTw8OzU"

# install googleapiclient with:
# pip install --upgrade google-api-python-client

# if you want to send the image or audio data as base64-encoded text for google analyzing
# import base64

from googleapiclient.discovery import build


#--------------Translation

t_service = build('translate', 'v2', developerKey=API_Key)
translate_input = input('Type in English to translate to Chinese --> ')
t_input = []
t_input.append(translate_input)
#en=English, zh=Chinese
outputs = t_service.translations().list(source='en', target='zh', q=t_input).execute()
for the_input, output in zip(t_input, outputs['translations']):
	print(f"\n{the_input}\n->\n{output['translatedText']}\n")


#--------------Image detection

IMAGE = input('Extract text from an image and translate into English. Enter an image URL--> ')
v_service = build('vision', 'v1', developerKey=API_Key)
request = v_service.images().annotate(body={
	'requests': [{
		'image': {
			'source': {
				'imageUri':IMAGE
			}
		},
		'features': [{
			'type': 'TEXT_DETECTION',
			# 'type': 'LABEL_DETECTION',
			'maxResults':3,
		}]
	}],
})
responses = request.execute()

foreign_text = responses['responses'][0]['textAnnotations'][0]['description']
language_code = responses['responses'][0]['textAnnotations'][0]['locale']

print(f'Language code --> {language_code},\n\n Content:\n\n{foreign_text}')


#--------------translate sign
if language_code != 'en':
    t_service = build('translate', 'v2', developerKey=API_Key)
    t_input = []
    t_input.append(foreign_text)
    outputs = t_service.translations().list(source=language_code, target='en', q=t_input).execute() 
    for the_input, output in zip(t_input, outputs['translations']):
    	print(f'Translation:\n{output["translatedText"]}\n\n')


#--------------Sentiment analysis

l_service = build('language', 'v1', developerKey=API_Key)
senti_input = input(
	'To analyse sentiment in sentences. Type them into here --> ')
s_input = []
s_input.append(senti_input)

for a_s_input in s_input:
	responses = l_service.documents().analyzeSentiment(
		body={
			'document': {
				'type': 'PLAIN_TEXT',
				'content': a_s_input
			}
		}
	).execute()
	sentiment = responses['documentSentiment']['score']
	language_code = responses['language']
	# print(responses)
		
	if sentiment > 0.75:
		sentiment_score = 'Very Positive'
	elif sentiment > 0.5:
		sentiment_score = 'Pretty Positive'
	elif sentiment > 0.25:
		sentiment_score = 'Quite Positive'
	elif sentiment > 0.1:
		sentiment_score = 'Fairly Positive'
	elif sentiment > -0.1:
		sentiment_score = 'Neutral'
	elif sentiment > -0.25:
		sentiment_score = 'Fairly Negative'
	elif sentiment > -0.5:
		sentiment_score = 'Quite Negative'
	elif sentiment > -0.75:
		sentiment_score = 'Pretty Negative'
	else:
		sentiment_score = 'Very Negative'
	print(f'\n\nAnalyzing following sentences\n{s_input}')
	print(f'Language code --> {language_code}')
	print(
		f'Sentiment score: {sentiment} <-- (-1~+1), therefore sentiment of the input is {sentiment_score}\n')


#--------------Speech dictation

s_service = build('speech', 'v1', developerKey=API_Key)
responses = s_service.speech().recognize(
	body={
		'config': {
			'encoding': 'FLAC',
			'sampleRateHertz': 16000,
			"languageCode": "en-US"
		},
		'audio': {
			'uri': 'gs://cloud-samples-tests/speech/brooklyn.flac'
		}
	}
).execute()
# print(responses)

transcript = responses['results'][0]['alternatives'][0]['transcript']
print(f'Transcript of the audio --> {transcript}')
confidence = responses['results'][0]['alternatives'][0]['confidence']
print(f'Confidence of being correct --> {confidence}')
