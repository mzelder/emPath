import os
import json
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
    
def group_picture_ids_by_display(json_file_path):
    # Inicjalizacja pustego słownika do przechowywania pogrupowanych Picture ID
    grouped_picture_ids = {}

    try:
        # Wczytanie danych z pliku .json
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)

        # Iteracja po danych i grupowanie Picture ID według emocji (Display)
        for record in json_data:
            picture_id = record.get("Picture ID")
            display = record.get("Display")

            # Dodanie Picture ID do odpowiedniej listy emocji w słowniku
            if display in grouped_picture_ids:
                grouped_picture_ids[display].append(picture_id)
            else:
                grouped_picture_ids[display] = [picture_id]

        return grouped_picture_ids

    except FileNotFoundError:
        print("Plik textformated.json nie istnieje.")
    except Exception as e:
        print(f"Błąd podczas przetwarzania danych: {str(e)}")
        return None
    
def random_photo(valid_records_random):
    taken_pic = r.choice(valid_records_random)
    valid_records_random.remove(taken_pic)
    return taken_pic

def generate_output():
    CorrectPhoto = random_photo(valid_records_random)

    while True:
        InCorrectPhoto1 = random_photo(valid_records_random)
        if get_display_for_picture_id(InCorrectPhoto1) == get_display_for_picture_id(CorrectPhoto):
            pass
        else:
            break

    while True:
        InCorrectPhoto2 = random_photo(valid_records_random)
        if get_display_for_picture_id(InCorrectPhoto2) == get_display_for_picture_id(CorrectPhoto) or get_display_for_picture_id(InCorrectPhoto2) == get_display_for_picture_id(InCorrectPhoto1):
            pass
        else:
            break

    while True:
        InCorrectPhoto3 = random_photo(valid_records_random)
        if get_display_for_picture_id(InCorrectPhoto3) == get_display_for_picture_id(CorrectPhoto) or get_display_for_picture_id(InCorrectPhoto3) == get_display_for_picture_id(InCorrectPhoto2) or get_display_for_picture_id(InCorrectPhoto3) == get_display_for_picture_id(InCorrectPhoto1):
            pass
        else:
            break
    InCorrectPhotos = [InCorrectPhoto1, InCorrectPhoto2, InCorrectPhoto3]
    return (CorrectPhoto, InCorrectPhotos, get_display_for_picture_id(CorrectPhoto))

print(generate_output())
    