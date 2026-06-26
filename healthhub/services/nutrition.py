"""USDA FoodData Central nutrition lookups with a graceful fallback."""
import requests
import streamlit as st

from healthhub.config import USDA_API_KEY, USDA_API_URL


def _nutrient(food, name, unit=None):
    for n in food.get("foodNutrients", []):
        if n.get("nutrientName") == name and (unit is None or n.get("unitName") == unit):
            return n.get("value", 0)
    return 0


def _dv(amount, dv_value, unit):
    if not amount:
        return "0%"
    return f"{min(round((amount / dv_value) * 100), 100)}%"


def api_configured() -> bool:
    return bool(USDA_API_KEY)


def get_nutrition_from_api(food_name: str):
    """Fetch nutrition from USDA; fall back to local data on any failure."""
    if not USDA_API_KEY:
        return get_nutrition_fallback(food_name)
    try:
        params = {"query": food_name, "pageSize": 1, "api_key": USDA_API_KEY}
        resp = requests.get(USDA_API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("foods"):
            return get_nutrition_fallback(food_name)
        food = data["foods"][0]
        return {
            "Calories": _nutrient(food, "Energy", "KCAL"),
            "Protein_g": _nutrient(food, "Protein"),
            "Carbs_g": _nutrient(food, "Carbohydrate, by difference"),
            "Fat_g": _nutrient(food, "Total lipid (fat)"),
            "Fiber_g": _nutrient(food, "Fiber, total dietary"),
            "Sugars_g": _nutrient(food, "Sugars, total including NLEA"),
            "Sodium_mg": _nutrient(food, "Sodium, Na"),
            "Vitamin A": _dv(_nutrient(food, "Vitamin A, IU"), 5000, "IU"),
            "Vitamin C": _dv(_nutrient(food, "Vitamin C, total ascorbic acid"), 90, "mg"),
            "Calcium": _dv(_nutrient(food, "Calcium, Ca"), 1300, "mg"),
            "Iron": _dv(_nutrient(food, "Iron, Fe"), 18, "mg"),
        }
    except Exception:
        return get_nutrition_fallback(food_name)


def get_nutrition_fallback(food_name: str):
    fallback = {
        "Grilled Chicken": {"Calories": 165, "Protein_g": 31, "Carbs_g": 0, "Fat_g": 3.6, "Fiber_g": 0, "Sugars_g": 0, "Sodium_mg": 74, "Vitamin A": "1%", "Vitamin C": "0%", "Calcium": "1%", "Iron": "6%"},
        "Baked Salmon": {"Calories": 206, "Protein_g": 22, "Carbs_g": 0, "Fat_g": 13, "Fiber_g": 0, "Sugars_g": 0, "Sodium_mg": 59, "Vitamin A": "6%", "Vitamin C": "0%", "Calcium": "1%", "Iron": "3%"},
        "Banana": {"Calories": 89, "Protein_g": 1.1, "Carbs_g": 22.8, "Fat_g": 0.3, "Fiber_g": 2.6, "Sugars_g": 12.2, "Sodium_mg": 1, "Vitamin A": "1%", "Vitamin C": "14%", "Calcium": "0%", "Iron": "1%"},
        "Apple": {"Calories": 52, "Protein_g": 0.3, "Carbs_g": 13.8, "Fat_g": 0.2, "Fiber_g": 2.4, "Sugars_g": 10.4, "Sodium_mg": 1, "Vitamin A": "1%", "Vitamin C": "7%", "Calcium": "0%", "Iron": "0%"},
        "Broccoli": {"Calories": 34, "Protein_g": 2.8, "Carbs_g": 7, "Fat_g": 0.4, "Fiber_g": 2.6, "Sugars_g": 1.7, "Sodium_mg": 33, "Vitamin A": "11%", "Vitamin C": "135%", "Calcium": "5%", "Iron": "4%"},
        "Milk": {"Calories": 42, "Protein_g": 3.4, "Carbs_g": 5, "Fat_g": 1, "Fiber_g": 0, "Sugars_g": 5, "Sodium_mg": 44, "Vitamin A": "5%", "Vitamin C": "0%", "Calcium": "12%", "Iron": "0%"},
        "Brown Rice": {"Calories": 111, "Protein_g": 3, "Carbs_g": 23, "Fat_g": 1, "Fiber_g": 1.8, "Sugars_g": 0.4, "Sodium_mg": 5, "Vitamin A": "0%", "Vitamin C": "0%", "Calcium": "1%", "Iron": "2%"},
    }
    return fallback.get(
        food_name,
        {"Calories": 150, "Protein_g": 10, "Carbs_g": 15, "Fat_g": 5, "Fiber_g": 2,
         "Sugars_g": 5, "Sodium_mg": 50, "Vitamin A": "5%", "Vitamin C": "5%",
         "Calcium": "5%", "Iron": "5%"},
    )


def nutrition_score(data) -> str:
    score = 0
    if data.get("Fiber_g", 0) > 3: score += 1
    if data.get("Sugars_g", 0) < 10: score += 1
    if data.get("Sodium_mg", 0) < 200: score += 1
    if data.get("Protein_g", 0) > 10: score += 1
    if data.get("Fat_g", 0) < 10: score += 1
    return "⭐" * score if score else "⭐ (Basic)"


@st.cache_data(show_spinner=False)
def test_api_connection() -> bool:
    if not USDA_API_KEY:
        return False
    try:
        r = requests.get(USDA_API_URL, params={"query": "apple", "pageSize": 1, "api_key": USDA_API_KEY}, timeout=10)
        return r.status_code == 200
    except Exception:
        return False
