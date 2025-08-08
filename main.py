import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random as rn
import time
from googletrans import Translator

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"] }


print ('Выберете уровень, введите "easy", "medium" или "hard":')
lvl = input()

if lvl == "easy" or lvl == "medium" or lvl == "hard":
    cont = '1'
    slova = words_by_level[lvl]
else:
    cont = '0'
    print ("Запустите игру еще раз и выберите уровень корректно.")

if cont == "1":

    translator = Translator()
 
    rn.shuffle(slova)

    duration = 5 
    sample_rate = 44100
    num = 0
    print ('Твой счет сейчас: ', num)
    print ('Поехали!')
    for a in slova:
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
    if num<=3:
        print('Проигрыш. Твой результат меньше четырех очков.')
    else:
        print('Ты выиграл!')





