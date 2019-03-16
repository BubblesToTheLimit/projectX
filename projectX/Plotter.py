import plotly.offline as py
import plotly.graph_objs as go
import Booking as Booking
from datetime import datetime

def plot_daily_expenses(bookings: Booking, start_date, end_date):
    x = []
    y = []

    expenses_tag_day = {}

    for booking in bookings:
        print(expenses_tag_day)
        if datetime.strptime(start_date, "%d.%m.%y") < booking.date < datetime.strptime(end_date, "%d.%m.%y"): 
            day = booking.date.strftime(format="%d.%m.%y")
            tag = booking.tag
            value = int(booking.value)
            if not tag:
                tag = "default"

            if tag not in expenses_tag_day:
                expenses_tag_day[tag] = {}

            if day in expenses_tag_day[tag]:
                expenses_tag_day[tag][day] += value
            else:
                expenses_tag_day[tag][day] = value
        
    print(expenses_tag_day)

    for day, value in expenses_tag_day["default"].items():
        x.append(day)
        y.append(value)

    data = [go.Bar(x=x, y=y)]
    py.plot(data, filename='basic-bar')
