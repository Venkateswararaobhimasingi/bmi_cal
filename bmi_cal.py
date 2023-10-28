import tkinter as tk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
            user_id INTEGER,
            weight REAL,
            height REAL,
            bmi REAL,
            date TEXT
            )''')

conn.commit()

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = round(weight / (height * height), 2)
        result_label.config(text=f"Your BMI is: {bmi}")
        store_bmi_data(weight, height, bmi)
        classify_bmi(bmi)
        show_bmi_history()
        show_trend_analysis()
    except ValueError:
        result_label.config(text="Please enter valid values for weight and height.")

def store_bmi_data(weight, height, bmi):
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO bmi_records (user_id, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)", (1, weight, height, bmi, formatted_date))
    conn.commit()

def classify_bmi(bmi):
    if bmi < 18.5:
        classification = "Underweight"
    elif 18.5 <= bmi < 25:
        classification = "Normal weight"
    elif 25 <= bmi < 30:
        classification = "Overweight"
    else:
        classification = "Obese"
    classification_label.config(text=f"Classification: {classification}")

def show_bmi_history():
    c.execute("SELECT date, bmi FROM bmi_records")
    data = c.fetchall()

    dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]
    bmis = [row[1] for row in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmis, marker='o')
    plt.title('BMI History')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_trend_analysis():
    c.execute("SELECT bmi FROM bmi_records")
    data = c.fetchall()
    bmis = [row[0] for row in data]
    mean_bmi = round(np.mean(bmis), 2)
    std_dev_bmi = round(np.std(bmis), 2)

    trend_label.config(text=f"Mean BMI: {mean_bmi}, Standard Deviation: {std_dev_bmi}")
    plt.figure(figsize=(8, 4))
    plt.plot(bmis, marker='o')
    plt.title('BMI Trend Analysis')
    plt.xlabel('Record Number')
    plt.ylabel('BMI')
    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("BMI Calculator")
weight_label = tk.Label(root, text="Enter Weight (kg):")
weight_label.pack()
weight_entry = tk.Entry(root)
weight_entry.pack()
height_label = tk.Label(root, text="Enter Height (m):")
height_label.pack()
height_entry = tk.Entry(root)
height_entry.pack()
calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.pack()
result_label = tk.Label(root, text="")
result_label.pack()
classification_label = tk.Label(root, text="")
classification_label.pack()
trend_label = tk.Label(root, text="")
trend_label.pack()
root.mainloop()
