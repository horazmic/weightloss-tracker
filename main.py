from data_io import get_data, input_data
from report import dayly_report
from datetime import date

def main():
    BMR = 2000
    initial_weight = 105
    weight_goal = 95
    target_date = date(2025, 7, 1)
    input_data()
    data = get_data()
    dayly_report(data, BMR, weight_goal, target_date, initial_weight)

if __name__ == '__main__': 
    main()