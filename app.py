import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

#  Load API Ke
def load_api_key():
    try:
        with open("API_key.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        st.error("⚠️ API key file not found! Please ensure `API_key.txt` exists.")
        st.stop()

# Initialize LLm  Model
def initialize_chat_model():
    api_key = load_api_key()
    return ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)

#  Generate travel sugestion
def generate_travel_suggestions(start_point, end_point):
    system_instruction = SystemMessage(
        content=("You are a smart travel assistant. Provide diverse travel options "
                 "(cab, train, bus, flight) with estimated costs, duration, and travel tips.")
    )
    user_request = HumanMessage(
        content=f"Suggest travel options from {start_point} to {end_point}, including cost estimates and key details."
    )
    
    chat_model = initialize_chat_model()
    try:
        response = chat_model.invoke([system_instruction, user_request])
        return response.content if response else "⚠️ No response from AI."
    except Exception as err:
        return f"❌ Error fetching travel suggestions: {str(err)}"

#  Streamlit  
st.title("🌍 AI Travel Guide")
st.markdown("Plan your journey effortlessly! Get AI-powered travel options with estimated costs and helpful insights.")

# ✅User Inputs
start_point = st.text_input("📍 Departure Location", placeholder="E.g., Delhi")
end_point = st.text_input("🎯 Destination", placeholder="E.g., Kolkata")

if st.button("🔎 Get Travel Suggestions"):
    if start_point.strip() and end_point.strip():
        with st.spinner("⏳ Gathering best travel options..."):
            travel_details = generate_travel_suggestions(start_point, end_point)
            st.success("✅ Here are your travel recommendations:")
            st.markdown(travel_details)
    else:
        st.warning("⚠️ Please enter both departure and destination locations.")
