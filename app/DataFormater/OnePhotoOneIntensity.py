import os
import json
#import Random4Photos1Emotion as rand
import random as r

valid_records_file_path = 'valid_records.txt'

valid_records_origin = []
with open(valid_records_file_path, 'r') as file:
    for picture_id in file:
        valid_records_origin.append(picture_id.strip())

valid_records_random = valid_records_origin.copy()

def get_display_for_picture_id(picture_id):
    # Ścieżka do pliku textformated.json
    json_file_path = 'textformated.json'

    try:
        # Wczytaj dane z pliku .json
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)

        # Przeszukaj dane w poszukiwaniu odpowiedniego Picture ID
        for record in json_data:
            if record.get("Picture ID") == picture_id:
                return record.get("Display", "Emocja nieznana")

        # Jeśli nie znaleziono odpowiadającego Picture ID
        return None

    except FileNotFoundError:
        return "Plik textformated.json nie istnieje"
    except Exception as e:
        return f"Błąd podczas przetwarzania danych: {str(e)}"

def random_photo(valid_records_random):
    taken_pic = r.choice(valid_records_random)
    valid_records_random.remove(taken_pic)
    return taken_pic

def get_intensity_for_picture_id(picture_id):
    # Ścieżka do pliku textformated.json
    json_file_path = 'textformated.json'

    try:
        # Wczytaj dane z pliku .json
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)

        # Przeszukaj dane w poszukiwaniu odpowiedniego Picture ID
        for record in json_data:
            if record.get("Picture ID") == picture_id:
                return record.get("Intensity (0-1)", "Emocja nieznana")

        # Jeśli nie znaleziono odpowiadającego Picture ID
        return None

    except FileNotFoundError:
        return "Plik textformated.json nie istnieje"
    except Exception as e:
        return f"Błąd podczas przetwarzania danych: {str(e)}"

def get_output():
    while True:
        output = random_photo(valid_records_random)
        if get_display_for_picture_id(output) == 'neutral':
            pass
        else:
            break
    
    return (output, get_intensity_for_picture_id(output))