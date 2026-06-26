"""BMI & TDEE calculator with a glass result panel."""
import streamlit as st

from healthhub.styles import hero

_ACTIVITY = {
    "Sedentary": 1.2,
    "Light": 1.375,
    "Moderate": 1.55,
    "Active": 1.725,
    "Very Active": 1.9,
}


def render():
    hero("⚖️ BMI & TDEE Calculator", "Know your numbers — body mass index and daily calorie needs.",
         pill="📐 Precision metrics")

    with st.form("bmi_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Your name", "")
            sex = st.selectbox("Sex", ["Male", "Female", "Other"])
            age = st.number_input("Age", 10, 100, 25)
        with c2:
            height = st.number_input("Height (cm)", 100, 250, 170)
            weight = st.number_input("Weight (kg)", 30, 300, 70)
            activity = st.selectbox("Activity level", list(_ACTIVITY.keys()))
        submitted = st.form_submit_button("Calculate", use_container_width=True)

    if not submitted:
        return

    bmi = weight / ((height / 100) ** 2)
    category = ("Underweight" if bmi < 18.5 else "Normal" if bmi < 25
                else "Overweight" if bmi < 30 else "Obese")

    if sex.lower() == "male":
        bmr = 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age
    else:
        bmr = 447.593 + 9.247 * weight + 3.098 * height - 4.330 * age
    tdee = bmr * _ACTIVITY[activity]

    st.markdown(
        f"""
        <div class="glass" style="margin-top:18px;">
          <h3 style="margin-top:0;">Results for {name or 'You'}</h3>
          <div style="display:flex;gap:16px;flex-wrap:wrap;">
            <div class="fcard" style="flex:1;min-width:140px;">
              <div class="ico">📊</div><h3>{bmi:.1f}</h3><p>BMI · {category}</p></div>
            <div class="fcard" style="flex:1;min-width:140px;">
              <div class="ico">🔥</div><h3>{bmr:.0f}</h3><p>BMR kcal/day</p></div>
            <div class="fcard" style="flex:1;min-width:140px;">
              <div class="ico">⚡</div><h3>{tdee:.0f}</h3><p>TDEE kcal/day</p></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pos = min(max((bmi - 16) / (40 - 16), 0), 1) * 100
    st.markdown(
        f"""
        <div style="margin:34px 0 8px;">
          <div style="position:relative;height:18px;border-radius:999px;
               background:linear-gradient(to right,#34e7c8,#ffb347,#ff6ec7);">
            <div style="position:absolute;left:{pos}%;top:-26px;transform:translateX(-50%);
                 text-align:center;font-weight:700;color:#fff;">{bmi:.1f}
              <div style="width:0;height:0;border-left:7px solid transparent;
                   border-right:7px solid transparent;border-top:10px solid #fff;margin:2px auto 0;"></div>
            </div>
          </div>
          <div style="display:flex;justify-content:space-between;color:var(--muted);
               font-size:.8rem;margin-top:6px;">
            <span>16</span><span>18.5</span><span>25</span><span>30</span><span>40+</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
