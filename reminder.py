import streamlit as st
import schedule
import time
from datetime import datetime
from plyer import notification
import threading
import pytz  # timezone handling

st.title("Water Reminder Setup")

india_tz = pytz.timezone("Asia/Kolkata")
current_time_ist = datetime.now(india_tz)
current_hour = current_time_ist.hour

st.write(f"🕒 Current IST time: {current_time_ist.strftime('%H:%M')}")

WATER_GOAL_LITERS = st.number_input("Enter your water goal (liters):", min_value=0.5, max_value=5.0, step=0.1, value=2.5)
FREQUENCY_MINUTES = st.slider("Remind every (minutes):", 15, 180, 60)

START_HOUR = current_hour
END_HOUR = min(current_hour + 10, 23)  

total_hours = END_HOUR - START_HOUR
total_reminders = max(1, (total_hours * 60) // FREQUENCY_MINUTES)
amount_per_reminder = WATER_GOAL_LITERS / total_reminders

def send_reminder():
    now = datetime.now(india_tz).strftime('%H:%M')
    notification.notify(
        title="Time to Drink Water!",
        message=f"It's {now}. Drink ~{amount_per_reminder:.2f} liters of water.",
        timeout=10
    )
    print(f"[{now}] Reminder sent.")

def start_schedule():
    for hour in range(START_HOUR, END_HOUR):
        for minute in range(0, 60, FREQUENCY_MINUTES):
            time_str = f"{hour:02d}:{minute:02d}"
            schedule.every().day.at(time_str).do(send_reminder)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if st.button("Start Reminders"):
    start_schedule()
    threading.Thread(target=run_scheduler).start()
    st.success("Reminders scheduled!")
