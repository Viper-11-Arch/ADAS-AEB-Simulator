import streamlit as st
import pandas as pd
from AEBSimulation import AEBSimulation
import matplotlib.pyplot as plt
import time

if "df" not in st.session_state:
    st.session_state.df = None

# ----- Lay-Out and Title ------
st.set_page_config("AI Assisted ADAS Simulator")
st.set_page_config(layout="wide")
st.title("AI Assisted ADAS Simulator")
st.markdown(
    """AI-Assisted Automated Emergency Braking (AEB) Simulator.
    This project simulates a real-world ADAS AEB system by combining
    physics-based safety logic with machine-learning risk estimation.
    The system dynamically evaluates collision risk, safety zones,
    and braking decisions in real time.
    """
)
#--------Input Slide-Bars-------
st.sidebar.header("Simulation Inputs")
speed_kmph = st.sidebar.slider("Initial Speed(kmph)",0,120,80)
distance = st.sidebar.slider("Obstacle Distance(m)", 5,200,50)
throttle_change = st.sidebar.slider("Throttle Change(%)",0,100,40)
speed_change = st.sidebar.slider("Speed Change(kmph)",0,60,30)
run = st.sidebar.button("Run Simulation")

ZONE_COLORS = {
    "safe_zone" : "#2ecc71",
    "warning_zone" : "#f39c12",
    "critical_zone" : "#e74c3c"
}

# ------- Simulation ---------
if run:
    st.session_state.df = AEBSimulation(speed_kmph, distance, throttle_change,speed_change).run_simulation()
    
    if st.session_state.df is not None:
        df = st.session_state.df
        st.subheader("Live Simulation View")
        road_placeholder = st.empty()
        zone_placeholder = st.empty()
        risk_placeholder = st.empty()
        risk_bar_placeholder = st.empty()

        INITIAL_DISTANCE = df["distance"].iloc[0]
        ROAD_LENGTH = 40

        for _, row in df.iterrows():
            current_distance = row["distance"]
            speed = row["speed_kmph"]
            progress = 1 - (current_distance / INITIAL_DISTANCE)
            car_pos = int((1 - progress) * ROAD_LENGTH)
            car_pos = min(max(car_pos,0),ROAD_LENGTH)

            road = (
                "🚶‍♂️" +
                "-" * car_pos +
                "🚗" +
                "-" * (ROAD_LENGTH - car_pos)
            )

            with road_placeholder.container():
                st.markdown(
                    f""" 
                    <div style="font-size:30px; text-align:center;">
                        {road}
                    </div>
                    <div style = "text-align:center; font-size:16px;">
                        🚗 Speed: <b>{speed:.1f} kmph</b> &nbsp; | &nbsp;
                        🚶‍♂️ Distance: <b>{current_distance:.1f} m</b>
                    </div>
                    """,
                    unsafe_allow_html = True        
                )

            zone = row["zone"]
            risk = float(row["risk"])

            zone_placeholder.markdown(
                f"""   
                <div style="padding:16px; 
                            border-radius:10px;
                            background-color:{ZONE_COLORS[zone]}; 
                            color:white;
                            font-size:20px;
                            font-weight:bold;
                            text-align:center; 
                ">
                    CURRENT ZONE: {zone.upper()}
                </div>      
                """,
                unsafe_allow_html=True
            )
            
            #risk_percent = int(risk * 100)
            
            risk_placeholder.markdown(
                f"""
                    <div style="font-size:28px;
                                font-weight:bold;
                                text-align:center;
                                margin-top:10px;
                    ">
                        Risk Score: {risk:.2f}
                    </div>
                """,
                unsafe_allow_html=True
            )
            bar_width = int(risk * 20)   # 20 blocks wide
            bar = "🟥" * bar_width + "⬜" * (20 - bar_width)

            risk_bar_placeholder.markdown(
                f"""
                <div style="font-size:22px; text-align:center;">
                    Risk Level
                    <br>
                    {bar}
                    <br>
                    <b>{risk*100:.1f}%</b>
                </div>
                """,
                unsafe_allow_html=True
            )
        
            time.sleep(0.2)
        st.success("Simulation Completed")
        #st.write(df.head())


        #------Title Metrics------
        st.subheader("Final State")
        last = df.iloc[-1]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Final Speed(kmph)", f"{last.speed_kmph:.1f}")
        col2.metric("Final Distance(m)",f"{last.distance:.1f}")
        col3.metric("Final_Risk",f"{last.risk:.2f}")
        col4.metric("Final Zone",last.zone)

        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        #----- Speed VS Time ------
        with row1_col1:
            st.subheader("Speed VS Time")

            fig,ax = plt.subplots(figsize=(5,4))
            ax.plot(df["time"],df["speed_kmph"])
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Speed (kmph)")
            ax.set_title("Vehicle Speed Profile")
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

        #----- Distance VS Time ------

        with row1_col2:
            st.subheader("Distance VS Time")

            fig, ax = plt.subplots(figsize=(5,4))
            ax.plot( df["time"],df["distance"])
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Distance (m)")
            ax.set_title("Obstacle Distance Over Time")
            ax.grid(True,alpha=0.3)

            st.pyplot(fig)

        with row2_col1:
            st.subheader("Risk VS Time")
            fig, ax = plt.subplots(figsize=(5,3))
            ax.plot(df["time"],df["risk"])
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Risk Score")
            ax.set_ylim(0,1)
            ax.set_title("Risk Evolution")
            ax.grid(True,alpha=0.3)

            st.pyplot(fig)

        with row2_col2:
            zone_map = {
                "safe_zone" : 0,
                "warning_zone" : 1,
                "critical_zone" : 2
            }

            df["zone_level"] = df["zone"].map(zone_map)

            st.subheader("Zone Timeline")

            fig, ax = plt.subplots(figsize = (5,3))
            ax.step(df["time"],df["zone_level"],where="post")
            ax.set_yticks([0,1,2])
            ax.set_yticklabels(["SAFE","WARNING","CRITICAL"])
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Zone")
            ax.set_title("Safety Zone Over Time")
            ax.grid(True, alpha=0.3)
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)
        
st.caption(
    "Note: This simulator demonstrates ADAS decision logic and risk estimation. "
    "It is not intended for real-world vehicle control."
)
