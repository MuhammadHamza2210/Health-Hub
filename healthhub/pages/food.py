"""Food Database — searchable nutrition explorer with glass cards."""
from datetime import datetime

import pandas as pd
import streamlit as st

from healthhub.config import FOOD_CATEGORIES
from healthhub.styles import hero
from healthhub.services.nutrition import (
    api_configured,
    get_nutrition_from_api,
    nutrition_score,
    test_api_connection,
)

# Food, Calories, Protein, Carbs, Fat, Category, Fiber, Sugars, Sodium
_FOODS = [
    ["Grilled Chicken", 165, 31, 0, 3.6, "Protein", 0, 0, 74],
    ["Baked Salmon", 208, 20, 0, 13, "Protein", 0, 0, 59],
    ["Lamb Chops", 294, 25, 0, 21, "Protein", 0, 0, 87],
    ["Grilled Beef", 271, 26, 0, 19, "Protein", 0, 0, 72],
    ["Turkey Breast", 135, 29, 0, 1.7, "Protein", 0, 0, 49],
    ["Shrimp", 99, 24, 0.2, 0.3, "Protein", 0, 0, 111],
    ["Eggs", 143, 13, 1.1, 9.5, "Protein", 0, 0.6, 142],
    ["Tofu", 76, 8, 2, 4, "Protein", 0.3, 0, 7],
    ["Paneer", 265, 18, 1.2, 20, "Protein", 0, 1, 18],
    ["Grilled Fish", 206, 22, 0, 12, "Protein", 0, 0, 88],
    ["Walnuts", 654, 15, 14, 65, "Nut", 7, 2.6, 2],
    ["Almonds", 579, 21, 22, 50, "Nut", 12, 4.4, 1],
    ["Pistachios", 562, 20, 28, 45, "Nut", 10, 7.7, 1],
    ["Cashews", 553, 18, 30, 44, "Nut", 3.3, 5.9, 12],
    ["Pumpkin Seeds", 446, 19, 54, 19, "Nut", 1.7, 0.3, 18],
    ["Banana", 89, 1.1, 23, 0.3, "Fruit", 2.6, 12, 1],
    ["Apple", 52, 0.3, 14, 0.2, "Fruit", 2.4, 10, 1],
    ["Orange", 47, 0.9, 12, 0.1, "Fruit", 2.4, 9, 0],
    ["Mango", 60, 0.8, 15, 0.4, "Fruit", 1.6, 14, 1],
    ["Strawberries", 32, 0.7, 8, 0.3, "Fruit", 2.0, 4.9, 1],
    ["Blueberries", 57, 0.7, 14, 0.3, "Fruit", 2.4, 10, 1],
    ["Grapes", 69, 0.7, 18, 0.2, "Fruit", 0.9, 16, 2],
    ["Pineapple", 50, 0.5, 13, 0.1, "Fruit", 1.4, 10, 1],
    ["Watermelon", 30, 0.6, 8, 0.2, "Fruit", 0.4, 6, 1],
    ["Peach", 39, 0.9, 10, 0.3, "Fruit", 1.5, 8, 0],
    ["Broccoli", 34, 2.8, 7, 0.4, "Vegetable", 2.6, 1.7, 33],
    ["Spinach", 23, 2.9, 4, 0.4, "Vegetable", 2.2, 0.4, 79],
    ["Carrots", 41, 0.9, 10, 0.2, "Vegetable", 2.8, 4.7, 69],
    ["Bell Pepper", 31, 1, 6, 0.3, "Vegetable", 2.1, 4.2, 3],
    ["Cauliflower", 25, 1.9, 5, 0.3, "Vegetable", 2.0, 1.9, 30],
    ["Sweet Potato", 86, 1.6, 20, 0.1, "Vegetable", 3.0, 4.2, 55],
    ["Zucchini", 17, 1.2, 3, 0.3, "Vegetable", 1.0, 2.5, 8],
    ["Eggplant", 25, 1, 6, 0.2, "Vegetable", 3.0, 3.5, 2],
    ["Cucumber", 16, 0.7, 4, 0.1, "Vegetable", 0.5, 1.7, 2],
    ["Tomato", 18, 0.9, 4, 0.2, "Vegetable", 1.2, 2.6, 5],
    ["Milk", 42, 3.4, 5, 1, "Dairy", 0, 5, 44],
    ["Greek Yogurt", 59, 10, 4, 0.4, "Dairy", 0, 4, 36],
    ["Cheese", 402, 25, 1, 33, "Dairy", 0, 0.1, 621],
    ["Cottage Cheese", 98, 11, 3, 4, "Dairy", 0, 3, 364],
    ["Labneh", 60, 4, 3, 4, "Dairy", 0, 3, 40],
    ["Brown Rice", 111, 3, 23, 1, "Carb", 1.8, 0.4, 5],
    ["Whole Wheat Bread", 247, 13, 41, 4, "Carb", 7.0, 6.0, 477],
    ["Oatmeal", 150, 5, 27, 3, "Carb", 4.0, 1.0, 2],
    ["Quinoa", 120, 4, 21, 2, "Carb", 2.8, 0.9, 7],
    ["Whole Wheat Pasta", 124, 5, 25, 1, "Carb", 3.2, 1.2, 4],
    ["Sweet Corn", 86, 3, 19, 1, "Carb", 2.0, 6.3, 15],
    ["Potato", 77, 2, 17, 0.1, "Carb", 2.2, 0.8, 6],
    ["Whole Wheat Roti", 104, 3, 20, 1, "Carb", 3.0, 0.5, 190],
    ["Bulgur Wheat", 83, 3, 18, 0.2, "Carb", 4.5, 0.2, 5],
    ["Buckwheat", 343, 13, 71, 3, "Carb", 10, 0, 1],
]
_COLUMNS = ["Food", "Calories", "Protein_g", "Carbs_g", "Fat_g", "Category", "Fiber_g", "Sugars_g", "Sodium_mg"]


def _sample_db() -> pd.DataFrame:
    return pd.DataFrame(_FOODS, columns=_COLUMNS)


def _macro_bar(label, value, color):
    return (
        f'<div style="flex:1;text-align:center;">'
        f'<div style="font-size:.72rem;color:var(--muted);">{label}</div>'
        f'<div style="font-size:1.15rem;font-weight:700;color:{color};">{value}g</div></div>'
    )


def _food_card(row):
    emoji = FOOD_CATEGORIES.get(row["Category"], "🍽️")
    st.markdown(
        f"""
        <div class="glass" style="padding:18px 20px;">
          <div style="font-size:2rem;">{emoji}</div>
          <h3 style="margin:.3rem 0 .1rem;">{row['Food']}</h3>
          <div style="color:var(--muted);font-size:.85rem;margin-bottom:12px;">
            {row['Category']} · {row['Calories']} kcal / 100g</div>
          <div style="display:flex;gap:8px;">
            {_macro_bar('Protein', row['Protein_g'], '#7c5cff')}
            {_macro_bar('Carbs', row['Carbs_g'], '#34e7c8')}
            {_macro_bar('Fat', row['Fat_g'], '#ff6ec7')}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _detail_view(db):
    name = st.session_state.selected_food
    row = db[db["Food"] == name].iloc[0]

    if st.button("← Back to search"):
        st.session_state.selected_food = None
        st.rerun()

    _food_card(row)

    # Favorites toggle
    favs = st.session_state.setdefault("favorites", set())
    if name in favs:
        if st.button("❌ Remove from favorites"):
            favs.discard(name); st.rerun()
    else:
        if st.button("❤️ Add to favorites"):
            favs.add(name); st.rerun()

    # Live API nutrition (cached per food)
    cache = st.session_state.setdefault("nutrition_cache", {})
    if name not in cache:
        with st.spinner("Fetching detailed nutrition from USDA…"):
            cache[name] = get_nutrition_from_api(name)
    data = cache[name]

    with st.expander("📊 Detailed nutrition", expanded=True):
        st.caption(f"USDA FoodData Central · retrieved {datetime.now():%Y-%m-%d}")
        st.metric("Nutrition Quality Score", nutrition_score(data))
        display = {
            "Vitamin A": data.get("Vitamin A", "N/A"),
            "Vitamin C": data.get("Vitamin C", "N/A"),
            "Calcium": data.get("Calcium", "N/A"),
            "Iron": data.get("Iron", "N/A"),
            "Fiber": f"{data.get('Fiber_g', 0)}g",
            "Sugars": f"{data.get('Sugars_g', 0)}g",
            "Sodium": f"{data.get('Sodium_mg', 0)}mg",
        }
        cols = st.columns(4)
        for i, (k, v) in enumerate(display.items()):
            cols[i % 4].metric(k, v)

    with st.expander("🧮 Serving size calculator"):
        grams = st.slider("Serving size (grams)", 50, 500, 100, 10)
        r = grams / 100
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Calories", round(row["Calories"] * r))
        c2.metric("Protein", f"{round(row['Protein_g'] * r, 1)}g")
        c3.metric("Carbs", f"{round(row['Carbs_g'] * r, 1)}g")
        c4.metric("Fat", f"{round(row['Fat_g'] * r, 1)}g")


def render():
    hero("🍎 Food Database", "Explore nutrition for 50 whole foods, powered by USDA data.",
         pill="✅ USDA Connected" if api_configured() else "⚠️ Offline mode")

    db = st.session_state.setdefault("food_db", _sample_db())
    st.session_state.setdefault("selected_food", None)

    with st.sidebar:
        st.markdown("### 🔌 API")
        st.write("Status:", "✅ Connected" if api_configured() else "❌ Not configured")
        if st.button("Test connection"):
            st.success("Connection OK") if test_api_connection() else st.error("Connection failed")
        if st.session_state.get("favorites"):
            st.markdown("### ⭐ Favorites")
            for fav in list(st.session_state.favorites):
                if st.button(f"📌 {fav}", key=f"fav_{fav}"):
                    st.session_state.selected_food = fav
                    st.rerun()

    if st.session_state.selected_food:
        _detail_view(db)
        return

    c1, c2 = st.columns(2)
    term = c1.text_input("🔍 Search by name")
    category = c2.selectbox("Filter by category", ["All"] + list(FOOD_CATEGORIES.keys()))

    view = db.copy()
    if term:
        view = view[view["Food"].str.contains(term, case=False)]
    if category != "All":
        view = view[view["Category"] == category]

    if view.empty:
        st.warning("No foods match your search.")
        return

    st.markdown(f"#### Found {len(view)} items")
    cols = st.columns(3)
    for i, (_, row) in enumerate(view.iterrows()):
        with cols[i % 3]:
            _food_card(row)
            if st.button("View details", key=f"sel_{row['Food']}", use_container_width=True):
                st.session_state.selected_food = row["Food"]
                st.rerun()
