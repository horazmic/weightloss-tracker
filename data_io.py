import pandas as pd
import os
from datetime import date as Date

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(script_dir, 'data.csv')

def get_data():
    if not os.path.exists(FILE_PATH):
        print(f"[ERROR] Soubor {FILE_PATH} neexistuje.")
        print("[INFO] Vytvářím nový soubor.")
        df = pd.DataFrame(columns=['DATE', 'INTAKE', 'BURN', 'WEIGHT', 'PROTEIN'])
        df.to_csv(FILE_PATH, index=False)
        print("[INFO] Nový soubor byl vytvořen.")

    try:
        df = pd.read_csv(FILE_PATH, sep=',')
        df.columns = df.columns.str.strip()
        df['INTAKE'] = df['INTAKE'].astype(int)
        df['BURN'] = df['BURN'].astype(int)
        df['WEIGHT'] = df['WEIGHT'].astype(float)
        df['PROTEIN'] = df['PROTEIN'].astype(float)

        data = df.set_index('DATE').to_dict(orient='index')
        print("[INFO] Data byla úspěšně načtena.")
        print(f"[INFO] Počet záznamů: {len(data)}")

        # Kontrola kontinuity dat
        dates = pd.to_datetime(list(data.keys()))
        date_range = pd.date_range(start=dates.min(), end=dates.max())
        if len(date_range) != len(dates):
            print("[WARNING] Data nejsou kontinuální.")

        return data
    except Exception as e:
        print(f"[ERROR] Chyba při načítání dat: {e}")
        return {}

def input_data(data):
    date = Date.today().strftime("%Y-%m-%d")

    def clean_value(value, units):
        for unit in units:
            value = value.replace(unit, "")
        return value.strip()
    intake = clean_value(data.get('intake', ''), ["kcal", " kcal"])
    burn = clean_value(data.get('burn', ''), ["kcal", " kcal"])
    weight = clean_value(data.get('weight', ''), ["kg", " kg"])
    protein = clean_value(data.get('protein', ''), ["g", " g"])
    print(f"[INFO] Intake: {intake} kcal, Burn: {burn} kcal, Weight: {weight} kg, Protein: {protein} g")

    if not os.path.exists(FILE_PATH):
        print(f"[ERROR] Soubor {FILE_PATH} neexistuje.")
        print("[INFO] Vytvářím nový soubor.")
        df = pd.DataFrame(columns=['DATE', 'INTAKE', 'BURN', 'WEIGHT', 'PROTEIN'])
        df.to_csv(FILE_PATH, index=False)
        print("[INFO] Nový soubor byl vytvořen.")

    try:
        new_entry = {
            'DATE': date,
            'INTAKE': int(intake),
            'BURN': int(burn),
            'WEIGHT': float(weight),
            'PROTEIN': int(protein)
        }
    except ValueError:
        print("[ERROR] Invalid value, record not saved.")
        return None

    df = pd.read_csv(FILE_PATH, sep=',')
    df.columns = df.columns.str.strip()

    if date in df['DATE'].values:
        print("[INFO] Record for today already exists. Overwriting.")
        df.loc[df['DATE'] == date, ['INTAKE', 'BURN', 'WEIGHT', 'PROTEIN']] = (
            new_entry['INTAKE'], new_entry['BURN'], new_entry['WEIGHT'], new_entry['PROTEIN']
        )
    else:
        print("[INFO] Adding a new record.")
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

    df.to_csv(FILE_PATH, index=False)
    print("[INFO] Data has been successfully saved.")