import streamlit as st
import pandas as pd
import os
import random
import string
from datetime import datetime, timedelta

# --- Configuration & Helper Functions ---
CERT_FOLDER = "certificates"
TICKET_FILE = "valid_tickets.csv"
RESPONSE_FILE = "survey_responses.csv"

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- APP START ---
st.set_page_config(page_title="TEGAS Industry Visit Survey", layout="centered")

# --- SIDEBAR NAVIGATION (Radio Button Format) ---
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:", 
    ["Survey Instructions", "Take Survey", "Claim Certificate", "Admin Panel"]
)

# --- PAGE 1: INSTRUCTIONS ---
if page == "Survey Instructions":
    st.title("Student Feedback Survey")
    st.subheader("Industry Visit: TEGAS Digital Village")
    
    st.markdown("""
    Thank you for participating in the learning visit to **TEGAS Digital Village** on 15th April 2026. 
    This survey aims to gather your feedback on your understanding of entrepreneurship and personal insights gained.
    
    **Please note:**
    * Participation is **voluntary** and **anonymous**.
    * No personally identifiable information will be collected.
    * Your answers will **not affect your academic results**.
    * It takes approximately **5–7 minutes**.
    
    *Upon completion, you will receive a digital certificate of participation.*
    """)
    if st.button("Proceed to Survey"):
        st.info("Please select 'Take Survey' from the sidebar.")

# --- PAGE 2: TAKE SURVEY ---
elif page == "Take Survey":
    st.title("Anonymous Survey")
    st.caption("Please answer all questions. 1 = Strongly Disagree, 5 = Strongly Agree.")

    with st.form("survey_form"):
        # Likert Scale Questions (1-3)

        # Example Question (Keep all your Q1-Q24 here)
        q1 = st.select_slider("1. I actively engaged with the sharing sessions and demonstrations during the visit.", options=[1, 2, 3, 4, 5])
        q2 = st.select_slider("2. The visit helped me better understand what a startup is and how entrepreneurs begin their journey.", options=[1, 2, 3, 4, 5])
        q3 = st.select_slider("3. This visit helped me understand how TEGAS can support me if I want to start my own business.", options=[1, 2, 3, 4, 5])
        
        # Qualitative (4)
        q4 = st.text_area("4. After engaging with the startup sharings and facilities at TEGAS, which types of support do you find most helpful in building entrepreneurial knowledge and skills?")
        
        # Likert Scale Questions (5-21)
        st.divider()
        q5 = st.select_slider("5. The visit provided meaningful real-world exposure to engineering, science and digital technologies.", options=[1, 2, 3, 4, 5])
        q6 = st.select_slider("6. The environment stimulated my curiosity about innovation and startups with the integration of digital technologies.", options=[1, 2, 3, 4, 5])
        q7 = st.select_slider("7. The visit enhanced my understanding of how engineering, science, and digital solutions impact society and the environment.", options=[1, 2, 3, 4, 5])
        q8 = st.select_slider("8. The visit encouraged me to think critically about real-world engineering, scientific, and digital innovation challenges and opportunities. ", options=[1, 2, 3, 4, 5])
        q9 = st.select_slider("9. The visit increased my awareness of the importance of creativity, teamwork, and adaptability in innovation.", options=[1, 2, 3, 4, 5])
        q10 = st.select_slider("10. I can relate what I experienced during the visit to concepts learned in class.", options=[1, 2, 3, 4, 5])
        q11 = st.select_slider("11. I developed a better understanding of how innovation is created and applied in real-world contexts.", options=[1, 2, 3, 4, 5])
        q12 = st.select_slider("12. The entrepreneurs’ stories helped me understand the challenges involved in starting a business.", options=[1, 2, 3, 4, 5])
        q13 = st.select_slider("13. The tips and advice shared by the entrepreneurs were practical and easy to understand.", options=[1, 2, 3, 4, 5])
        q14 = st.select_slider("14. I felt inspired by at least one of the entrepreneurs who shared their experience.", options=[1, 2, 3, 4, 5])
        q15 = st.select_slider("15. After this visit, I feel more motivated to consider entrepreneurial activities (e.g. starting a project or business) in the future.", options=[1, 2, 3, 4, 5])
        q16 = st.select_slider("16. The visit helped me see more options and possibilities for my future career path.", options=[1, 2, 3, 4, 5])
        q17 = st.select_slider("17. I can imagine myself starting a business or startup at some point in my future.", options=[1, 2, 3, 4, 5])
        q18 = st.select_slider("18. The entrepreneurs’ sharing helped me recognise my strengths and how I can develop myself further.", options=[1, 2, 3, 4, 5])
        q19 = st.select_slider("19. The stories shared made me think differently about how to face failures in my life.", options=[1, 2, 3, 4, 5])
        q20 = st.select_slider("20. I could personally relate to at least one entrepreneur’s life story or struggle.", options=[1, 2, 3, 4, 5])
        q21 = st.select_slider("21. After this visit, I feel more confident in my ability to explore or engage in entrepreneurial activities.", options=[1, 2, 3, 4, 5])
        
        # Final Qualitative Questions
        st.divider()
        q22 = st.text_area("22. What was the most valuable insight or experience you gained from the visit, and how do you think it will influence your future learning or career?")
        q23 = st.text_area("23. What suggestion(s) do you have to improve future industrial visits or sharing sessions?")
        
        # Question 24
        # Amended Question 24
        q24 = st.text_area("24. Do you have a company or industry you would like to visit in the future (e.g. technology, creative media, healthcare, engineering, startups)?")

        submitted = st.form_submit_button("Submit Survey")

    if submitted:
        # Simple check for the qualitative fields
        if not q22.strip() or not q23.strip() or not q24.strip():
            st.error("⚠️ Please answer the text questions before submitting.")
        else:
            # --- MALAYSIA TIME CALCULATION ---
            # Streamlit servers are UTC, so we add 8 hours for Malaysia
            malaysia_time = datetime.utcnow() + timedelta(hours=8)
            timestamp_str = malaysia_time.strftime("%Y-%m-%d %H:%M:%S")

            # Save Responses
            resp_data = {
                "Timestamp (MYT)": timestamp_str,
                "Q1": q1,
                "Q22": q22, "Q23": q23, "Q24": q24
            }
            pd.DataFrame([resp_data]).to_csv(RESPONSE_FILE, mode='a', index=False, header=not os.path.exists(RESPONSE_FILE))
            
            # Generate Ticket
            ticket = generate_code()
            pd.DataFrame([{"code": ticket}]).to_csv(TICKET_FILE, mode='a', index=False, header=not os.path.exists(TICKET_FILE))
            
            st.balloons()
            st.success(f"Thank you! Your completion code is: **{ticket}**")

# --- PAGE 3: CLAIM CERTIFICATE ---
elif page == "Claim Certificate":
    st.title("Download Participation Certificate")
    claim_name = st.text_input("Full Name")
    claim_code = st.text_input("Completion Code")
    
    if st.button("Verify & Download"):
        if os.path.exists(TICKET_FILE):
            tickets_df = pd.read_csv(TICKET_FILE)
            if claim_code in tickets_df['code'].astype(str).values:
                file_path = os.path.join(CERT_FOLDER, f"{claim_name}.pdf")
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button("📥 Download PDF", data=f, file_name=f"Visit_{claim_name}.pdf")
                else:
                    st.error("Certificate not found. Check spelling.")
            else:
                st.error("Invalid Code.")

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
