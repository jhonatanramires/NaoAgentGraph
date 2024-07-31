import speech_recognition as sr
import numpy as np
from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
import torch
import argparse
from faster_whisper import WhisperModel
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

from fuzzywuzzy import fuzz

from speechToText.utils.microphone_setup import setup_microphone
from speechToText.utils.whisperUtils import load_model, get_parser

class SpeechToText():
  def __init__(self,Action, trigger, debug=True):
    self.Action = Action
    self.trigger = trigger 
    self.debug = debug
    #Loading Arguments 
    self.parser = get_parser()
    self.args = self.parser.parse_args()
    
    #Getting the microphone using setup_microphone 
    self.source = setup_microphone(self.args)

    # If there is no source not doing anything
    if not self.source:
      return
    
    # The last time a recording was retrieved from the queue.
    self.phrase_time = None
    # Thread safe Queue for passing data from the threaded recording callback.
    self.data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
    self.recorder = sr.Recognizer()
    self.recorder.energy_threshold = self.args.energy_threshold
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
    self.recorder.dynamic_energy_threshold = False

    # Load / Download model using load_model function
    self.audio_model = WhisperModel("tiny")
    self.temp_file = NamedTemporaryFile().name

    self.record_timeout = self.args.record_timeout
    self.phrase_timeout = self.args.phrase_timeout

    self.transcription = ['']

    with self.source:
      self.recorder.adjust_for_ambient_noise(self.source)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    self.recorder.listen_in_background(self.source, self.record_callback, phrase_time_limit=self.record_timeout)
    
    # Cue the user that we're ready to go.
    print("Model loaded.\n")
    
    self.last_sample = bytes()

    # LLM Specifics
    self.active = False
    self.prompt = ""

  def record_callback(self,_, audio:sr.AudioData) -> None:
    """
    Threaded callback function to receive audio data when recordings finish.
    audio: An AudioData containing the recorded bytes.
    """
    # Grab the raw bytes and push it into the thread safe queue.
    data = audio.get_raw_data()
    self.data_queue.put(data)

  def ActionCaller(self):
    ratio = fuzz.ratio(self.trigger,self.transcription[-1])
    print(self.transcription[-1],ratio)
    if ratio > 50 and not self.active:
      self.active = True
      os.system('cls' if os.name=='nt' else 'clear')
      self.transcription = [""]
      print("escuchando")
    elif self.active:
      prompt = ""
      print("hola: ",self.transcription)
      for words in self.transcription:
        prompt = prompt.join(" ")
        prompt = prompt.join(words)
      self.Action(prompt)
      self.active = False
      self.transcription = [""]

  def Loop(self):
    os.system('cls' if os.name=='nt' else 'clear')
    while True:
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not self.data_queue.empty():
                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                    phrase_complete = True
                # This is the last time we received new audio data from the queue.
                self.phrase_time = now
                
                # Combine audio data from queue
                audio_data = b''.join(self.data_queue.queue)
                self.data_queue.queue.clear()
                
                # Convert in-ram buffer to something the model can use directly without needing a temp file.
                # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # Read the transcription.
                text = ""
                segments, info = self.audio_model.transcribe(audio_np)
                segments = list(segments) 
                for segment in segments:
                  text = text.join(segment.text)

                # If we detected a pause between recordings, add a new item to our transcription.
                # Otherwise edit the existing one.
                if phrase_complete:
                    self.transcription.append(text)
                    self.ActionCaller()
                else:
                    self.transcription[-1] = text

                # Clear the console to reprint the updated transcription.
                #os.system('cls' if os.name=='nt' else 'clear')

                # Flush stdout.
                print('', end='', flush=True)
            else:
                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in self.transcription:
        print(line)

if __name__ == "__main__":
  def Action(prompt):
    print("Hello from the action my buddy",prompt)

  try:
    recognizer = SpeechToText(Action=Action, trigger="realiza algo")
  except Exception as e:
    print(f"Error during initialization: {e}")

  recognizer.Loop()