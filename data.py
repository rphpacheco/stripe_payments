from datetime import datetime, date

date_string = "12/5/2022"

# new_date = datetime.strptime(date_string, '%d/%m/%y %H:%M:%S')
new_date = [int(x) for x in date_string.strip().split("/")]
new_date = date(new_date[2], new_date[1], new_date[0])
print(new_date)
