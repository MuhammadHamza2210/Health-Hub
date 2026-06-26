"""Groq-powered AI health coach with an offline intelligent fallback."""
import requests

from healthhub.config import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL

SYSTEM_PROMPT = """You are an expert AI Health Coach with certifications in nutrition, \
fitness, sleep science, and mental wellness. Provide:
1. Evidence-based, accurate health information
2. Personalized, practical advice
3. An encouraging and supportive tone
4. Clear explanations without medical jargon
5. Safety disclaimers when appropriate
6. Specific action steps
7. Follow-up questions to understand better
Always remind users to consult healthcare professionals for medical issues."""


def coach_ready() -> bool:
    return bool(GROQ_API_KEY)


def get_ai_response(user_input, chat_history):
    """Call Groq; fall back to a smart canned response on any failure."""
    if not GROQ_API_KEY:
        return get_intelligent_fallback(user_input)
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in chat_history[-8:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": GROQ_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9,
        }
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        return get_intelligent_fallback(user_input)
    except Exception:
        return get_intelligent_fallback(user_input)


def get_intelligent_fallback(user_input: str) -> str:
    q = user_input.lower()
    if any(w in q for w in ["diet", "food", "eat", "nutrition", "calorie", "weight", "protein"]):
        return """🥗 **Nutrition Advice:**
Based on your question about nutrition, here's what I recommend:
• Focus on whole, unprocessed foods
• Include plenty of colorful fruits and vegetables
• Choose lean proteins like chicken, fish, beans, and tofu
• Stay hydrated with water throughout the day
• Practice portion control and mindful eating

*For specific medical conditions, please consult a registered dietitian or doctor.*"""
    if any(w in q for w in ["exercise", "workout", "gym", "fitness", "muscle", "cardio"]):
        return """💪 **Fitness Guidance:**
• Aim for 150 minutes of moderate exercise per week
• Combine cardio and strength training
• Start slow and progress gradually
• Pick activities you enjoy to stay consistent
• Prioritise rest and recovery days

*Always warm up and listen to your body.*"""
    if any(w in q for w in ["sleep", "tired", "energy", "insomnia", "rest"]):
        return """😴 **Sleep Optimization:**
• Aim for 7–9 hours of quality sleep nightly
• Keep consistent sleep/wake times
• Create a dark, cool, quiet bedroom
• Limit screens an hour before bed
• Build a relaxing wind-down routine

*Chronic sleep issues may need medical consultation.*"""
    if any(w in q for w in ["stress", "anxiety", "mental", "mind", "relax", "meditate"]):
        return """🧠 **Mental Wellness:**
• Practice slow, deep breathing
• Try 5 minutes of mindfulness daily
• Stay physically active
• Nurture social connections
• Journal your thoughts

*Serious concerns should be discussed with a mental health professional.*"""
    return """🤖 **Health Coach:**
I can help with nutrition, fitness, sleep, stress management, and general wellness.
Tell me a bit more about your goal or concern and I'll give you evidence-based,
practical guidance. 🌟"""
