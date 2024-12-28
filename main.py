import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amt, get_cat, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod #interacts with class level attributes
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod 
    def add_entry(cls, date, amt, cat, des):
        new_entry = {
            "date": date,
            "amount": amt,
            "category": cat,
            "description": des
        }
        with open(cls.CSV_FILE, 'a', newline="") as csvfile: #context manager only opens the file and closes within the scope
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLS)
            writer.writerow(new_entry)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)

        #convert param to datetime object
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask] #return a data frame that is filtered for the target dates
        if filtered_df.empty:
            print("no transactions in the given data range")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)})) #lambda function to format it into 
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
        
        return filtered_df;

def plot_transactions(df):
    df.set_index('date', inplace=True)

    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df.amount, "Income", "g")
    plt.plot(expense_df.index, expense_df.amount, "Expense", "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction in dd-mm-yyyy or enter for today's date: ", allow_default=True)
    amt = get_amt()
    cat = get_cat()
    des = get_description()
    CSV.add_entry(date, amt, cat, des)


def main():
    while True:
        print("\n 1. Add a new transaction \n 2. View transactions within a date range \n 3. Exit")
        choice = input("Enter your choice (1 - 3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (Y/N)").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("exiting")
            return;
        else:
            print("Invalid choice: please enter 1, 2, or 3")

if __name__ == "__main__":
    main();