from data_io import get_data, input_data
from report import dayly_report
from scrape import main as scrape_main
from datetime import date

def main():
    # set initial parameters
    BMR = 2100
    initial_weight = 99.6
    weight_goal = 90
    target_date = date(2026, 4, 28)
    
    # scrape data from Dine4fit
    intake, burn, weight  = scrape_main()
    input_data(intake, burn, weight)
    
    # get data and generate report
    data = get_data()
    dayly_report(data, BMR, weight_goal, target_date, initial_weight)

    # TODO generate ai overview of the report
    # TODO send report to messenger

if __name__ == '__main__': 
    main()