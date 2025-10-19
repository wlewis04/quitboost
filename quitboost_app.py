import streamlit as st
import pandas as pd
from datetime import date, datetime

# ------------------------------
# Streamlit config
# ------------------------------
st.set_page_config(page_title="QuitBoost Ultimate 🚀", layout="wide")
st.title("QuitBoost Ultimate: Gamified Habit Game 🎮")
st.subheader("Turn quitting habits into an addictive game!")

# ------------------------------
# Load or initialize data
# ------------------------------
try:
    habits = pd.read_csv("habits.csv")
except:
    habits = pd.DataFrame(columns=[
        "Habit", "Start Date", "Streak", "Points", "Level", "Status", "Last Marked"
    ])

# ------------------------------
# Helper functions
# ------------------------------
def add_habit(name):
    new_habit = pd.DataFrame({
        "Habit": [name],
        "Start Date": [date.today().strftime("%Y-%m-%d")],
        "Streak": [0],
        "Points": [0],
        "Level": [1],
        "Status": ["Active"],
        "Last Marked": [""]
    })
    return pd.concat([habits, new_habit], ignore_index=True)

def update_points_and_level(idx):
    habits.at[idx, "Points"] += 10  # Base points per day
    while habits.at[idx, "Points"] >= habits.at[idx, "Level"] * 100:
        habits.at[idx, "Level"] += 1
        st.balloons()
        st.success(f"{habits.at[idx, 'Habit']} leveled up to Level {habits.at[idx, 'Level']}!")

def unlock_achievements(idx):
    streak = habits.at[idx, "Streak"]
    points = habits.at[idx, "Points"]
    badges = []
    if streak >= 7: badges.append("1 Week Streak 🏆")
    if streak >= 30: badges.append("1 Month Streak 🏅")
    if points >= 500: badges.append("500 Points Badge ⭐")
    if points >= 1000: badges.append("1k Points Badge 💎")
    return badges

# ------------------------------
# Sidebar: Add Habit
# ------------------------------
st.sidebar.header("Add a New Habit")
habit_name = st.sidebar.text_input("Habit Name")
if st.sidebar.button("Add Habit"):
    if habit_name.strip() != "":
        habits = add_habit(habit_name.strip())
        habits.to_csv("habits.csv", index=False)
        st.sidebar.success(f"Habit '{habit_name}' added!")

# ------------------------------
# Active Habits Section
# ------------------------------
st.subheader("Your Active Habits 🎯")
today = date.today().strftime("%Y-%m-%d")

for idx, row in habits.iterrows():
    if row["Status"] == "Active":
        last_marked = row["Last Marked"]
        if last_marked != today:
            if st.button(f"Mark {row['Habit']} as no slip today ✅", key=idx):
                habits.at[idx, "Streak"] += 1
                habits.at[idx, "Last Marked"] = today
                update_points_and_level(idx)
                habits.to_csv("habits.csv", index=False)
                st.success(f"{row['Habit']} streak: {habits.at[idx, 'Streak']} days, Points: {habits.at[idx, 'Points']}, Level: {habits.at[idx, 'Level']}")
        else:
            st.info(f"{row['Habit']} already marked today ✅")

# ------------------------------
# Achievements
# ------------------------------
st.subheader("Achievements / Badges 🏆")
all_badges = []
for idx, row in habits.iterrows():
    badges = unlock_achievements(idx)
    if badges:
        all_badges.append(f"{row['Habit']}: {', '.join(badges)}")
if all_badges:
    st.write("\n".join(all_badges))
else:
    st.write("No badges yet. Keep going!")

# ------------------------------
# Leaderboard
# ------------------------------
st.subheader("Leaderboard 🏅")
if not habits.empty:
    leaderboard = habits.sort_values(by="Points", ascending=False)[["Habit", "Points", "Level"]]
    st.table(leaderboard)

# ------------------------------
# Mini-Challenge
# ------------------------------
st.subheader("Daily Mini-Challenge 🎲")
challenge_text = "No sugar today for double points!"
st.write(challenge_text)
if st.button("Complete Mini-Challenge"):
    for idx, row in habits.iterrows():
        if row["Status"] == "Active":
            habits.at[idx, "Points"] += 20  # bonus points
            update_points_and_level(idx)
    habits.to_csv("habits.csv", index=False)
    st.success(f"Mini-Challenge completed! +20 points for all active habits!")

# ------------------------------
# Completed / Dropped Habits
# ------------------------------
st.subheader("Completed / Dropped Habits")
completed = habits[habits["Status"] != "Active"]
if not completed.empty:
    st.table(completed)
else:
    st.write("No completed or dropped habits yet.")

# ------------------------------
# Optional: Daily Reminder
# ------------------------------
st.sidebar.subheader("Tip 💡")
st.sidebar.info("Check your habits daily to keep your streaks alive! 🚀")