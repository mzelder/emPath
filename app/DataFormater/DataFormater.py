#DataFormater
import os
import json

# Funkcja do przetwarzania rekordów
def process_records(records):
    processed_records = []
    current_record = {}

    for record in records:
        if 'Displayer ID' in record:
            if current_record:
                processed_records.append(current_record)
                current_record = {}
            current_record['Displayer ID'] = record['Displayer ID']
            current_record.update(record)
        elif 'FACS ' in record:
            current_record['FACS '] = record['FACS ']
            current_record.update(record)
            processed_records.append(current_record)
            current_record = {}
        else:
            current_record.update(record)

    return processed_records

# Wczytanie danych z pliku
with open('textformat.txt', 'r') as file:
    data = json.load(file)

# Przetwarzanie rekordów
processed_data = process_records(data)

with open('textformated.json', 'w') as file:
    json.dump(processed_data, file, indent=4)

print("Dane zostały zapisane do pliku 'textformated.json'.")