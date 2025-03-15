import os
import assemblyai as aai
from dotenv import load_dotenv

# load
load_dotenv()

# Replace with your API key
aai.settings.api_key = os.getenv('AAI_API_KEY')

# URL of the file to transcribe
FILE_URL = "/home/catalin/workspace/ITFest2025/Server/src/temp/a9ae59d8fc1834b5.mp4"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

def transcript(url: str):
	print(f'{url}')
	transcriber = aai.Transcriber()

	transcript = transcriber.transcribe(url)

	if transcript.status == aai.TranscriptStatus.error:
		print(transcript.error)
	else:
		print(transcript.text)

transcript(FILE_URL)