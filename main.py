import sys
from data_io import get_data, input_data
from report import dayly_report
from scrape import main as scrape_main
from datetime import date
from send_email import send_email
import os

def main(do_scrape: bool):
    if do_scrape:
        # scrape data from the website
        print("Scraping data from the website...")
        data = scrape_main()
        input_data(data)
    else:
        # set initial parameters
        parameters = {
            "BMR": 2100,
            "initial_weight": 99.3,
            "weight_goal": 95,
            "target_date": date(2025, 8, 14),
            "name": os.getenv("name")
        }
        # get data and generate report
        data = get_data()
        report = dayly_report(data, parameters) 

        send_email(
            subject=f"Denní přehled {parameters['name']} {date.today()}",
            body=report)

if __name__ == '__main__':
    do_scrape = len(sys.argv) > 1 and sys.argv[1].lower() == 'scrape'
    main(do_scrape)
