# import ollama
import os
from datetime import date as Date
import re

def get_ai_report(data, avarege_deficit, days_delta, weight_goal):
    ai_data = {}
    for key, value in data.items():
        ai_data[key] = {
            'CALORIC SURPLUS/DEFICIT': value['INTAKE'] - (value['BURN'] + 2200),
            'WEIGHT ON THIS DATE (KG)': value['WEIGHT']
        }

    prompt = f"""
    Personal Info:
        Age: 22, Male, 188 cm
        Goal: Reduce weight to {weight_goal} kg
    Ideal scenario:
        Deficit of 1000 kcal per day
        That suggests 

    Current Data: {ai_data}
    Avarage deficit is: {avarege_deficit}
    Instructions:
        You are DAVID GOGGINS, lean heavy into it.
        Your response should be brief and to the point.
        Avoid unnecessary details.
        Avoid using sentences like this example: 
        "it's difficult to give an exact number without more information about your diet and exercise habits."
        1 kg of fat = 7700 kcal.
        on 2025-04-04 i started using creatine.
    Tasks:
        1. Analyze my weight trends and summarize in a few sentences.
        2. Estimate the number of days required to reach {weight_goal} kg.
        3. Provide an estimated weight in {days_delta} days based on provided weight data
        4. Am i on the right track to reach my goal? Should i make any changes?
    """
    os.environ["OLLAMA_ACCELERATOR"] = "cuda"
    model = "deepseek-r1:14b"
    response = ollama.chat(model, messages=[{"role": "user", "content": prompt}])
    response = response["message"]["content"]
    pattern = r"<think>.*?</think>"
    print_think = False
    if not print_think: response = re.sub(pattern, "", response, flags=re.S)
    print(response)