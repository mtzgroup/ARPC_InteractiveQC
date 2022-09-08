from pubchempy import Compound, get_cids, get_properties
import json 
import requests
import numpy as np
from tcc import client 
from sys import argv
import speech_recognition as sr
import os 
from google.cloud import texttospeech
import playsound

#########################################################################################################
#########################################################################################################
#                              Functions 
#########################################################################################################
#########################################################################################################

# TCC autentication (contact us for valid key)
URL_SERVER = # TO ADD 
USER =       # TO ADD
API_KEY =    # TO ADD

def voice_recognition():

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'file.json'    # TO ADD 
   
# Obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say name of the molecule")
        audio = r.listen(source)
   
    # recognize speech using Google Speech Recognition
    try:
        text =  r.recognize_google(audio)
        print("Recognized sentence: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return text

def text_to_speech(sentence):
# Synthesize speech from the input string of text or ssml.
     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'file.json'   # TO ADD
    
     # Instantiates a client
     client = texttospeech.TextToSpeechClient()
    
     synthesis_input = texttospeech.SynthesisInput(text=sentence)
    
     # Build the voice request, select the language code ("en-US") and the ssml
     # voice gender ("neutral")
     voice = texttospeech.VoiceSelectionParams(
         language_code="en-US", name='en-US-Wavenet-F', ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
     )
    
     # Select the type of audio file you want returned
     audio_config = texttospeech.AudioConfig(
         audio_encoding=texttospeech.AudioEncoding.MP3
     )
    
     # Perform the text-to-speech request on the text input with the selected
     # voice parameters and audio file type
     response = client.synthesize_speech(
         input=synthesis_input, voice=voice, audio_config=audio_config
     )
    
     # The response's audio_content is binary.
     with open("output.mp3", "wb") as out:
         # Write the response to the output file.
         out.write(response.audio_content)
         print('Audio content written to file "output.mp3"')
    
     playsound.playsound('output.mp3', True)

def get_parameters(cids):        

#   Retrieve XYZ and molecular charge from PUBCHEM  

    cids = cids[0]
    try :
          c = Compound.from_cid(cids, record_type='3d')
          Natoms = len(c.to_dict(properties=['atoms'])['atoms'])
          charge = get_properties('charge',cids)[0]['Charge']
          coors = []
          atoms = []
          for i in range(Natoms):
              atoms.append(c.to_dict(properties=['atoms'])['atoms'][i]['element'])
              coors.append([c.to_dict(properties=['atoms'])['atoms'][i]['x'],c.to_dict(properties=['atoms'])['atoms'][i]['y'],c.to_dict(properties=['atoms'])['atoms'][i]['z']])
          geom = np.array(coors)
    except :
          Natoms = None
          atoms = None
          geom = None
          charge = None
     
    return Natoms,atoms,geom,charge

def launch_calculation(name, atoms, geom, charge):   

#   Perform the calculation

    ## Initialize client
    TC = client.Client(url=URL_SERVER, user=USER, api_key=API_KEY,  engine="terachem", verbose=False)

    ## Set the job specification
    tcc_options = {
        # TCC options
        'runtype':      'energy',
        'jobname':      'TerX calculation',
        'units':        'angstrom',
    # TeraChem engine options
        'atoms':        atoms,
        'charge':       charge,
        'spinmult':     1,
        'closed_shell': True,
        'restricted':   True,
        'method':       'pbe0',
        'basis':        '3-21g',
		'convthre': 3.0e-3,
		'precision':'single',
		'dftgrid': 0
    }
    
    result = TC.compute(geom, tcc_options)

    tc_out = result['dipole_moment']
    output = 'The dipole moment of {} in isolation is: '.format(name)
    output += '{:.1f} Debye. '.format(tc_out)

    return output 

def compute(name):  

#   Check if the coordinates are on PUBCHEM and launch the calculation 

    cids = get_cids(name, 'name')
    if not cids:
          raise ValueError("Sorry, I could not find {} on PubChem.".format(name))
    else:
          Natoms,atoms,geom,charge = get_parameters(cids)
          if geom is None:
             raise ValueError("Sorry, I could not find the coordinates of {} on PubChem.".format(name))
          else: 
             results = launch_calculation(name, atoms, geom, charge)
    return  results 

#########################################################################################################
#########################################################################################################
#                              MAIN 
#########################################################################################################
#########################################################################################################

if __name__ == "__main__":

#   Recognize molecule 

    print('WELCOME!')
    text = voice_recognition()

    text_split = text.split()

    molecule = text_split[-1]

#   Launch calculation 
    output = compute(molecule)  
    print(output)
    text_to_speech(output)
    print('Thank you for using TCC!')


