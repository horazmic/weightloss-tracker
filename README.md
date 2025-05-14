# Weightloss Tracker – Automatizovaný systém pro sledování kalorického příjmu a redukci váhy

## 🎯 Úvod
Weight Tracker je aplikace, která umožňuje efektivní sledování kalorického příjmu, výdeje a změn váhy. Díky integraci s AI modelem dokáže analyzovat dosažený pokrok, predikovat dosažení váhových cílů a poskytovat doporučení pro úpravu kalorického deficitu. 

## ✨ Funkce aplikace
- 📈 **Import a validace dat** z CSV souboru
- 🔥 **Výpočet kalorického deficitu/surplusu** vůči bazálnímu metabolismu (BMR)
- 🧠 **AI predikce váhy** na základě aktuálního deficitu a nastaveného cíle
- 🗓️ **Denní reporty** s odhadem dosažení cílové váhy
- 💾 **Ukládání nových dat** a aktualizace historie přímo do CSV

## 🛠️ Použité technologie
- **Python** – Backend logika aplikace
- **Pandas** – Práce s daty a výpočty
- **Ollama AI** – Predikce na základě kalorického deficitu
- **Rich Console** – Stylované tabulky a výstupy
- **Plotext** – Vytváření konzolových grafů

## 🚀 Instalace
1. Naklonujte si repozitář:
    ```bash
    git clone https://github.com/horazmic/weight-tracker.git
    cd weight-tracker
    ```
2. Nainstalujte závislosti:
    ```bash
    pip install -r requirements.txt
    ```
3. Spusťte aplikaci:
    ```bash
    python main.py
    ```

## ⚙️ Použití
- Program po spuštění automaticky načte data z `data.csv`, zkontroluje kontinuitu dat a vypočítá průměrný deficit/surplus.
- Pokud pro daný den není vytvořený záznam program se zeptá na potřebné údaje.
- Na konci zobrazí přehledný report v konzoli a predikce pro další období.

## 📊 Ukázka výstupu
```
===============================================
            📊 WEIGHT LOSS REPORT
===============================================
🔥 Total calories burned: 18,500 kcal
📉 Expected weight loss: 2.4 kg
📉 Actual weight loss: 2.1 kg
⚖️ Today's weight: 102.9 kg
🥗 Today's deficit: -500 kcal
📊 7-day average deficit: -600 kcal
📉 Average daily deficit: -500 kcal
🎯 Weight to goal: 7.9 kg
🔥 Calories needed to lose: 61,000 kcal
📆 Estimated days to goal: 102 days
✅ You are on track! Keep going! 🚀
```
