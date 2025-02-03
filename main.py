import streamlit as st
import time
import pandas as pd
from datetime import datetime, timedelta
import os


if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=["Task", "Time"])
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = pd.DataFrame(columns=["Task", "Time Completed"])



if "is_paused" not in st.session_state:
    st.session_state.is_paused = False
if "stop_timer" not in st.session_state:
    st.session_state.stop_timer = False

st.set_page_config(page_title="Hour Control", page_icon="🕒", layout="centered")

st.title("Streamlit Hour Control")
st.sidebar.title("Here you organize your tasks")
st.sidebar.markdown("Use the controls to organize your tasks")


task = st.sidebar.text_input("Task", "Type your task here")
time_task = st.sidebar.time_input("Time")

if st.sidebar.button("Add Task"):
    if task.strip():  
        new_task = pd.DataFrame({"Task": [task], "Time": [time_task]})
        st.session_state.tasks = pd.concat([st.session_state.tasks, new_task], ignore_index=True)
        st.sidebar.success("Task added successfully!")
        st.rerun() 

st.sidebar.subheader("Pending Tasks")
st.sidebar.dataframe(st.session_state.tasks)


st.sidebar.subheader("Completed Tasks")
st.sidebar.dataframe(st.session_state.completed_tasks)








if not st.session_state.tasks.empty:
    selected_task = st.selectbox("Select a task", st.session_state.tasks["Task"])


    task_time = st.session_state.tasks.loc[st.session_state.tasks["Task"] == selected_task, "Time"].values[0]


    st.write(f"Duration: {task_time}")


    task_time = datetime.strptime(str(task_time), "%H:%M:%S").time()
    task_time_in_seconds = task_time.hour * 3600 + task_time.minute * 60 + task_time.second


    time_display = st.empty()
    


    def beep():
        try:
            
            if os.name == "nt":
                import winsound
                winsound.Beep(1000, 500)
            
            else:
                print("\a")
        except:
            pass  


  
    if st.button("Start Task"):

       
        for x in range(task_time_in_seconds, 0, -1):
            if st.session_state.stop_timer:
                break
            while st.session_state.is_paused:
                time.sleep(0.5)  

            time_left = str(timedelta(seconds=x))  
            time_display.write(f"⏳ {time_left} left")
            time_display.metric("Time left", time_left)
            time.sleep(1)

        if not st.session_state.stop_timer:
            time_display.write("✅ Task completed!")
            beep()
            new_completed_task = pd.DataFrame({"Task": [selected_task], "Time Completed": [task_time]})
            st.session_state.completed_tasks = pd.concat([st.session_state.completed_tasks, new_completed_task], ignore_index=True)
            st.session_state.tasks = st.session_state.tasks[st.session_state.tasks["Task"] != selected_task]
            st.rerun()

          

 


else:
    st.write("No tasks available. Add a task to start.")

