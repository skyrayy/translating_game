import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random as rn
import time
from googletrans import Translator

words = []

print ('Чтобы играть, пополните список слов. Для добавления слова в список, введите его на русском и нажмите Enter. Чтобы закончить список, введите на новой строке "end". Вы можете добавить максимум 15 слов.')
n=0
while n<16:
    word = input()
    n+=1
    if word == 'end':
        break
    else:
        words.append(word)

print ('Список слов составлен. Начинаем игру.')

translator = Translator()

rn.shuffle(words)

duration = 5 
sample_rate = 44100
num = 0
print ('Твой счет сейчас: ', num)
print ('Поехали!')
for a in words:
    print ('Дождись команды и переведи на английский это слово: ', a)
    time.sleep(3)
    print('Говори...')
    recording = sd.rec(
    int(duration * sample_rate), 
    samplerate=sample_rate,      
    channels=1,                  
    dtype="int16")            
    sd.wait() 
    output_rec = "output.wav"

    wav.write(output_rec, sample_rate, recording)
    print("Стоп! Распознаю слово...")

    b = translator.translate(a, 'en').text

    recognizer = sr.Recognizer()
    with sr.AudioFile(output_rec) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        text = text.lower()
        b = b.lower()
        if text == b:
            num+=1 
            print ('Верно! Твой счет: ', num)
        else:
            print ("Неверно!", ' Ты сказал ', text, ". Твой счет: ", num)

    except sr.UnknownValueError:             
        print ("Неверно! Твой счет: ", num)
    except sr.RequestError as e:             
        print ( f"Ошибка сервиса. Перезапустите игру позже. Код ошибки: {e}" )
        break
    if (n-num)/n<0.6:
        print('Проигрыш. Ты перевел менее 60% слов верно.')
    else:
        print('Ты верно перевел более 60% слов! Победа!')






