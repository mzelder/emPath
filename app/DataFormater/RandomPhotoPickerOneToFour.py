import os
import json
import random as r

valid_records_file_path = 'valid_records.txt'

valid_records_origin = []
with open(valid_records_file_path, 'r') as file:
    for picture_id in file:
        valid_records_origin.append(picture_id.strip())

valid_records_random = valid_records_origin.copy()

def random_photo(valid_records_random):
    taken_pic = r.choice(valid_records_random)
    valid_records_random.remove(taken_pic)
    return taken_pic


def choose_correct_emotion():
    # Wczytaj Picture ID z pliku valid_records.txt
    with open('valid_records.txt', 'r') as file:
        valid_records = [line.strip() for line in file.readlines()]

    chosen_picture_id = r.choice(valid_records)

    # Wczytaj dane z pliku testformated.json
    with open('textformated.json', 'r') as json_file:
        json_data = json.load(json_file)

    # Znajdź wartość Display dla wybranego Picture ID
    for record in json_data:
        if record['Picture ID'] == chosen_picture_id:
            correct_emotion = record['Display']
            break

    # Zdefiniuj listę emocji
    emotions = ['neutral', 'joy', 'disgust', 'surprise', 'fear', 'sadness', 'anger']

    # Losuj 3 niepoprawne emocje z listy emocji
    emotions.remove(correct_emotion)
    incorrect_emotions = r.sample(emotions, 3)
    return (correct_emotion, incorrect_emotions)


