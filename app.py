import streamlit as st
import pandas as pd
import os
import random
import string
from datetime import datetime, timedelta

# TEMPORARY RESET - Remove these two lines after the app loads once!
#if os.path.exists("survey_responses.csv"): os.remove("survey_responses.csv")
#if os.path.exists("valid_tickets.csv"): os.remove("valid_tickets.csv")

# --- Configuration & Helper Functions ---
CERT_FOLDER = "certificates"
TICKET_FILE = "valid_tickets.csv"
RESPONSE_FILE = "survey_responses.csv"

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- APP START ---
st.set_page_config(page_title="TEGAS Industry Visit Survey", layout="centered")

# --- SIDEBAR NAVIGATION ---
# Initialize session state for navigation if it doesn't exist
if 'page_nav' not in st.session_state:
    st.session_state.page_nav = "Survey Instructions"

# Update the sidebar to use the session state
page = st.sidebar.radio(
    "Go to:", 
    ["Survey Instructions", "Take Survey", "Claim Certificate", "Admin Panel"],
    index=["Survey Instructions", "Take Survey", "Claim Certificate", "Admin Panel"].index(st.session_state.page_nav),
    key="navigation_radio"
)
# --- PAGE 1: INSTRUCTIONS ---
if page == "Survey Instructions":
    st.title("Student Feedback Survey")
    st.subheader("Industry Visit: TEGAS Digital Village")
    
    st.markdown("""
    Thank you for participating in the learning visit to **TEGAS Digital Village** on 15th April 2026 organized by School of Foundation Studies, Swinburne Sarawak. 
    This survey aims to gather your feedback on your understanding of entrepreneurship and personal insights gained.
    
    **Please note:**
    * Participation is **voluntary** and **anonymous**.
    * No personally identifiable information will be collected.
    * Your answers will **not affect your academic results**.
    * It takes approximately **5–7 minutes**.
    
    *Upon completion, you will receive a digital certificate of participation.*
    """)
    # BIG BUTTON FIX: This now triggers a page switch
    if st.button("Proceed to Survey", use_container_width=True):
        st.session_state.page_nav = "Take Survey"
        st.rerun()

# --- PAGE 2: TAKE SURVEY ---
elif page == "Take Survey":
    st.title("Anonymous Survey")
    st.session_state.page_nav = "Take Survey"

    # 1. Define your Likert questions in a list
    questions_list = [
        "I actively engaged with the sharing sessions and demonstrations during the visit.",
        "The visit helped me better understand what a startup is and how entrepreneurs begin their journey.",
        "This visit helped me understand how TEGAS can support me if I want to start my own business.",
        "The visit provided meaningful real-world exposure to engineering, science and digital technologies.",
        "The environment stimulated my curiosity about innovation and startups with the integration of digital technologies.",
        "The visit enhanced my understanding of how engineering, science, and digital solutions impact society and the environment.",
        "The visit enhanced my understanding of how engineering, science, and digital solutions impact society and the environment.",
        "The visit increased my awareness of the importance of creativity, teamwork, and adaptability in innovation.",
        "I can relate what I experienced during the visit to concepts learned in class.",
        "I developed a better understanding of how innovation is created and applied in real-world contexts.",
        "The entrepreneurs’ stories helped me understand the challenges involved in starting a business.",
        "The tips and advice shared by the entrepreneurs were practical and easy to understand.",
        "I felt inspired by at least one of the entrepreneurs who shared their experience.",
        "After this visit, I feel more motivated to consider entrepreneurial activities (e.g. starting a project or business) in the future.",
        "The visit helped me see more options and possibilities for my future career path.",
        "I can imagine myself starting a business or startup at some point in my future.",
        "The entrepreneurs’ sharing helped me recognise my strengths and how I can develop myself further.",
        "The stories shared made me think differently about how to face failures in my life.",
        "I could personally relate to at least one entrepreneur’s life story or struggle.",
        "After this visit, I feel more confident in my ability to explore or engage in entrepreneurial activities."
    ]

    with st.form("survey_form"):
        answers = {}
        scale_text = "*(1 = Strongly Disagree, 5 = Strongly Agree)*"

        # --- LOOP FOR Q1, Q2, Q3 ---
        for i in range(1, 4):
            q_text = questions_list[i-1] # Gets text for Q1-Q3
            st.write(f"**{i}. {q_text}**")
            st.caption(scale_text)
            answers[f"q{i}"] = st.radio(f"q{i}", [1,2,3,4,5], horizontal=True, label_visibility="collapsed", key=f"q{i}")
            st.divider()

        # --- Q4: TEXT AREA (Special Case) ---
        st.write(f"**4. After engaging with the startup sharings and facilities at TEGAS, which types of support do you find most helpful in building entrepreneurial knowledge and skills?**")
        q4 = st.text_area("Your response:", label_visibility="collapsed", key="q4")
        st.divider()

        # --- LOOP FOR Q5 THROUGH Q21 ---
        for i in range(5, 22):
            q_text = questions_list[i-2] # Adjust index because of the Q4 gap
            st.write(f"**{i}. {q_text}**")
            st.caption(scale_text)
            answers[f"q{i}"] = st.radio(f"q{i}", [1,2,3,4,5], horizontal=True, label_visibility="collapsed", key=f"q{i}")
            st.divider()

        # --- Q22, Q23, Q24: TEXT AREAS ---
        q22 = st.text_area("22. What was the most valuable insight or experience you gained from the visit, and how do you think it will influence your future learning or career?, key="q22")
        q23 = st.text_area("23. What suggestion(s) do you have to improve future industrial visits or sharing sessions?, key="q23")
        q24 = st.text_area("24. Do you have a company or industry you would like to visit in the future (e.g. technology, creative media, healthcare, engineering, startups)? If yes, please specify the company name or industry.", key="q24")

        submitted = st.form_submit_button("Submit Survey")

    if submitted:
        # 5. Access the data from 'answers' when saving
        malaysia_time = datetime.utcnow() + timedelta(hours=8)
        
        resp_data = {
            "Timestamp (MYT)": malaysia_time.strftime("%Y-%m-%d %H:%M:%S"),
            **answers,  # This "unpacks" all q1-q21 answers into the dictionary
            "Q4": q4,
            "Q22": q22, 
            "Q23": q23, 
            "Q24": q24
        }
        
        # Save to CSV
        pd.DataFrame([resp_data]).to_csv(RESPONSE_FILE, mode='a', index=False, header=not os.path.exists(RESPONSE_FILE))
        
        # Generate code logic follows...

    if submitted:
        # Check if the text areas are filled
        if not q4.strip() or not q22.strip() or not q23.strip() or not q24.strip():
            st.error("⚠️ Please answer all text questions before submitting.")
        else:
            # --- MALAYSIA TIME CALCULATION ---
            malaysia_time = datetime.utcnow() + timedelta(hours=8)
            timestamp_str = malaysia_time.strftime("%Y-%m-%d %H:%M:%S")

            # 1. Create a dictionary with ALL 24 questions
            resp_data = {
                "Timestamp (MYT)": timestamp_str,
                "Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, 
                "Q6": q6, "Q7": q7, "Q8": q8, "Q9": q9, "Q10": q10, 
                "Q11": q11, "Q12": q12, "Q13": q13, "Q14": q14, "Q15": q15, 
                "Q16": q16, "Q17": q17, "Q18": q18, "Q19": q19, "Q20": q20, 
                "Q21": q21, "Q22": q22, "Q23": q23, "Q24": q24
            }
            
            # 2. Append to CSV
            df_new = pd.DataFrame([resp_data])
            df_new.to_csv(RESPONSE_FILE, mode='a', index=False, header=not os.path.exists(RESPONSE_FILE))
            
            # 3. Generate Ticket
            ticket = generate_code()
            pd.DataFrame([{"code": ticket}]).to_csv(TICKET_FILE, mode='a', index=False, header=not os.path.exists(TICKET_FILE))
            
            st.balloons()
            st.success(f"Thank you! Your completion code is: **{ticket}**")
            st.warning("Copy this code and head to the 'Claim Certificate' page to get your PDF.")

# --- PAGE 3: CLAIM CERTIFICATE ---
elif page == "Claim Certificate":
    st.title("Download Participation Certificate")
    
    st.info("Note: Each completion code can only be used ONCE. Please ensure your name is spelled correctly before clicking verify.")

    # Using a callout box for the examples
    st.info("""
    **Format Examples:**
    * Full Name: **Jenny Choo Cheng Yi**
    * Full Name: **Ali Bin Ahmad**
    """)
    
    # Added the 'help' parameter for extra clarity
    claim_name = st.text_input(
        "Full Name", 
        help="Enter your name exactly as shown in the examples above to match our records."
    )

    claim_code = st.text_input("Completion Code").strip()
    
    if st.button("Verify & Download"):
        if os.path.exists(TICKET_FILE):
            # 1. Load the valid tickets
            tickets_df = pd.read_csv(TICKET_FILE)
            
            # 2. Check if the code exists
            if claim_code in tickets_df['code'].astype(str).values:
                file_path = os.path.join(CERT_FOLDER, f"{claim_name}.pdf")
                
                if os.path.exists(file_path):
                    # --- THE "BURN" LOGIC ---
                    # Remove the used code from the dataframe
                    updated_tickets = tickets_df[tickets_df['code'].astype(str) != claim_code]
                    # Overwrite the CSV file without the used code
                    updated_tickets.to_csv(TICKET_FILE, index=False)
                    
                    # Provide the download
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="📥 Download PDF", 
                            data=f, 
                            file_name=f"Visit_{claim_name}.pdf",
                            mime="application/pdf"
                        )
                    st.success("Verification successful! Your code has been used and is now deactivated.")
                else:
                    st.error(f"Certificate for '{claim_name}' not found. Please ensure the filename exists in your GitHub certificates folder.")
            else:
                st.error("This code is invalid or has already been used.")
        else:
            st.error("No completion records found on the server.")


# --- PAGE 4: ADMIN PANEL ---
elif page == "Admin Panel":
    st.title("📂 Admin Data Retrieval")
    access_code = st.text_input("Enter Access Key", type="password")
    
    if access_code == "Sarawak2026": 
        if os.path.exists(RESPONSE_FILE):
            df = pd.read_csv(RESPONSE_FILE)
            st.write(f"Total Submissions: {len(df)}")
            st.dataframe(df)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Master CSV", data=csv, file_name="TEGAS_Survey_Data.csv")
        else:
            st.info("No data collected yet.")
