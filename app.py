import streamlit as st

# ============================================
# 🌩️ StormSenseXU — Evacuation Assistant
# Risk computation · Human-readable summaries · Resource links
# ============================================

# SECTION: core risk logic (written by Aquilah)
def compute_risk(
    wind_speed: float,
    hours_to_landfall: float,
    family_size: int,
    has_car: bool,
    has_elderly_or_disabled: bool = False,
    has_pets: bool = False,
) -> str:
    """Compute a simple categorical risk level based on storm + household factors."""
    score = 0.0

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


# SECTION: evacuation timing recommendation (written by Aquilah)
def recommend_leave_time(risk: str) -> str:
    """Map risk category to a plain-language time recommendation."""
    if risk == "High":
        return "Leave within the next 6 hours."
    elif risk == "Medium":
        return "Prepare to leave within 12–18 hours and monitor official alerts closely."
    else:
        return "Monitor local alerts, but evacuation is not yet urgent."


# SECTION: packing list helper (written by Aquilah)
def generate_packing_list(family_size: int, has_pets: bool = False) -> list[str]:
    """Return a simple recommended packing list based on family size and pets."""
    items: list[str] = []

    water_gallons = max(1, 2 * family_size)
    meals = max(3 * family_size, 6)

    items.append(f"{water_gallons} gallons of water")
    items.append(f"{meals} non-perishable meals (canned food, granola, etc.)")
    items.append("Flashlight + batteries")
    items.append("Basic first-aid kit")
    items.append("Important documents (IDs, insurance, medication list)")

    if has_pets:
        items.append("Pet food, water, and leash/carrier")

    return items


# SECTION: text summary generator (AI-assisted; reviewed & edited by team)
def generate_summary(
    wind_speed: float,
    hours_to_landfall: float,
    family_size: int,
    has_car: bool,
    has_elderly_or_disabled: bool,
    has_pets: bool,
) -> tuple[str, str, list[str]]:
    """
    Build a human-readable explanation + recommendation + packing list
    using the core risk and timing logic above.
    """
    risk = compute_risk(
        wind_speed,
        hours_to_landfall,
        family_size,
        has_car,
        has_elderly_or_disabled,
        has_pets,
    )
    plan = recommend_leave_time(risk)

    car_text = "a car" if has_car else "no car"
    people_text = f"{family_size} people" if family_size > 1 else "1 person"

    # reasons for extra vulnerability
    reasons = []
    if family_size > 4:
        reasons.append("a large household")
    if not has_car:
        reasons.append("no personal vehicle")
    if has_elderly_or_disabled:
        reasons.append("an elderly or disabled member")
    if has_pets:
        reasons.append("pets that also need to be evacuated")

    if reasons:
        reason_text = "; ".join(reasons)
        reason_sentence = (
            f"Because you have {reason_text}, you may need extra time and support "
            "to evacuate safely. "
        )
    else:
        reason_sentence = ""

    summary = (
        f"Based on wind speeds of **{wind_speed} mph** and an estimated landfall "
        f"in **{hours_to_landfall} hours**, your household of **{people_text}** "
        f"with **{car_text}** is at **{risk} risk**. "
        f"{plan} "
        f"{reason_sentence}"
        "Always follow local officials and XULASAFE alerts first."
    )

    packing_list = generate_packing_list(family_size, has_pets)
    return risk, summary, packing_list


# ============================================
# Streamlit app layout
# ============================================

st.set_page_config(
    page_title="StormSenseXU Evacuation Assistant",
    page_icon="🌀",
    layout="centered",
)

st.markdown(
    "<h1 style='text-align:center;'>🌀 StormSenseXU — Evacuation Assistant</h1>",
    unsafe_allow_html=True,
)
st.write(
    "Prototype tool to help households think through hurricane evacuation decisions. "
    "**Not official guidance — always follow emergency managers and XULASAFE.**"
)

st.markdown("### 1. Enter storm forecast information")
col1, col2 = st.columns(2)

with col1:
    wind_speed = st.number_input(
        "Expected sustained wind speed (mph)",
        min_value=0,
        max_value=200,
        value=80,
        step=5,
    )
    hours_to_landfall = st.number_input(
        "Estimated hours until strongest impact/landfall",
        min_value=0,
        max_value=96,
        value=24,
        step=1,
    )

with col2:
    family_size = st.number_input(
        "Household size (people)",
        min_value=1,
        max_value=20,
        value=3,
        step=1,
    )
    has_car = st.checkbox("We have access to a car", value=True)
    has_elderly_or_disabled = st.checkbox(
        "Someone is elderly or has a disability", value=False
    )
    has_pets = st.checkbox("We have pets that would evacuate with us", value=False)

st.markdown("")

if st.button("🧮 Assess evacuation risk"):
    risk, summary, packing_list = generate_summary(
        wind_speed,
        hours_to_landfall,
        int(family_size),
        has_car,
        has_elderly_or_disabled,
        has_pets,
    )

    st.markdown("### 2. Results")
    st.markdown(f"**Risk level:** `{risk}`")
    st.markdown(summary)

    st.markdown("### 3. Suggested packing list")
    for item in packing_list:
        st.markdown(f"- {item}")

    st.info(
        "This is a prototype built by Xavier students for educational purposes. "
        "It does not replace advice from local officials or FEMA."
    )

st.markdown("---")
st.markdown("### 🛟 Official emergency resources")
st.markdown(
    """
- [National Hurricane Center](https://www.nhc.noaa.gov/) – official forecasts and advisories  
- [FEMA Disaster Recovery Center Locator](https://egateway.fema.gov/ESF6/DRCLocator) – find support after a storm  
"""
)

st.markdown("### 💚 Connection to XULASAFE")
st.write(
    "StormSenseXU is designed to **complement** Xavier's XULASAFE system by giving students and families "
    "a simple way to think through evacuation risk and basic preparation at home. "
    "In the future, the logic here could be connected to campus alerts, student first responders, and text notifications."
)

