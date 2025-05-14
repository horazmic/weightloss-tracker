import pandas as pd
import os
from datetime import date as Date

FILE_PATH = './data.csv'

def get_data():
    if not os.path.exists(FILE_PATH):
        print(f"[ERROR] Soubor {FILE_PATH} neexistuje.")
        return {}
    
    try:
        df = pd.read_csv(FILE_PATH, sep=',')
        df.columns = df.columns.str.strip()
        df['INTAKE'] = df['INTAKE'].astype(int)
        df['BURN'] = df['BURN'].astype(int)
        df['WEIGHT'] = df['WEIGHT'].astype(float)

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


def input_data():
    date = Date.today().strftime("%Y-%m-%d")
    if not os.path.exists(FILE_PATH):
        print(f"[ERROR] Soubor {FILE_PATH} neexistuje.")
        return None

    df = pd.read_csv(FILE_PATH, sep=',')
    df.columns = df.columns.str.strip()
    dates = df['DATE'].tolist()
    if date in dates:
        print("[INFO] Záznam pro dnešní den již existuje.")
        return None

    try:
        new_entry = {
            'DATE': date,
            'INTAKE': int(input("\nEnter intake: ")), 
            'BURN': int(input("Enter burn: ")),  
            'WEIGHT': float(input("Enter weight: "))
        }
    except ValueError:
        print("[ERROR] Neplatná hodnota, záznam neuložen.")
        return None

    print("[INFO] Nový záznam:", new_entry)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)
    print("[INFO] Data byla úspěšně uložena.")
    return new_entry
