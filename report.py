from datetime import date, timedelta
from ai_report import get_ai_report

def dayly_report (data, parameters):
    # get today's data
    today_str = date.today().strftime("%Y-%m-%d")
    todays_data = data.get(today_str)

    if not todays_data:
        print("[INFO] No data available for today.")
        return None    

    # extract today's values
    intake = todays_data['INTAKE']
    burn = todays_data['BURN']
    weight = todays_data['WEIGHT']
    net_intake = intake - burn

    # calculate total calorie deficit
    calorie_deficit_sum = sum(
        (entry["INTAKE"] - entry["BURN"] - parameters["BMR"]) for entry in data.values()
    )
    average_deficit = calorie_deficit_sum // len(data)

    # calculate average weekly deficit (last 7 days)
    week_calorie_deficit_sum = sum(
        data.get((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"), {"INTAKE": 0, "BURN": 0})["INTAKE"] 
        - data.get((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"), {"INTAKE": 0, "BURN": 0})["BURN"] 
        - parameters["BMR"]
        for i in range(7)
    )
    average_week_deficit = week_calorie_deficit_sum // 7

    # days remaining until the target date
    today = date.today()
    days_delta = (parameters["target_date"] - today).days
    
    return generate_report(weight, parameters["weight_goal"], net_intake, parameters["BMR"], days_delta, average_deficit, average_week_deficit, calorie_deficit_sum, parameters["initial_weight"], parameters["target_date"], parameters)
    # get_ai_report(data, avarege_deficit , days_delta, weight_goal)

def generate_report(weight, weight_goal, net_intake, BMR, days_delta, average_deficit, average_week_deficit, calorie_deficit_sum, initial_weight, target_date, parameters):
    kg_in_kcal = 7700
    lines = []

    lines.append("=" * 30)
    lines.append(f"                 📊 REPORT HUBNUTÍ {parameters['name']}")
    lines.append("=" * 30)

    # Základní statistiky
    expected_loss = abs(calorie_deficit_sum) / kg_in_kcal
    expected_weight = initial_weight - expected_loss
    actual_weight_loss = initial_weight - weight

    lines.append(f"🔥 Celkový kalorický deficit:    {calorie_deficit_sum:,.0f} kcal")
    lines.append(f"📉 Očekávaný úbytek váhy:        {expected_loss:.1f} kg")
    lines.append(f"📉 Skutečný úbytek váhy:         {actual_weight_loss:.1f} kg")
    lines.append(f"📉 Očekávaná váha:               {expected_weight:.1f} kg")
    lines.append(f"⚖️  Aktuální váha:                {weight:.1f} kg")

    # Dnešní deficit
    daily_deficit = net_intake - BMR
    fat_loss_grams = ((BMR - net_intake) / kg_in_kcal) * 1000
    lines.append(f"\n🥗 Dnešní kalorický rozdíl:      {daily_deficit:+} kcal")
    lines.append(f"💧 Odhad úbytku tuku dnes:       {fat_loss_grams:.0f} g")

    # Průměry
    lines.append(f"📉 Průměrný denní deficit:       {average_deficit:,.0f} kcal")      
    lines.append(f"📊 7denní průměr deficitu:       {average_week_deficit:,.0f} kcal") 

    weight_left = weight - weight_goal
    total_calories_needed = weight_left * kg_in_kcal
    days_till_goal = total_calories_needed / abs(average_week_deficit) if average_week_deficit != 0 else float('inf')
    estimated_reach_date = (date.today() + timedelta(days=int(days_till_goal))).strftime('%d.%m.%Y')

    if average_week_deficit > 0:
        lines.append(f"\n⚠️  Přibíráš na váze.")
    else:
        lines.append(f"🔥 Potřebný deficit celkem:      {total_calories_needed:,.0f} kcal")
        lines.append(f"📆 Odhad dnů do cíle:            {days_till_goal:.0f} dní")
        lines.append(f"📅 Odhad dosažení cíle:          {estimated_reach_date}")

    lines.append(f"📅 Dní do cílového data:         {days_delta}")
    lines.append(f"🎯 Cílová váha:                  {weight_goal:.1f} kg")
    lines.append(f"\n🎯 Zbývá shodit:                 {weight_left:.1f} kg")

    # Stav
    lines.append("\n[Stav]")
    if days_till_goal < days_delta:
        lines.append("✅ Jsi na dobré cestě! Jen tak dál! 🚀")
    else:
        recommended_deficit = total_calories_needed / days_delta
        lines.append("⚠️  Jsi pozadu. Zvaž úpravu plánu.")
        lines.append(f"💡 Doporučený denní deficit:     {recommended_deficit:.0f} kcal")

    # Finální predikce
    estimated_weight_at_target_date = weight - (days_delta * abs(average_week_deficit)) / kg_in_kcal  
    lines.append(f"🔮 Odhad váhy k {target_date}: {estimated_weight_at_target_date:.1f} kg")
    lines.append("=" * 30)

    return "\n".join(lines)
