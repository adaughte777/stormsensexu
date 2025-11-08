# 🌩️ StormSenseXU — Evacuation AI Brain
### Risk computation · Human-readable summaries · FEMA/NHC integration links

def compute_risk(wind_speed, hours_to_landfall, family_size, has_car,
                 has_elderly_or_disabled=False, has_pets=False):
    score = 0

    # wind speed weighting
    if wind_speed >= 74:        # hurricane force
        score += 2
    elif wind_speed >= 40:      # strong storm
        score += 1

    # time weighting
    if hours_to_landfall <= 24:
        score += 2
    elif hours_to_landfall <= 48:
        score += 1

    # household factors
    if family_size > 4:
        score += 1
    if not has_car:
        score += 1
    if has_elderly_or_disabled:
        score += 1
    if has_pets:
        score += 0.5  # smaller bump, but still matters

    # overall risk category
    if score >= 5:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"

# --- TEST CASE INPUT ---
wind_speed = 80                # mph
hours_to_landfall = 20         # hours
family_size = 3
has_car = False
has_elderly_or_disabled = False
has_pets = True

# --- COMPUTE RISK ---
risk_level = compute_risk(
    wind_speed, hours_to_landfall, family_size,
    has_car, has_elderly_or_disabled, has_pets
)

print(f"⚠️ Risk Level: {risk_level}")

def generate_summary(wind_speed, hours_to_landfall, family_size, has_car, has_elderly_or_disabled, has_pets, risk_level):
    reasons = []
    if family_size > 4:
        reasons.append("a large family")
    if not has_car:
        reasons.append("no car")
    if has_elderly_or_disabled:
        reasons.append("an elderly or disabled member")
    if has_pets:
        reasons.append("pets")

    if reasons:
        reason_text = " and ".join(reasons)
        return f"Because you have {reason_text}, your household’s current storm risk is **{risk_level}**."
    else:
        return f"Your household’s current storm risk is **{risk_level}**."

print(generate_summary(wind_speed, hours_to_landfall, family_size, has_car, has_elderly_or_disabled, has_pets, risk_level))

from IPython.display import Markdown

Markdown("""
### 🛟 Official Emergency Resources
- [National Hurricane Center](https://www.nhc.noaa.gov/)
- [FEMA Disaster Recovery Center Locator](https://egateway.fema.gov/ESF6/DRCLocator)

### 💚 Connection to XULASAFE
StormSenseXU complements Xavier’s **XULASAFE** system by offering personalized risk guidance
for students and families off-campus. In the future, registered Xavier first responders could
receive alerts and assist others.
""")


import streamlit as st

st.set_page_config(page_title="StormSenseXU Evacuation Assistant", page_icon="🌀")

def compute_risk(wind_speed, hours_to_landfall, family_size, has_car,
                 has_elderly_or_disabled=False, has_pets=False):
    score = 0
    # wind speed weighting
    if wind_speed >= 74:
        score += 2
    elif wind_speed >= 40:
        score += 1
    # time weighting
    if hours_to_landfall <= 24:
        score += 2
    elif hours_to_landfall <= 48:
        score += 1
    # household factors
    if family_size > 4:
        score += 1
    if not has_car:
        score += 1
    if has_elderly_or_disabled:
        score += 1
    if has_pets:
        score += 0.5
    # overall risk category
    if score >= 5:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"

def recommend_leave_time(risk):
    if risk == "High":
        return "Leave within the next 6 hours."
    elif risk == "Medium":
        return "Prepare to leave within 12–18 hours."
    else:
        return "Monitor local alerts, but evacuation isn’t urgent yet."

def generate_packing_list(family_size, has_pets=False):
    items = []
    water_gallons = max(1, 2 * family_size)
    meals = max(3 * family_size, 6)
    items.append(f"{water_gallons} gallons of water")
    items.append(f"{meals} non-perishable meals (canned food, granola, etc.)")
    items.append("Flashlight + batteries")
    items.append("Basic first-aid kit")
    items.append("Important documents (IDs, insurance, meds list)")
    if has_pets:
        items.append("Pet food + leash/carrier")
    return items

def generate_summary(wind_speed, hours_to_landfall, family_size, has_car,
                     has_elderly_or_disabled=False, has_pets=False):
    risk = compute_risk(wind_speed, hours_to_landfall, family_size, has_car,
                        has_elderly_or_disabled, has_pets)
    plan = recommend_leave_time(risk)
    car_text = "a car" if has_car else "no car"
    people_text = f"{family_size} people" if family_size > 1 else "1 person"
    summary = (
        f"Based on wind speeds of {wind_speed} mph and an estimated landfall in {hours_to_landfall} hours, "
        f"your household of {people_text} with {car_text} is at **{risk} risk**. "
        f"{plan}"
    )
    packing_list = generate_packing_list(family_size, has_pets)
    return summary, packing_list

# Streamlit UI
st.title("StormSenseXU — Evacuation Assistant")
st.markdown("Enter the current forecast and household details to get a risk assessment and packing list.")

col1, col2 = st.columns(2)
with col1:
    wind_speed = st.number_input("Wind speed (mph)", min_value=0, value=40)
    hours_to_landfall = st.number_input("Hours to landfall", min_value=0, value=48)
    family_size = st.number_input("Household size (people)", min_value=1, value=2)
with col2:
    has_car = st.checkbox("Have a car?", value=True)
    has_elderly = st.checkbox("Elderly or disabled household member?", value=False)
    has_pets = st.checkbox("Have pets?", value=False)

if st.button("Assess risk"):
    summary, packing = generate_summary(wind_speed, hours_to_landfall, family_size, has_car, has_elderly, has_pets)
    st.markdown(summary)
    st.subheader("Recommended packing list")
    for item in packing:
        st.write("- " + item)

st.info("To deploy: push this repo to GitHub, then add it in Streamlit Cloud and point to this app.py")
