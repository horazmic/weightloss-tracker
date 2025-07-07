from datetime import date, timedelta
from ai_report import get_ai_report

def dayly_report (data, BMR, weight_goal, target_date, initial_weight):
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
        (entry["INTAKE"] - entry["BURN"] - BMR) for entry in data.values()
    )
    average_deficit = calorie_deficit_sum // len(data)

    # calculate average weekly deficit (last 7 days)
    week_calorie_deficit_sum = sum(
        data.get((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"), {"INTAKE": 0, "BURN": 0})["INTAKE"] 
        - data.get((date.today() - timedelta(days=i)).strftime("%Y-%m-%d"), {"INTAKE": 0, "BURN": 0})["BURN"] 
        - BMR
        for i in range(7)
    )
    average_week_deficit = week_calorie_deficit_sum // 7

    # days remaining until the target date
    today = date.today()
    days_delta = (target_date - today).days
    
    print_report(weight, weight_goal, net_intake, BMR, days_delta, average_deficit, average_week_deficit, calorie_deficit_sum, initial_weight)
    # get_ai_report(data, avarege_deficit , days_delta, weight_goal)


def print_report(weight, weight_goal, net_intake, BMR, days_delta, average_deficit, average_week_deficit, calorie_deficit_sum, initial_weight):
    kg_in_kcal = 7700

    print("=" * 55)
    print("                    📊 WEIGHT LOSS REPORT")
    print("=" * 55)

    # Basic Statistics
    expected_loss = abs(calorie_deficit_sum) / kg_in_kcal
    expected_weight = initial_weight - expected_loss
    actual_weight_loss = initial_weight - weight
    
    print(f"🔥 Total Calories Burned:        {calorie_deficit_sum:,.0f} kcal")
    print(f"📉 Expected Weight Loss:         {expected_loss:.1f} kg")
    print(f"📉 Actual Weight Loss:           {actual_weight_loss:.1f} kg")
    print(f"📉 Expected Weight:              {expected_weight:.1f} kg")
    print(f"⚖️  Current Weight:               {weight:.1f} kg")
    
    # Daily Deficit
    daily_deficit = net_intake - BMR
    fat_loss_grams = ((BMR - net_intake) / kg_in_kcal) * 1000
    print(f"\n🥗 Today's Deficit:              {daily_deficit:+} kcal")
    print(f"💧 Estimated Fat Loss Today:     {fat_loss_grams:.0f} g")

    # Averages
    print(f"📉 Average Daily Deficit:        {average_deficit:,.0f} kcal")      
    print(f"📊 7-Day Average Deficit:        {average_week_deficit:,.0f} kcal") 
    weight_left = weight - weight_goal
    total_calories_needed = weight_left * kg_in_kcal
    days_till_goal = total_calories_needed / abs(average_week_deficit)
    estimated_reach_date = (date.today() + timedelta(days=int(days_till_goal))).strftime('%d-%m-%Y')
    
    if average_week_deficit > 0:
        print(f"\n⚠️ You are gaining weight.")
    else:
        # Goal Tracking
        
        print(f"🔥 Total Calories Needed:        {total_calories_needed:,.0f} kcal")
        print(f"📆 Estimated Days to Goal:       {days_till_goal:.0f} days")
        print(f"📅 Estimated Date to Reach Goal: {estimated_reach_date}")
    print(f"📅 Days Left Until Target Date:  {days_delta}")
    print(f"\n🎯 Weight Goal:                  {weight_goal:.1f} kg")
    print(f"\n🎯 Weight Left to Goal:          {weight_left:.1f} kg")

    # Status Check
    print("\n[Status]")
    if days_till_goal < days_delta:
        print("✅ You are on track! Keep going! 🚀")
    else:
        recommended_deficit = total_calories_needed / days_delta
        print("⚠️  You are behind schedule. Consider adjusting your plan.")
        print(f"💡 Recommended daily deficit:    {recommended_deficit:.0f} kcal")

    # Final Prediction
    estimated_weight_at_target_date = weight - (days_delta * abs(average_week_deficit)) / kg_in_kcal  
    print(f"🔮 Estimated Weight on 07-01:    {estimated_weight_at_target_date:.1f} kg")
    print("=" * 55)
