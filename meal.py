import streamlit as st
import requests

# Gemini API information
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyClGQusntsKRRi5pDyQzjoBxzPafOCqlko"

# Function to get meal plan with descriptions from Gemini API
def get_meal_plan_with_descriptions(calories, restrictions):
    # Structuring the prompt for the API
    prompt = (
        f"Design a detailed meal plan for one day, tailored to provide approximately {calories} calories. "
        f"The plan should include five meals: breakfast, lunch, dinner, and two snacks. "
        f"For each meal, specify: The meal name. The main ingredient. A brief description of the meal. "
        f"Ensure the meal plan adheres to the following dietary restrictions: {', '.join(restrictions)}. "
        f"The total calorie count should align with the specified target, and the meals should be diverse and balanced."
    )
    
    # Define the data to be sent to the API
    data = {"inputs": prompt}  # Correctly define the `data` variable
    
    # Make the API request
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        
        # Check response status and extract meal plan if successful
        if response.ok:
            try:
                return response.json()[0].get("generated_text", "No meal plan generated.")
            except (KeyError, IndexError, TypeError):
                return "Meal plan could not be generated due to unexpected response format."
        else:
            return f"Meal plan could not be generated. Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Connection error: Unable to reach the Gemini API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

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
