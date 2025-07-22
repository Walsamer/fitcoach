import streamlit as st
# from app.logic import analyze_and_recommend  # Du implementierst das gleich in logic.py
# from app.database import save_log            # Optional: späteres Speichern in CSV oder DB
# from app.visualize import show_training_chart  # Optional: Verlauf zeigen

st.set_page_config(page_title="FitCoach", page_icon=None, layout="centered")
st.title("FitCoach - geh beweg di endlich!")

st.markdown("""Gib hier dein Training stichpunktartig ein, z.B.: Dumbbell Benchpress 8x 18kg, 8x 18kg, 8x 18kg. 
            Feeling: Schulter Rechts knickt etwas ein, sonst Mega!""")

#Eingabe: Freier-Log Text
raw_log = st.text_area("Trainingslog eingeben", height=150)

#Analyze
if st.Button("Analyze") and raw_log.strip():
    with st.spinner("Analyze"):
        analysis, recommendation = analyze_and_recommend(raw_log)
        
	#Show result:
    st.subheader("Analyzed:")
    st.write(analysis)
    
    st.subheader("Recommendation for next Training")
    st.write(recommendation)

    # Save (optoinal)
    if st.checkbox("Save Trainingslog"):
        save_log(raw_log, analysis, recommendation)
        st.success("Log saved!")

    # Show History
    if st.checkbox("Show log"):
        show_training_chart()

else:
    st.info("Type in your trainingslog and GO!")

