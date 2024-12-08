import streamlit as st
import requests

# Gemini API information
API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5-flash:generateText"
GEMINI_API_KEY = "AIzaSyClGQusntsKRRi5pDyQzjoBxzPafOCqlko"  # Replace with your Gemini API Key

# Function to get meal plan with descriptions from Gemini API
def get_meal_plan_with_descriptions(calories, restrictions):
    # Structuring the prompt for the Gemini model
    prompt = (
        f"Create a detailed meal plan for an entire day providing approximately {calories} calories. "
        f"Include breakfast, lunch, dinner, and two snacks, with each meal having a brief description. "
        f"Consider these dietary restrictions: {', '.join(restrictions)}. "
        f"Each meal should have a name, main ingredients, and a short description."
    )
    
    # Gemini API payload
    payload = {
        "input": prompt,
        "temperature": 0.7,  # Adjust for creativity
        "candidateCount": 1,  # Number of responses to generate
        "maxOutputTokens": 512  # Ensure enough space for detailed responses
    }
    
    # Making the API request
    response = requests.post(
        f"{API_URL}?key={GEMINI_API_KEY}",
        json=payload
    )
    
    # Handling the response
    if response.ok:
        try:
            # Extract the generated text
            meal_plan = response.json()["candidates"][0]["output"]
        except (KeyError, IndexError, TypeError):
            meal_plan = "Meal plan could not be generated due to unexpected response format."
    else:
        meal_plan = f"Meal plan could not be generated. Error: {response.status_code} - {response.text}"
    
    return meal_plan

# Calorie calculation function
def calculate_calories(age, weight, height, gender):
    # Using the Harris-Benedict equation for BMR and assuming moderate activity level
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    daily_calories = bmr * 1.55  # Moderate activity factor
    return daily_calories

# Streamlit application
st.title("Daily Calorie Intake & Meal Plan with Descriptions")

# Input fields
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, step=0.1)
height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
gender = st.selectbox("Gender", ["Male", "Female"])
restrictions = st.multiselect("Dietary Restrictions", ["Diabetic", "Vegan", "Vegetarian", "Gluten-Free", "Lactose-Free", "Low-Carb"])

# Calculate button
if st.button("Calculate & Get Meal Plan"):
    if name and age and weight and height and gender:
        daily_calories = calculate_calories(age, weight, height, gender)
        meal_plan = get_meal_plan_with_descriptions(daily_calories, restrictions)
        st.success(f"Hello {name}! Your daily caloric requirement is approximately {daily_calories:.2f} calories.")
        st.subheader("Suggested Meal Plan with Descriptions:")
        st.write(meal_plan)
    else:
        st.error("Please fill in all fields.")
