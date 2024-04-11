import os
import json

def check_picture_ids(jpg_files, json_data):
    picture_ids = [record['Picture ID'] for record in json_data]
    missing_files = [jpg_file for jpg_file in jpg_files if jpg_file not in picture_ids]
    return missing_files

folder_path = 'db_files'  # Ścieżka do folderu z plikami
json_file_path = 'C:\\Users\\mokra\\OneDrive\\Dokumenty\\GitHub\\emPath\\app\\DataFormater\\textformated.json'  # Ścieżka do pliku .json

# Sprawdź, czy folder istnieje
if not os.path.exists(folder_path):
    print(f"Folder '{folder_path}' nie istnieje.")
    exit()

# Sprawdź, czy plik .json istnieje
if not os.path.exists(json_file_path):
    print(f"Plik '{json_file_path}' nie istnieje.")
    exit()

# Pobierz listę plików w folderze
file_list = os.listdir(folder_path)

# Wybierz tylko pliki typu .jpg
jpg_files = [file for file in file_list if file.endswith('.jpg')]

# Wczytaj dane z pliku .json
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Sprawdź, czy każdy plik .jpg ma odpowiadający rekord w pliku .json
missing_files = check_picture_ids(jpg_files, json_data)

# Wyświetl pliki .jpg, których brakuje w pliku .json
if missing_files:
    print("Pliki .jpg, których brakuje w pliku .json:")
    for missing_file in missing_files:
        print(missing_file)
else:
    print("Wszystkie pliki .jpg mają odpowiadające rekordy w pliku .json.")