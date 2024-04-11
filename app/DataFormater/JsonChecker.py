import os
import json

def find_missing_values(json_data):
    missing_values = []

    for record in json_data:
        missing_info = {'Picture ID': record['Picture ID'], 'Missing Values': []}
        for key, value in record.items():
            if value == "" or value is None:
                missing_info['Missing Values'].append(key)
        if missing_info['Missing Values']:
            missing_values.append(missing_info)
        elif not all(key in record for key in ["Displayer ID", "Picture ID", "Male/ Female", "Display", "Agreement (%)", "Putity   (0-1)", "Intensity (0-1)", "N", "FACS "]):
            missing_info['Missing Values'].append("Brak kompletnych danych")
            missing_values.append(missing_info)

    return missing_values

# Ścieżka do pliku .json
json_file_path = 'textformated.json'

# Sprawdź, czy plik .json istnieje
if not os.path.exists(json_file_path):
    print(f"Plik '{json_file_path}' nie istnieje.")
    exit()

# Wczytaj dane z pliku .json
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Znajdź brakujące wartości w pliku .json
missing_values = find_missing_values(json_data)


# Wyświetl nazwy zdjęć, dla których wszystkie dane są poprawne
valid_records = []
for record in json_data:
    is_valid = True
    for key in ["Displayer ID", "Picture ID", "Male/ Female", "Display", "Agreement (%)", "Putity   (0-1)", "Intensity (0-1)", "N", "FACS "]:
        if key not in record:
            is_valid = False
            break
    if is_valid:
        valid_records.append(record['Picture ID'])

# Ścieżka do pliku valid_records.txt
valid_records_file_path = 'valid_records.txt'

with open(valid_records_file_path, 'w') as file:
    for picture_id in valid_records:
        file.write(picture_id + '\n')