import tkinter as tk
from tkcalendar import DateEntry
from datetime import date
from dateutil.relativedelta import relativedelta


root = tk.Tk()
root.title("Date Selector")
root.geometry("400x250")


today = date.today()
max_date = today + relativedelta(months=2)


date_entry = DateEntry(
    root,
    date_pattern="dd/mm/yyyy",
    mindate=today,
    maxdate=max_date
)

date_entry.place(
    x=130,
    y=80
)


def get_date():
    selected_date = date_entry.get_date()
    print("Selected date:", selected_date)
    print(date.isoformat(selected_date))


button = tk.Button(
    root,
    text="Get Date",
    command=get_date
)

button.place(
    x=165,
    y=130
)


root.mainloop()