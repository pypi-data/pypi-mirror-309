from gtts import gTTS

text = input("text : ")

speech  = gTTS(text = text, lang = "hi" )
speech.save("kaanu.mp3")