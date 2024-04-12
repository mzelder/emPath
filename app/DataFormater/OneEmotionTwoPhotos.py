import os
import json
import random
import Random4Photos1Emotion as r4p
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

    selected_picture_data = random.sample(chosen_emotion_picture_data, 2)
    print(selected_picture_data)

    # Zapytanie użytkownika, które Picture ID jest bardziej intensywne to można usunąc w zależności jak front to przyjmuje
    print(f"Które Picture ID jest według Ciebie bardziej intensywne dla emocji '{chosen_emotion}'?")
    for idx, data in enumerate(selected_picture_data, start=1):
        print(f"{idx}. Picture ID: {data['Picture ID']}")
    user_choice = input("Wybierz 1 lub 2: ")

    # Ocena, czy wybrane przez użytkownika Picture ID jest bardziej intensywne
    try:
        user_choice_idx = int(user_choice) - 1
        return (selected_picture_data[user_choice_idx]['Intensity (0-1)'] > selected_picture_data[1 - user_choice_idx]['Intensity (0-1)'])
    except (ValueError, IndexError):
        return "Niepoprawny wybór. Wprowadź 1 lub 2."

print(get_random_picture_ids_by_emotion(json_file_path))


