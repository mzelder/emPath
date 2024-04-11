import pandas as pd
import os
 #dfsdfsd
def save_data_to_txt():
    # Pobierz ścieżkę do bieżącego katalogu roboczego
    current_dir = os.path.dirname(__file__)
    
    # Ustaw ścieżkę do pliku labels.xlsx w bieżącym katalogu
    excel_file_path = os.path.join(current_dir, "labels.xlsx")

    # Sprawdź, czy plik istnieje
    if os.path.exists(excel_file_path):
        data = pd.read_excel(excel_file_path)
        data_json = data.to_json(orient="records")

        # Zapisz dane do pliku tekstowego
        with open("labels.json", "w") as file:
            file.write(data_json)
    else:
        print("Plik labels.xlsx nie istnieje.")

# Wywołanie funkcji do zapisu danych do pliku
save_data_to_txt()