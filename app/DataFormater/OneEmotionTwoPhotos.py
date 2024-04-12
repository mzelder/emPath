import os
import json
import random
#import Random4Photos1Emotion as r4p
import math as m
json_file_path = 'textformated.json'

def get_random_picture_ids_by_emotion(json_file_path):
    # Wczytanie danych z pliku JSON
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    chosen_emotion_picture_data = []

    # Losowanie emocji
    chosen_emotion = random.choice(['joy', 'disgust', 'surprise', 'fear', 'sadness', 'anger'])

    # Wybieranie Picture ID i ich Intensity (0-1) dla wybranej emocji
    for record in json_data:
        if record['Display'] == chosen_emotion:
            picture_data = {'Picture ID': record['Picture ID'], 'Intensity (0-1)': record['Intensity (0-1)']}
            chosen_emotion_picture_data.append(picture_data)

    # Losowe wybranie dwóch Picture ID wraz z Intensity (0-1) z wybranej emocji
    threshold = 0.2
    
    selected_picture_data = random.sample(chosen_emotion_picture_data, 2)
    while abs(selected_picture_data[0]['Intensity (0-1)'] - selected_picture_data[1]['Intensity (0-1)']) < threshold:
        selected_picture_data = random.sample(chosen_emotion_picture_data, 2)

    if selected_picture_data[0]['Intensity (0-1)'] > selected_picture_data[1]['Intensity (0-1)']:
        return (selected_picture_data[0]['Picture ID'], selected_picture_data[1]['Picture ID'])
    else:
        return (selected_picture_data[1]['Picture ID'], selected_picture_data[0]['Picture ID'])


def get_output():
    return get_random_picture_ids_by_emotion(json_file_path)

print(get_output())




