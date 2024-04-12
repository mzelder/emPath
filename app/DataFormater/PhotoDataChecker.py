import os
import json

def check_picture_ids(jpg_files, json_data):
    picture_ids = [record['Picture ID'] for record in json_data]
    missing_files = [jpg_file for jpg_file in jpg_files if jpg_file not in picture_ids]
    return missing_files

#os.chdir('..')
print(os.path.join(os.getcwd(), 'app', 'static', 'db_files'))
folder_path = os.path.join(os.getcwd(), 'app', 'static', 'db_files')  # Ścieżka do folderu z plikami
json_file_path = 'textformated.json'  # Ścieżka do pliku .json

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


def get_all_files_in_folder(folder_path):
    # Sprawdź, czy folder istnieje
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' nie istnieje.")
        return []

    # Pobierz listę plików w folderze
    file_list = os.listdir(folder_path)

    # Zwróć listę nazw plików
    return file_list

folder_path = 'db_files'

# Wywołanie funkcji i wyświetlenie nazw plików
file_names = get_all_files_in_folder(os.path.join(os.getcwd(), 'app', 'static', 'db_files'))

def get_picture_ids_from_json(json_file_path):
    # Sprawdź, czy plik .json istnieje
    if not os.path.exists(json_file_path):
        print(f"Plik '{json_file_path}' nie istnieje.")
        return []

    # Wczytaj dane z pliku .json
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)

    # Zbuduj listę Picture ID
    picture_ids = [record['Picture ID'] for record in json_data]

    return picture_ids
picture_ids = get_picture_ids_from_json(json_file_path)

# Utwórz listę nazw plików z folderu db_files
db_files_list = os.listdir(os.path.join(os.getcwd(), 'app', 'static', 'db_files'))

# Porównaj listy i zwróć brakujące pliki
missing_files = set(db_files_list) - set(picture_ids)

picture_ids = get_picture_ids_from_json(json_file_path)