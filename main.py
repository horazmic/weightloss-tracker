import sys
from data_io import get_data, input_data
from report import dayly_report
from scrape import main as scrape_main
from datetime import date
from send_email import send_email

def main(do_scrape: bool):

    if do_scrape:
        # scrape data from the website
        print("Scraping data from the website...")
        intake, burn, weight  = scrape_main()
        input_data(intake, burn, weight)
    else:
        # set initial parameters
        BMR = 2100
        initial_weight = 99.8
        weight_goal = 90
        target_date = date(2026, 4, 28)

        # get data and generate report
        data = get_data()
        report = dayly_report(data, BMR, weight_goal, target_date, initial_weight)

        send_email(
            subject=f"Denní přehled Michal {date.today()}",
            body=report)

if __name__ == '__main__':
    do_scrape = len(sys.argv) > 1 and sys.argv[1].lower() == 'scrape'
    main(do_scrape)
