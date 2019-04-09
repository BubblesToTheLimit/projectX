import plotly.offline as py
import plotly.graph_objs as go
import Booking as Booking
from datetime import datetime, timedelta, date

def plot_timeframe(bookings: Booking, start_date, end_date):
    expenses_tag_day = calc_expenses_tag_day(bookings, start_date, end_date)
    expenses_tag_day_acc = calc_expenses_tag_day_acc(expenses_tag_day, start_date, end_date)

    plot_all_tags(expenses_tag_day_acc, start_date, end_date)

def calc_expenses_tag_day(bookings: Booking, start_date, end_date):
    """
    Calculate the spendings per tag per day.
    """
    expenses_tag_day = {}

    for booking in bookings:
        print(expenses_tag_day)
        if datetime.strptime(start_date, "%d.%m.%y") < booking.date < datetime.strptime(end_date, "%d.%m.%y"): 
            day = booking.date.strftime(format="%d.%m.%y")
            tag = booking.tag
            value = int(booking.value)
            if not tag:
                tag = "untagged"

            if tag not in expenses_tag_day:
                expenses_tag_day[tag] = {}

            if day in expenses_tag_day[tag]:
                expenses_tag_day[tag][day] += value
            else:
                expenses_tag_day[tag][day] = value

    return expenses_tag_day

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def calc_expenses_tag_day_acc(expenses_tag_day, start_date, end_date):
    """
    Calculate the accumulated spendings per tag per day
    """
    sorted_expenses_tag_day_acc = {}

    for tag, expenses in expenses_tag_day.items():
        print(f"Going trough {tag}:")
        for day in daterange(datetime.strptime(start_date, "%d.%m.%y"), datetime.strptime(end_date, "%d.%m.%y")):
            daystr = day.strftime("%d.%m.%y")

            previous_day = day - timedelta(days=1) 
            previous_daystr = previous_day.strftime("%d.%m.%y")
            if previous_daystr not in expenses:
                previous_expense = 0
            else:
                previous_expense = expenses[previous_daystr]
            
            if daystr in expenses:
                expenses[daystr] += previous_expense 
            else:
                expenses[daystr] = previous_expense 

            print(f"{daystr}: {expenses[daystr]}")

        sorted_expenses_tag_day_acc[tag] = {}
        for key in sorted(expenses.keys()) :
            sorted_expenses_tag_day_acc[tag][key] = expenses[key]

    print(sorted_expenses_tag_day_acc)
    return sorted_expenses_tag_day_acc

def plot_all_tags(expenses_tag_day, start_date, end_date):
    traces = []

    for tag, days in expenses_tag_day.items():            
        x = []
        y = []
        for day, value in expenses_tag_day[tag].items():
            x.append(datetime.strptime(day, "%d.%m.%y"))
            y.append(value)
        traces.append(go.Bar(x=x,y=y,name=tag))


    layout = go.Layout(
        barmode='stack',
        xaxis = dict(
            range = [datetime.strptime(start_date, "%d.%m.%y"), datetime.strptime(end_date, "%d.%m.%y")]
        )
    )

    fig = go.Figure(data=traces, layout=layout)
    py.plot(fig, filename='bar-chart-new')