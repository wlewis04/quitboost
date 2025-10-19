import streamlit as st
import pandas as pd
from datetime import date

st.title("QuitBoost ")
st.subheader("Turn quitting habits into a game!")

# Load or initialize habits
try:
    habits = pd.read_csv("habits.csv")
except:
    habits = pd.DataFrame(columns=["Habit", "Start Date", "Streak", "Status"])

# --- Add new habit ---
st.sidebar.header("Add a Habit")
habit_name = st.sidebar.text_input("Habit Name")
if st.sidebar.button("Add Habit"):
    new_habit = pd.DataFrame({
        "Habit": [habit_name],
        "Start Date": [date.today()],
        "Streak": [0],
        "Status": ["Active"]
    })
    habits = pd.concat([habits, new_habit], ignore_index=True)
    habits.to_csv("habits.csv", index=False)
    st.sidebar.success("Habit added!")

# --- Show active habits ---
st.subheader("Your Habits")
for idx, row in habits.iterrows():
    if row["Status"] == "Active":
        if st.button(f"Mark {row['Habit']} as no slip today ", key=idx):
            habits.at[idx, "Streak"] += 1
            habits.to_csv("habits.csv", index=False)
            st.success(f"Streak: {habits.at[idx, 'Streak']} days! Keep going!")

# --- Show completed / dropped habits ---
st.subheader("Completed / Dropped Habits")
completed = habits[habits["Status"] != "Active"]
st.table(completed)
