from gtts import gTTS
import os

stations = ["Dormont", "Poplar", "Overbrook", "Glenbury", "Inglewood", "central"]

for i in stations:
    speech=gTTS(text="approaching " + i, lang="en", slow=False)
    speech.save(i + ".mp3")
    os.system("mpg123 " + i + ".mp3")
