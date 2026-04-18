import streamlit as st
import google.generativeai as genai

# --- AI Configuration ---
# This looks for the key in your Streamlit Cloud Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("AI Configuration Error: Please check Secrets settings.")

def get_career_insight(q22, q23, q24):
    # (The rest of the function remains the same)

import streamlit as st
import pandas as pd
import os
import random
import string

# --- Configuration ---
CERT_FOLDER = "certificates"
TICKET_FILE = "valid_tickets.csv"
RESPONSE_FILE = "survey_responses.csv"

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

st.set_page_config(page_title="TEGAS Industry Visit Survey", layout="centered")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Survey Instructions", "Take Survey", "Claim Certificate"])

# --- PAGE 1: INSTRUCTIONS ---
if page == "Survey Instructions":
    st.title("Student Feedback Survey")
    st.subheader("Industry Visit: TEGAS Digital Village")
    
    st.markdown("""
    Thank you for participating in the learning visit to **TEGAS Digital Village**. 
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
        q1 = st.select_slider("1. I actively engaged with the sharing sessions.", options=[1, 2, 3, 4, 5])
        q2 = st.select_slider("2. The visit helped me understand what a startup is.", options=[1, 2, 3, 4, 5])
        q3 = st.select_slider("3. I understand how TEGAS can support me.", options=[1, 2, 3, 4, 5])
        
        # Qualitative (4)
        q4 = st.text_area("4. Which types of support do you find most helpful?")
        
        # Likert Scale Questions (5-21)
        st.divider()
        q5 = st.select_slider("5. Real-world exposure to engineering/science.", options=[1, 2, 3, 4, 5])
        q6 = st.select_slider("6. Stimulated curiosity about innovation.", options=[1, 2, 3, 4, 5])
        q7 = st.select_slider("7. Impact on society and environment.", options=[1, 2, 3, 4, 5])
        q8 = st.select_slider("8. Encouraged critical thinking.", options=[1, 2, 3, 4, 5])
        q9 = st.select_slider("9. Awareness of teamwork and creativity.", options=[1, 2, 3, 4, 5])
        q10 = st.select_slider("10. Can relate to concepts learned in class.", options=[1, 2, 3, 4, 5])
        q11 = st.select_slider("11. Better understanding of innovation application.", options=[1, 2, 3, 4, 5])
        q12 = st.select_slider("12. Understood challenges of starting a business.", options=[1, 2, 3, 4, 5])
        q13 = st.select_slider("13. Tips from entrepreneurs were practical.", options=[1, 2, 3, 4, 5])
        q14 = st.select_slider("14. Felt inspired by at least one entrepreneur.", options=[1, 2, 3, 4, 5])
        q15 = st.select_slider("15. Motivated to consider future activities.", options=[1, 2, 3, 4, 5])
        q16 = st.select_slider("16. See more options for my career path.", options=[1, 2, 3, 4, 5])
        q17 = st.select_slider("17. Can imagine starting a business/startup.", options=[1, 2, 3, 4, 5])
        q18 = st.select_slider("18. Helped recognize my strengths.", options=[1, 2, 3, 4, 5])
        q19 = st.select_slider("19. Think differently about facing failure.", options=[1, 2, 3, 4, 5])
        q20 = st.select_slider("20. Could personally relate to a struggle.", options=[1, 2, 3, 4, 5])
        q21 = st.select_slider("21. Confident in ability to explore startups.", options=[1, 2, 3, 4, 5])
        
        # Final Qualitative Questions
        st.divider()
        q22 = st.text_area("22. Most valuable insight/experience gained?")
        q23 = st.text_area("23. Suggestions to improve future visits?")
        
        # Question 24
        # Amended Question 24
        q24 = st.text_area("24. Do you have a company or industry you would like to visit in the future (e.g. technology, creative media, healthcare, engineering, startups)? If yes, please specify.")

        submitted = st.form_submit_button("Submit Survey")

    if submitted:
        # 1. Check for missing answers
        # We check if qualitative text areas are empty or if q24 detail is missing if selected
        if not q4.strip() or not q22.strip() or not q23.strip() or not q24.strip():
            st.error("⚠️ Please answer all questions before submitting.")
        else:
            # 2. Save responses (Anonymized)
            resp_data = {
                "Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, "Q6": q6, "Q7": q7,
                "Q8": q8, "Q9": q9, "Q10": q10, "Q11": q11, "Q12": q12, "Q13": q13,
                "Q14": q14, "Q15": q15, "Q16": q16, "Q17": q17, "Q18": q18, "Q19": q19,
                "Q20": q20, "Q21": q21, "Q22": q22, "Q23": q23, "Q24": q24
            }
            pd.DataFrame([resp_data]).to_csv(RESPONSE_FILE, mode='a', index=False, header=not os.path.exists(RESPONSE_FILE))
            
            # 3. Generate Ticket
            ticket = generate_code()
            pd.DataFrame([{"code": ticket}]).to_csv(TICKET_FILE, mode='a', index=False, header=not os.path.exists(TICKET_FILE))
            
            st.balloons()
            st.success(f"Thank you! Your anonymous completion code is: **{ticket}**")
            st.warning("Copy this code and head to the 'Claim Certificate' page to get your PDF.")

# --- PAGE 3: CLAIM CERTIFICATE ---
elif page == "Claim Certificate":
    st.title("Download Participation Certificate")
    
    # Using a callout box for the examples
    st.info("""
    **Format Examples:**
    * Full Name: **Jenny Choo Cheng Yi**
    * Full Name: **Ali Bin Ahmad**
    
    *Note: Please ensure the spelling matches your official registration.*
    """)
    
    # Added the 'help' parameter for extra clarity
    claim_name = st.text_input(
        "Full Name", 
        help="Enter your name exactly as shown in the examples above to match our records."
    )
    
    claim_code = st.text_input("Completion Code")
    
    if st.button("Verify & Download"):
        if os.path.exists(TICKET_FILE):
            # Read the CSV and ensure we are comparing strings
            tickets_df = pd.read_csv(TICKET_FILE)
            tickets = tickets_df['code'].astype(str).values
            
            if claim_code in tickets:
                # Logic to find the file
                file_path = os.path.join(CERT_FOLDER, f"{claim_name}.pdf")
                
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="📥 Click here to Download PDF", 
                            data=f, 
                            file_name=f"TEGAS_Visit_{claim_name}.pdf",
                            mime="application/pdf"
                        )
                    st.success("Verification successful! Your download is ready.")
                else:
                    st.error(f"Certificate for '{claim_name}' not found. Please check your spelling and try again.")
            else:
                st.error("Invalid Completion Code. Please check the code provided at the end of the survey.")
        else:
            st.error("No submissions found yet.")
