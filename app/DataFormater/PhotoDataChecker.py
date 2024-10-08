import os
import json

def check_picture_ids(jpg_files, json_data):
    picture_ids = [record['Picture ID'] for record in json_data]
    missing_files = [jpg_file for jpg_file in jpg_files if jpg_file not in picture_ids]
    return missing_files

#os.chdir('..')
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



def get_all_files_in_folder(folder_path):
    # Sprawdź, czy folder istnieje
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' nie istnieje.")
        return []

    # Pobierz listę plików w folderze
    file_list = os.listdir(folder_path)

    # Zwróć listę nazw plików
    return file_list

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


picture_ids = get_picture_ids_from_json(json_file_path)


with open('valid_records.txt', 'r') as file:
# Wczytaj wszystkie linie pliku do listy
    lines = file.readlines()

    # Usuń z listy linie zawierające Picture ID z listy missing_files
lines = [line.strip() for line in lines if line.strip() not in missing_files]

    # Otwórz plik valid_records.txt w trybie zapisu
with open('valid_records.txt', 'w') as file:
     # Zapisz zmienione linie z powrotem do pliku
    file.write('\n'.join(lines))