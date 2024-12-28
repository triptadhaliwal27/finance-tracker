from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid Date Format: Please enter in dd-mm-yyyy format")
        return get_date(prompt, allow_default)


def get_amt():
    try:
        amount = float(input("Enter the amt: "))
        if amount <= 0:
            raise ValueError("Amount must be a positive value")
        return amount
    except ValueError as e:
        print(e)
        return get_amt()

def get_cat():
    cat = input("Enter the category: 'I' for Income or 'E' for Expense: ").upper()
    if cat in CATEGORIES:
        return CATEGORIES[cat]
    else:
        print("Invalid category: Please enter either I for Income or E for Expense ")
        return get_cat();

def get_description():
    return input("Enter a description (optional): ")