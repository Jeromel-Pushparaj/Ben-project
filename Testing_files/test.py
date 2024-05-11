from datetime import datetime

def convert_to_datetime(string):
    # Parse the string into a datetime object
    datetime_obj = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
    # Extract the date and time components
    date_obj = datetime_obj.date()
    time_obj = datetime_obj.time()
    return date_obj, time_obj

# Example usage:
string = '2024-05-11'


current_datetime = datetime.now()
date = current_datetime.strftime('%Y-%m-%d')
print("Formatted Date and Time:", f"'{date}'")
marketTime = f"{date}"
print(marketTime," : ", string)

if (marketTime == string):
    print("hi")
