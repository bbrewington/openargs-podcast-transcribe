# Part 1 of 4: Define function transcribe_wav_file: function that actually calls the transcription API
# https://realpython.com/python-speech-recognition/#using-record-to-capture-data-from-a-file
    import speech_recognition as sr

    def transcribe_wav_file(input_filepath, azure_key_filepath):
        r = sr.Recognizer()
        tempfile = sr.AudioFile(input_filepath)
        with tempfile as source:
            audio = r.record(source)

        # recognize speech using Microsoft Azure Speech
        # had to install development version of speech_recognition from github b/c regognize_azure not currently published to PyPI
        #   sudo pip3 install --upgrade https://github.com/Uberi/speech_recognition/tarball/master

        f = open(azure_key_filepath, "r")
        AZURE_SPEECH_KEY = f.read() # Microsoft Speech API keys 32-character lowercase hexadecimal strings
        f.close()
        
        try:
            print('Successful Call (waiting on response)')
            return r.recognize_azure(audio, location='eastus', key=AZURE_SPEECH_KEY)
        except sr.UnknownValueError:
            print('ERROR')
            return 'ERROR: Microsoft Azure Speech could not understand audio'
        except sr.RequestError as e:
            print('ERROR')
            return 'ERROR: Could not request results from Microsoft Azure Speech service; {0}'.format(e)

# # Test the transcribe_wav_file function on a single chunk
# test1 = transcribe_wav_file('audio files/Open Args episode 302 first 15 min - chunk021.wav')
# f = open("test1.txt","w+")
# f.write(test1)
# f.close()
# print(test1)

# Part 2 of 4: Create chunks from mp3, and iterate over them - creating wav file...
#               then sending it to transcription API and write result to text file
    from os import path
    from pydub import AudioSegment
    from pydub.utils import make_chunks

    # file paths
    # src = 'Thomas and Andrew near end.mp3'
    src1 = 'audio files/'
    src2 = 'Open Args episode 302 first 15 min'
    src3 = '.mp3'

    # read mp3
    sound = AudioSegment.from_mp3(src1 + src2 + src3)
    total_duration = sound.duration_seconds
    print('Total Duration : ', total_duration)

    # https://stackoverflow.com/questions/36799902/how-to-splice-an-audio-file-wav-format-into-1-sec-splices-in-python
    chunk_length_ms = 1000 * 15 # pydub calculates in millisec
    chunks = make_chunks(sound, chunk_length_ms) #Make chunks

# Part 4 of 4: Export all of the individual chunks as wav files
    for i, chunk in enumerate(chunks):
        chunk_filename = src2 + ' - chunk{0}.wav'.format(str(i).zfill(3))
            # Open Args episode 302 first 15 min - chunk000.wav
        chunk_full_path = 'audio files/raw/' + chunk_filename
            # audio files/raw/Open Args episode 302 first 15 min - chunk000.wav
        print('Exporting :', chunk_filename)
        chunk.export(chunk_full_path, format="wav")
        print('Transcribing :', chunk_filename)
        transcription_result = transcribe_wav_file(chunk_full_path, '../api_azure_key.txt')
        f = open('audio files/transcribed/' + chunk_filename.replace('wav','txt'), 'w+')
        f.write(transcription_result)
        f.close()

# Part 3 of 4: Concatenate transcription into Master Transcription txt file
    from os import listdir, path
    from os.path import isfile, join
    import re
        
    master_transcription_raw = ''
        
    for filename in sorted(listdir('audio files/transcribed')):
        f = open('audio files/transcribed/' + filename, 'r')
        master_transcription_raw = master_transcription_raw + re.findall('(?<=chunk)\d{3}', filename)[0] + ' : ' + f.read() + '\n'
        f.close()
        
    f = open('master_transcription_raw.txt', 'w+')
    f.write(master_transcription_raw)
    f.close()
    
    f = open('master_transcription_edited.txt', 'w+')
    f.write(master_transcription_raw)
    f.close()