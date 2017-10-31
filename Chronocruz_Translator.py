from tkinter import *
import speech_recognition as sr
import pyaudio
from googletrans import Translator
import pyttsx3

#Technical Tweaks
sample_rate = 48000
chunk_size = 2048
device_id = 1
selection = 3

#Initializing the Recognizer
recognizer = sr.Recognizer()

#Initializing the Translator
translator = Translator()

#Initializing the Speaker
speaker = pyttsx3.init()

#Function to get default audio input device
def getAudioDevices():
    p = pyaudio.PyAudio()
    mic_name = p.get_default_input_device_info().get('name')
    mic_list = sr.Microphone.list_microphone_names()
    for i, microphone_name in enumerate (mic_list):
        if microphone_name == mic_name:
            device_id = i

gui = Tk()

#Mode Change
def RadioButtonCallback():
    selection = str(RadButtonVar.get())

#Calling hardware primer function
getAudioDevices()

#Speak Button Pressed
def SpeakCallBack():
    print ("Speak Pressed")
    TextEntry.delete (0, 100)
    with sr.Microphone(device_index = device_id, sample_rate = sample_rate, chunk_size = chunk_size) as AudioSource:
            recognizer.adjust_for_ambient_noise (AudioSource)
            print ("Say Something")
            if (str(RadButtonVar.get()) == "1"):
                audio = recognizer.listen(AudioSource)
                try:
                    text = recognizer.recognize_google(audio, language = 'hi-IN')
                    TextEntry.insert(0, text)
                    print ("You said " + text)
                except sr.UnknownValueError:
                    print ("Could not understand the input")
                except sr.RequestError as e:
                    print ("Check your internet connection; {0}".format(e))
            elif (str(RadButtonVar.get()) == "2"):
                audio = recognizer.listen(AudioSource)
                try:
                    text = recognizer.recognize_google(audio, language = 'en-IN')
                    TextEntry.insert(0, text)
                    print ("You said " + text)
                except sr.UnknownValueError:
                    print ("Could not understand the input")
                except sr.RequestError as e:
                    print ("Check your internet connection; {0}".format(e))
            else:
                TextEntry.insert (0, "Please Select a Mode")
    
#Translate Button Pressed
def TranslateCallBack():
    print ("Translate Pressed")
    textToTranslate = TextEntry.get()
    print (textToTranslate)
    if textToTranslate is not None:
        if (str(RadButtonVar.get()) == "1"):
            translatedText = translator.translate(textToTranslate, src = "hi", dest = "en")
            transVar.set(translatedText.text)
            speaker.say(translatedText.text)
            speaker.runAndWait()       
        elif (str(RadButtonVar.get()) == "2"):
            translatedText = translator.translate(textToTranslate, src = "en", dest = "hi")
            transVar.set(translatedText.text) 
        else:
            translatedText = "Please Select a Mode"        
        

SelectionLabelFrame = LabelFrame (gui, text = "Mode Selection")
SelectionLabelFrame.pack(side = LEFT)

RadButtonVar = IntVar()
R1 = Radiobutton (SelectionLabelFrame, text = "Hindi to English", variable = RadButtonVar, value = 1, command = RadioButtonCallback)
R1.pack (side = TOP)
R2 = Radiobutton (SelectionLabelFrame, text = "English to Hindi", variable = RadButtonVar, value = 2, command = RadioButtonCallback)
R2.pack (side = BOTTOM)

InputFrame = LabelFrame (gui, text = "Input")
InputFrame.pack (side = RIGHT)

SpeakButton = Button (InputFrame, text = "Speak", command = SpeakCallBack)
SpeakButton.pack (side = LEFT)

TranslateButton = Button (InputFrame, text = "Translate", command = TranslateCallBack)
TranslateButton.pack (side = RIGHT)

TextEntryLabelFrame = LabelFrame (gui, text = "Enter Text")
TextEntryLabelFrame.pack (side = BOTTOM)

#EnterTextLabel = Label (InputFrame, text = "Enter Text: ")
#EnterTextLabel.grid (column = 0, row = 1)

TextEntry = Entry (TextEntryLabelFrame, bd = 3, width = 100)
TextEntry.grid (column = 1, row = 1)

TranslationLabelFrame = LabelFrame (gui, text = "Translation")
TranslationLabelFrame.pack (side = BOTTOM)

TranslatedTextLabel = Label (TranslationLabelFrame, text = "Translated Text: ")
TranslatedTextLabel.pack (side = LEFT)

transVar = StringVar()
transVar.set ("")
TranslatedLabel = Label (TranslationLabelFrame, textvariable = transVar, font = ("Helvetica", 40))
TranslatedLabel.pack (side = RIGHT)

gui.mainloop()