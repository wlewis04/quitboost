import streamlit as st
import pandas as pd
from datetime import date
from PIL import Image
import random

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
        "Habit", "Start Date", "Streak", "Points", "Level", "Status", "Last Marked", "Premium"
    ])

# ------------------------------
# Helper functions
# ------------------------------
def add_habit(name, premium=False):
    new_habit = pd.DataFrame({
        "Habit": [name],
        "Start Date": [date.today().strftime("%Y-%m-%d")],
        "Streak": [0],
        "Points": [0],
        "Level": [1],
        "Status": ["Active"],
        "Last Marked": [""],
        "Premium": [premium]
    })
    return pd.concat([habits, new_habit], ignore_index=True)

def update_points_and_level(idx, bonus=0):
    habits.at[idx, "Points"] += 10 + bonus  # base + bonus
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
    if habits.at[idx, "Premium"]:
        badges.append("Premium Member 💎")
    return badges

def mark_habit(idx):
    today = date.today().strftime("%Y-%m-%d")
    if habits.at[idx, "Last Marked"] != today:
        habits.at[idx, "Streak"] += 1
        habits.at[idx, "Last Marked"] = today
        bonus = 5 if habits.at[idx, "Premium"] else 0
        update_points_and_level(idx, bonus)
        habits.to_csv("habits.csv", index=False)
        st.success(f"{habits.at[idx, 'Habit']} streak: {habits.at[idx, 'Streak']} days, Points: {habits.at[idx, 'Points']}, Level: {habits.at[idx, 'Level']}")
    else:
        st.info(f"{habits.at[idx, 'Habit']} already marked today ✅")

# ------------------------------
# Sidebar: Add Habit
# ------------------------------
st.sidebar.header("Add a New Habit")
habit_name = st.sidebar.text_input("Habit Name")
premium_checkbox = st.sidebar.checkbox("Premium Habit")
if st.sidebar.button("Add Habit"):
    if habit_name.strip() != "":
        habits = add_habit(habit_name.strip(), premium_checkbox)
        habits.to_csv("habits.csv", index=False)
        st.sidebar.success(f"Habit '{habit_name}' added! {'Premium activated!' if premium_checkbox else ''}")

# ------------------------------
# Premium Upgrade
# ------------------------------
st.sidebar.header("Upgrade to Premium 🚀")
st.sidebar.write("Unlock extra points, badges, and exclusive mini-challenges!")
if st.sidebar.button("Upgrade via Stripe"):
    st.sidebar.markdown("[Click here to pay via Stripe](YOUR_STRIPE_CHECKOUT_LINK)")

# ------------------------------
# Active Habits Section
# ------------------------------
st.subheader("Your Active Habits 🎯")
for idx, row in habits.iterrows():
    if row["Status"] == "Active":
        if st.button(f"Mark {row['Habit']} as no slip today ✅", key=idx):
            mark_habit(idx)

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
challenges = [
    "No sugar today for double points!",
    "No social media before 10am for +10 points!",
    "Drink 2L water for +5 points!",
    "Exercise for 20 min for +15 points!"
]
challenge_today = random.choice(challenges)
st.write(challenge_today)
if st.button("Complete Mini-Challenge"):
    for idx, row in habits.iterrows():
        if row["Status"] == "Active":
            bonus = 10 if row["Premium"] else 5
            habits.at[idx, "Points"] += bonus
            update_points_and_level(idx)
    habits.to_csv("habits.csv", index=False)
    st.success(f"Mini-Challenge completed! Points awarded to active habits!")

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
# Sidebar Tip
# ------------------------------
st.sidebar.subheader("Tip 💡")
st.sidebar.info("Check your habits daily to keep your streaks alive! 🚀")