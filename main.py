from data_io import get_data, input_data
from report import dayly_report
from scrape import main as scrape_main
from datetime import date


def main():
    BMR = 1600
    initial_weight = 92
    weight_goal = 75
    target_date = date(2026, 4, 28)
    intake, burn, weight  = scrape_main()
    input_data(intake, burn, weight)
    data = get_data()
    dayly_report(data, BMR, weight_goal, target_date, initial_weight)


if __name__ == '__main__': 
    main()