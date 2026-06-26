"""Dashboard / home — greeting, quick stats and feature tiles."""
import streamlit as st

from healthhub.styles import hero


def render(user_name: str, go_to):
    """`go_to(page_name)` switches the active nav page."""
    first = user_name.split()[0] if user_name else "there"
    hero(f"Welcome back, {first}! 👋",
         "Your all-in-one health & nutrition companion — now glass-finished.",
         pill="💎 Premium Edition")

    c1, c2, c3 = st.columns(3)
    c1.metric("Active Days", "7", "+1 day")
    c2.metric("Foods Explored", "12", "+3")
    c3.metric("Avg. Rating", "4.8", "0.2")

    st.markdown("#### Your tools")
    st.markdown(
        """
        <div class="feature-grid">
          <div class="fcard"><div class="ico">⚖️</div><h3>BMI Calculator</h3>
            <p>Track BMI, BMR & daily calorie needs.</p></div>
          <div class="fcard"><div class="ico">🍎</div><h3>Food Database</h3>
            <p>USDA-powered nutrition for 50 whole foods.</p></div>
          <div class="fcard"><div class="ico">🤖</div><h3>AI Health Coach</h3>
            <p>Personalised, evidence-based wellness advice.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    b1, b2, b3 = st.columns(3)
    if b1.button("⚖️  Open BMI Calculator", use_container_width=True):
        go_to("BMI Calculator")
    if b2.button("🍎  Open Food Database", use_container_width=True):
        go_to("Food Database")
    if b3.button("🤖  Chat with AI Coach", use_container_width=True):
        go_to("AI Health Coach")
