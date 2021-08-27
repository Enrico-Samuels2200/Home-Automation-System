from datetime import datetime

def date_text(value):
    switcher = {
        1: 'first',
        2: 'second',
        3: 'third',
        4: 'fourth',
        5: 'fivth',
        6: 'sixth',
        7: 'seventh',
        8: 'eighth',
        9: 'nineth',
        10: 'tenth',
        11: 'eleventh',
        12: 'twelvth',
        13: 'thirteenth',
        14: 'fourteenth',
        15: 'fifteenth',
        16: 'sixteenth',
        17: 'seventeenth',
        18: 'eighteenth',
        19: 'ninteenth',
        20: 'twentieth',
        30: 'thirtieth'
    }
    return switcher.get(int(value), "Invalid day of week")

def convert_time_to_text():
    hour = datetime.now().strftime('%H')
    time_of_day = ''

    time_hour = int(datetime.now().strftime('%I'))
    time_min = int(datetime.now().strftime('%M'))
    time = f'{time_hour} {time_min}'

    if int(hour) > 12:
        time_of_day = 'PM'
    else:
        time_of_day = 'AM'

    return f"It is, {time} {time_of_day}"

def convert_date_to_text():
    day = str(datetime.today().day)
    month = str(datetime.today().month)
    year = datetime.today().year
    
    data = [day, month]
    date = []
    
    for i in data:
        value = ''
        if int(i) >= 10 and int(i) <= 19:
            value += date_text(i)
        elif int(i) == 20 or int(i) == 30:
            value += date_text(i)
        elif int(i) > 20 and int(i) < 30:
            value += f'twenty {date_text(i[1])}'
        elif int(i) > 30 and int(i) <= 31:
            value += f'thirty {date_text(i[1])}'
        else:
            value += date_text(i)
        date.append(str(value))
    date.append(year)

    return f"Today is the {date[0]} of the {date[1]} of {date[2]}"

def main():
    date = convert_date_to_text()
    time = convert_time_to_text()
    

if __name__ == '__main__':
    main()