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
    Thank you for participating in the learning visit to TEGAS Digital Village.
This survey aims to gather your feedback and reflections on your learning experience, including your understanding of entrepreneurship, exposure to startups, and personal insights gained from the entrepreneurs’ sharings and facility tour.
Please note that:
•	Your participation in this survey is voluntary. You may withdraw your participation at any time.
•	The survey is anonymous. No personally identifiable information will be collected.
•	Your responses will be used only for learning and teaching enhancement, programme improvement, and educational research purposes.
•	Your answers will not affect your academic results.
The survey will take approximately 5–7 minutes to complete. Please answer honestly based on your experience.
Upon completing the survey, you will be able to obtain a digital certificate of participation.
By proceeding with the survey, you indicate your consent to participate. 
Thank you for your time and valuable feedback.
""")
    st.info("Please click 'Take Survey' in the sidebar to begin.")

# --- PAGE 2: TAKE SURVEY ---
elif page == "Take Survey":
    st.title("Anonymous Survey")
    st.caption("Please answer all questions. 1 = Strongly Disagree, 5 = Strongly Agree.")

    with st.form("survey_form"):
        # Example Question (Keep all your Q1-Q24 here)
        q1 = st.select_slider("1. I actively engaged with the sharing sessions.", options=[1, 2, 3, 4, 5])
        # ... [Add your other questions here as per your previous code] ...
        
        q22 = st.text_area("22. Most valuable insight?")
        q23 = st.text_area("23. Suggestions for improvement?")
        q24 = st.text_area("24. Future company/industry interests?")

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
