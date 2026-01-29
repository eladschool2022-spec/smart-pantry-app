import streamlit as st
import requests
import base64
from PIL import Image
import io

# הגדרות עיצוב
st.set_page_config(page_title="SmartPantry AI", page_icon="🍎")
st.title("🍎 SmartPantry: המקרר החכם שלי")

# סרגל צד להגדרות
st.sidebar.header("הגדרות")
api_key = st.sidebar.text_input("הכנס Google API Key:", type="password")

# העלאת תמונה
uploaded_file = st.file_uploader("צלם או העלה תמונה של המקרר", type=["jpg", "jpeg", "png"])

def process_image(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="המקרר שלך", use_container_width=True)
    
    if st.button('נתח מוצרים והצע מתכונים'):
        if not api_key:
            st.error("אנא הכנס מפתח API בסרגל הצד")
        else:
            try:
                with st.spinner('ה-AI בודק מה יש במקרר...'):
                    # הכנת התמונה
                    base64_img = process_image(image)
                    
                    # כתובת ה-API הישירה
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    
                    # הבקשה ל-AI
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": "נתח את התמונה בעברית. צור טבלה עם: שם המוצר, כמות, וכמה ימים נותרו לשימוש. בסוף הצע 2 מתכונים קלים לביצוע ממה שיש."},
                                {"inline_data": {"mime_type": "image/jpeg", "data": base64_img}}
                            ]
                        }]
                    }
                    
                    response = requests.post(url, json=payload)
                    data = response.json()
                    
                    if "candidates" in data:
                        answer = data['candidates'][0]['content']['parts'][0]['text']
                        st.success("הנה מה שמצאתי:")
                        st.markdown(answer)
                    else:
                        st.error("שגיאה מהשרת של גוגל. וודא שהמפתח תקין.")
                        st.write(data) # מציג את השגיאה אם יש כזו
            except Exception as e:
                st.error(f"קרתה שגיאה: {e}")
