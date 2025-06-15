import pyttsx3
import streamlit as st
from googletrans import Translator
import pandas as pd
import pickle
from fertilizer_logic import recommend_fertilizer
import os
from PIL import Image
from gtts import gTTS
import tempfile

# Load model and data
model = pickle.load(open("crop_model.pkl", "rb"))
market_data = pd.read_csv("market_data.csv")
market_data.columns = market_data.columns.str.strip().str.lower()

st.title("🌾 Smart Agriculture Advisor")
lang = st.selectbox("🌐 Choose Language", ["English", "Telugu", "Hindi"])

# Input Fields
n = st.number_input("Nitrogen (N)")
p = st.number_input("Phosphorous (P)")
k = st.number_input("Potassium (K)")
temp = st.number_input("Temperature (°C)")
humidity = st.number_input("Humidity (%)")
ph = st.number_input("pH level")
rainfall = st.number_input("Rainfall (mm)")

if st.button("Recommend Crop"):
    # 1. Predict Crop
    prediction = model.predict([[n, p, k, temp, humidity, ph, rainfall]])[0]
    crop_info = f"The recommended crop is {prediction}."
    st.success(crop_info)

    # Crop Image
    image_path = os.path.join("crop_images", f"{prediction.lower()}.jpg")
    if os.path.exists(image_path):
        st.image(Image.open(image_path), caption=prediction.capitalize(), use_column_width=True)
    else:
        st.warning("No image found for this crop.")

    # 2. Fertilizer Suggestions
    ferts = recommend_fertilizer(n, p, k)
    fert_text = "Recommended fertilizers are: " + ", ".join(ferts) + "."
    st.info("Fertilizer Suggestions:")
    for f in ferts:
        st.write(f"- {f}")

    # 3. Market Price Info
    prices = market_data[market_data["crop"].str.lower() == prediction.lower()]
    if not prices.empty:
        row = prices.iloc[0]
        price = row.get("price", "not available")
        market = row.get("market", "an unknown market")
        price_info = f"The market price is ₹{price} per quintal in {market}."
        st.info("📊 Market Price Info:")
        st.write(prices)
    else:
        price_info = "Market price data is not available."
        st.warning(price_info)

    # Combined Output for Voice
    full_text = f"{crop_info} {fert_text} {price_info}"

    # 4. Multilingual Voice Output
    translator = Translator()
    try:
        if lang == "English":
            engine = pyttsx3.init()
            engine.say(full_text)
            engine.runAndWait()
        else:
            dest_lang = "te" if lang == "Telugu" else "hi"
            translated_text = translator.translate(full_text, src="en", dest=dest_lang).text
            st.success(translated_text)

            # gTTS audio playback
            tts = gTTS(text=translated_text, lang=dest_lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                tts.save(tmpfile.name)
                st.audio(tmpfile.name, format="audio/mp3")
    except Exception as e:
        st.error(f"Audio generation failed: {e}")

