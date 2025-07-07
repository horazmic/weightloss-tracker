import sys
from data_io import get_data, input_data
from report import dayly_report
from scrape import main as scrape_main
from datetime import date
from send_email import send_email

def main(do_scrape: bool):
    # set initial parameters
    BMR = 2100
    initial_weight = 99.6
    weight_goal = 90
    target_date = date(2026, 4, 28)
    
    if do_scrape:
        intake, burn, weight  = scrape_main()
        input_data(intake, burn, weight)
    
    data = get_data()
    report = dayly_report(data, BMR, weight_goal, target_date, initial_weight)
    
    send_email(
        subject="Daily Report",
        body=report)

if __name__ == '__main__':
    do_scrape = len(sys.argv) > 1 and sys.argv[1].lower() == 'scrape'
    main(do_scrape)
