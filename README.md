# openargs-podcast-transcribe
Performing podcast transcription using Python &amp; MS Azure Cognitive Services

### Step 1: Run perform_transcription.py
1. Reads mp3 
2. Splits into 15 sec chunks 
3. For each chunk:
	- Converts chunk to wav 
	- Exports wav file to folder "audio files/raw"
4. For each wav file:
	- Sends for transcription to MS Azure Cognitive Services (using python library SpeechRecognition)
	- Saves result txt file in folder "audio files/transcribed"
5. Concatenate all transcribed txt files into file "master_transcription_raw.txt"
	- also, creates a copy of that file (initially is identical - to be manually edited) - "master_transcription_edited.txt"

### Step 2: Listen to episode and manually edit the file "master_transcription_edited.txt"
* Note: when this is rolled out to the OpenArgs wiki, this step can be crowdsourced?  To assess accuracy of speech transcription service, will do a diff of master_transcription_raw and master_transcription_edited
* accuracy pct = (total lines in raw - num lines edited) / (total lines in raw)