import streamlit as st
import pandas as pd
import os
import random
import string
import google.generativeai as genai

# --- AI Configuration ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    # We use st.write or pass here so the app doesn't crash if the key isn't set yet
    model = None 

def get_career_insight(q22, q23, q24):
    prompt = f"""
    Based on these student reflections from a visit to TEGAS Digital Village:
    - Insight: {q22}
    - Suggestions: {q23}
    - Future Interests: {q24}
    
    Provide a 2-3 sentence personalized, encouraging "Career Insight." 
    Focus on how their specific interests relate to the Sarawak digital economy.
    Keep it professional and inspiring.
    """
    if model:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Keep exploring the digital frontier! Your journey in innovation is just beginning."
    else:
        return "Great reflections! Continue exploring the opportunities at TEGAS and beyond."

# --- Configuration & Helper Functions ---
CERT_FOLDER = "certificates"
TICKET_FILE = "valid_tickets.csv"
RESPONSE_FILE = "survey_responses.csv"

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- APP START ---
st.set_page_config(page_title="TEGAS Industry Visit Survey", layout="centered")

# --- SIDEBAR NAVIGATION ---
# Add "Admin Panel" to the list of choices
page = st.sidebar.selectbox("Navigate", ["Survey", "Claim Certificate", "Admin Panel"])

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
        # 1. Check for missing answers
        # We check if qualitative text areas are empty or if q24 detail is missing if selected
        if not q4.strip() or not q22.strip() or not q23.strip() or not q24.strip():
            st.error("⚠️ Please answer all questions before submitting.")
        else:
            # 1. Generate the AI Career Insight
            with st.spinner("AI is analyzing your reflections..."):
                ai_insight = get_career_insight(q22, q23, q24)
            
            # 2. Save ALL responses including the AI insight (Anonymized)
            resp_data = {
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                "Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, "Q6": q6, "Q7": q7,
                "Q8": q8, "Q9": q9, "Q10": q10, "Q11": q11, "Q12": q12, "Q13": q13,
                "Q14": q14, "Q15": q15, "Q16": q16, "Q17": q17, "Q18": q18, "Q19": q19,
                "Q20": q20, "Q21": q21, "Q22": q22, "Q23": q23, "Q24": q24,
                "AI_Insight": ai_insight  # Added this so you can retrieve it later
            }
            pd.DataFrame([resp_data]).to_csv(RESPONSE_FILE, mode='a', index=False, header=not os.path.exists(RESPONSE_FILE))
            
            # 3. Generate Ticket and link it to the AI Insight
            ticket = generate_code()
            ticket_data = {
                "code": ticket, 
                "insight": ai_insight  # This is crucial for the Claim page to work!
            }
            pd.DataFrame([ticket_data]).to_csv(TICKET_FILE, mode='a', index=False, header=not os.path.exists(TICKET_FILE))
            
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
    
# --- SIDEBAR NAVIGATION ---
# ... after your 'Claim Certificate' code block ...

# --- PAGE 4: ADMIN PANEL (Add this here!) ---
elif page == "Admin Panel":
    st.title("📂 Admin Data Retrieval")
    st.write("Secure access to survey responses and AI insights.")

    access_code = st.text_input("Enter Access Key", type="password")
    
    if access_code == "Sarawak2026": 
        if os.path.exists(RESPONSE_FILE):
            responses_df = pd.read_csv(RESPONSE_FILE)
            st.metric("Total Responses", len(responses_df))
            st.dataframe(responses_df.tail(5))
            
            csv_data = responses_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Master CSV for Research",
                data=csv_data,
                file_name=f"TEGAS_Survey_Data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No data collected yet.")
    elif access_code != "":
        st.error("Incorrect Access Key.")
