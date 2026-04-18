import streamlit as st
import pandas as pd
import os
import random
import string

# --- Configuration & Helper Functions ---
CERT_FOLDER = "certificates"
TICKET_FILE = "valid_tickets.csv"
RESPONSE_FILE = "survey_responses.csv"

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- APP START ---
st.set_page_config(page_title="TEGAS Industry Visit Survey", layout="centered")

# --- SIDEBAR NAVIGATION ---
page = st.sidebar.selectbox("Navigate", ["Survey Instructions", "Take Survey", "Claim Certificate", "Admin Panel"])

# --- PAGE 1: INSTRUCTIONS ---
if page == "Survey Instructions":
    st.title("Student Feedback Survey")
    st.subheader("Industry Visit: TEGAS Digital Village")
    
    st.markdown("""
    Thank you for participating! 
    
    **Please note:**
    * Participation is **voluntary** and **anonymous**.
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
        q1 = st.select_slider("1. I actively engaged with the sharing sessions.", options=[1, 2, 3, 4, 5])
        q2 = st.select_slider("2. The visit helped me understand startups.", options=[1, 2, 3, 4, 5])
        q3 = st.select_slider("3. I understand how TEGAS can support me.", options=[1, 2, 3, 4, 5])
        
        q4 = st.text_area("4. Which types of support do you find most helpful?")
        
        st.divider()
        # Adding placeholders for Q5-Q21 (You can keep your original full list here)
        q5 = st.select_slider("5. Real-world exposure to engineering/tech.", options=[1, 2, 3, 4, 5])
        # ... (Include all your other sliders here) ...

        st.divider()
        q22 = st.text_area("22. Most valuable insight?")
        q23 = st.text_area("23. Suggestions for improvement?")
        q24 = st.text_area("24. Future company/industry interests?")

        submitted = st.form_submit_button("Submit Survey")

    if submitted:
        if not q4.strip() or not q22.strip() or not q23.strip() or not q24.strip():
            st.error("⚠️ Please answer all questions before submitting.")
        else:
            # Save Raw Responses (Q1 until Q24)
            resp_data = {
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                "Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, 
                "Q22": q22, "Q23": q23, "Q24": q24
            }
            pd.DataFrame([resp_data]).to_csv(RESPONSE_FILE, mode='a', index=False, header=not os.path.exists(RESPONSE_FILE))
            
            # Generate Ticket for Certificate
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
            st.download_button("📥 Download All Responses (CSV)", data=csv, file_name="survey_results.csv")
        else:
            st.info("No data collected yet.")
