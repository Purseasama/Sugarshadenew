import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image

# Telegram token and ID
TELEGRAM_BOT_TOKEN = "7886819703:AAGYLfxKsaY9TVYg9kwUyj2qAB-JBiIVcTE"
TELEGRAM_CHAT_ID = "7897964568"

# LINE Notify Token 
LINE_NOTIFY_TOKEN = "cFNP09HM6p72xrzSbqeiTrXHN81WYfbL1d8Spjp3Izi"

# Function to send telegram massage and photo
def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    telegram_payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    response = requests.post(telegram_url, json=telegram_payload)
    print(response.json())  # Debugging output

def send_telegram_photo(message, image_path):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    telegram_payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    # Send text first
    requests.post(telegram_url, json=telegram_payload)

    # Send image
    if image_path:
        telegram_photo_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as photo:
            files = {"photo": photo}
            requests.post(telegram_photo_url, data={"chat_id": TELEGRAM_CHAT_ID}, files=files)

# Function to send LINE notification
def send_line_notification(message, image_path=None):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    files = {"imageFile": open(image_path, "rb")} if image_path else None
    requests.post(url, headers=headers, data=data, files=files)
# LOGO
logo_url = "https://raw.githubusercontent.com/Purseasama/Testcakeapp/main/sugarshadelogo.jpeg"

# Display the logo at the top
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{logo_url}" width="200">
    </div>
    """,
    unsafe_allow_html=True,
)

# Modernized UI with Styled Sections
st.markdown("""
<style>
    .box {
        border: 1px solid #ddd;
        padding: 12px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .title {
        font-size: 20px;
        font-weight: bold;
        color: Black;
    }
</style>
""", unsafe_allow_html=True)

# Customer Information Section
st.markdown("<div class='box'><span class='title'>📋 ข้อมูลลูกค้า</span></div>", unsafe_allow_html=True)
customer_name = st.text_input("💌 ชื่อลูกค้า", placeholder="ใส่ชื่อเดียวกับชื่อ Line")
phone_number = st.text_input("📞 เบอร์โทรศัพท์", max_chars=15, placeholder=" XXX-XXX-XXXX")
order_channel = st.radio("📲 ช่องทางสั่ง", ["Line", "Facebook", "Instagram"], horizontal=True)

# Cake Type Selection
st.markdown("<div class='box'><span class='title'>🎂 ประเภทเค้ก</span></div>", unsafe_allow_html=True)
cake_type = st.radio("กรุณาเลือกประเภทเค้ก", ["เค้กปอนด์ 🎂", "เค้กชิ้น 🍰"], horizontal=True)

if cake_type == "เค้กปอนด์ 🎂":
    st.markdown("<div class='box'><span class='title'>🎂 เค้กปอนด์</span></div>", unsafe_allow_html=True)
    cake_base = st.selectbox("เนื้อเค้ก:", ["วานิลลา", "ช็อคโกแลต"])
    cake_filling = st.selectbox("ไส้:", ["🍓 สตรอเบอร์รี่", "🍫 ช็อคโกแลต", "🫐 บลูเบอร์รี่", "🍯 คาราเมล"])
    cake_size = st.selectbox("ขนาด:", ["0.5 ปอนด์", "1 ปอนด์", "1.5 ปอนด์"])
    
    cake_color_options = ["ชมพู", "ฟ้า", "ขาว", "ดำ", "ม่วง", "สีอื่นๆโปรดระบุ"]
    cake_color_choice = st.selectbox("สีเค้ก:", cake_color_options)
    if cake_color_choice == "สีอื่นๆโปรดระบุ":
        custom_cake_color = st.text_input("สีอื่นๆ")
        cake_color = custom_cake_color if custom_cake_color else "Not Specified"
    else:
        cake_color = cake_color_choice
        
    cake_text = st.text_input("ข้อความที่ต้องการเขียนบนเค้ก/ฐาน", placeholder="เช่น Happy birthday!")
    cake_specification = st.text_input("บรีฟอื่นๆ (หากมี)", placeholder="เช่น ขอเปลี่ยนจากโบว์สีแดงเป็นสีดำ")

    # Upload Cake Reference Image
    uploaded_file = st.file_uploader("📷 อัพโหลดภาพตัวอย่างเค้ก (ถ้ามี)", type=["jpg", "png", "jpeg"])

    # Save uploaded file
    image_path = None
    if uploaded_file is not None:
        image_path = os.path.join("uploaded_images", uploaded_file.name)
        os.makedirs("uploaded_images", exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(image_path, caption="ตัวอย่างเค้ก", use_container_width=True)

    # Selecting candle
    st.markdown("<div class='box'><span class='title'>🕯️เทียน </span></div>", unsafe_allow_html=True)
    candle_type = st.radio("เทียน (แท่งละ 10 บาท):", ["เทียนเกลียว", "เทียนสั้นสีชมพู", "ไม่รับเทียน"])

    num_candles = st.slider("จำนวน (แท่ง):", min_value=1, max_value=10, value=1) if candle_type != "ไม่รับเทียน" else 0

    # Delivery details
    st.markdown("<div class='box'><span class='title'>🚗 ข้อมูลการจัดส่ง </span></div>", unsafe_allow_html=True)
    delivery_date = st.date_input("วันรับเค้ก")
    delivery_time = st.time_input("เวลารับเค้ก")
    delivery_option = st.radio("วิธีส่ง:", ["มารับเอง", "รถมอเตอร์ไซต์", "รถยนต์"])
    
    if delivery_option == "รถมอเตอร์ไซต์":
        st.warning(
            "เนื่องจากเค้กมีความละเอียดในการส่ง รบกวนลูกค้าอ่านรายละเอียดก่อนนะคะ\n"
            "การส่งเค้กของทางร้านใช้บริการจาก lalamove / bolt / grab \n"
            
            "❌ ข้อจำกัดการส่งมอเตอร์ไซต์\n"
            "1. เค้ก 1.5 ปอนด์ขึ้นไปไม่สามารถส่งด้วยมอเตอร์ไซต์ได้\n"
            "2. ไม่แนะนำส่งในระยะทางเกิน 10 กม.\n"
            "3. ไม่แนะนำส่งงาน 3D หรือที่มีความสูง\n"
            "4. ไม่แนะนำส่งงานผลไม้\n"
            "⛔️ ทางร้านไม่รับผิดชอบเค้กที่เสียหายจากการขนส่งในทุกกรณีนะคะ🙏🏻"
        )
    delivery_location = st.text_input("สถานที่ส่ง (หากมารับเองใส่ว่ามารับเอง)", placeholder="สามารถใส่เป็น Google Link หรือชื่อสถานที่ได้")
    
    # Order Confirmation Buttons
    if st.button("✅ ยืนยันคำสั่งซื้อ"):
        order_summary = f"""
💌 K.{customer_name}
- เบอร์โทร: {phone_number}
- ช่องทางสั่ง : {order_channel}

🎂 รายละเอียดเค้ก
- เนื้อเค้ก: {cake_base}
- ไส้: {cake_filling}
- ขนาด: {cake_size}
- สีเค้ก: {cake_color}
- ข้อความ: {cake_text}
- บรีฟอื่นๆ: {cake_specification}

🕯️ เทียน 
- เทียน : {candle_type} {num_candles} แท่ง

🚗 ข้อมูลการจัดส่ง
- วันรับเค้ก: {delivery_date}
- เวลา: {delivery_time}
- วิธีจัดส่ง: {delivery_option}
- สถานที่รับ: {delivery_location}
        """
        st.success(order_summary)
        if image_path:
            st.image(image_path, caption="📷 รูปตัวอย่างเค้กที่อัพโหลด", use_container_width=True)
        
        # Send text + image to Line notify
        send_line_notification(order_summary, image_path)

        # Send text + image to Telegram
        send_telegram_photo(order_summary, image_path)


elif cake_type == "เค้กชิ้น 🍰":
    st.markdown("<div class='box'><span class='title'>🍰 เค้กชิ้น</span></div>", unsafe_allow_html=True)
    num_pieces = st.selectbox("จำนวนชิ้น:", list(range(1, 101)))
    
    cake_flavors = []
    for i in range(num_pieces):
        flavor = st.selectbox(f"เลือกไส้เค้กชิ้นที่ {i+1}", ["สตรอเบอร์รี่", "บลูเบอร์รี่", "ส้ม", "เลมอน", "มะม่วง", "มะพร้าว", "ช็อคโกแลต", "คาราเมล", "บานอฟฟี่"])
        cake_flavors.append(f"{i+1}. {flavor}")
    # Packing choice for 4 or 6 pieces
    packing_option = st.radio("เลือกวิธีแพ็ค:", ["แยกชิ้น", "รวมกล่องเดียวกัน"]) if num_pieces in [4, 6] else "แยกชิ้น"

    # Selecting candle
    st.markdown("<div class='box'><span class='title'>🕯️เทียน </span></div>", unsafe_allow_html=True)
    candle_type = st.radio("เทียน (แท่งละ 10 บาท):", ["เทียนเกลียว", "เทียนสั้นสีชมพู", "ไม่รับเทียน"])

    num_candles = st.slider("จำนวน (แท่ง):", min_value=1, max_value=10, value=1) if candle_type != "ไม่รับเทียน" else 0
    
    # Delivery details
    st.markdown("<div class='box'><span class='title'>🚗 ข้อมูลการจัดส่ง </span></div>", unsafe_allow_html=True)
    delivery_date = st.date_input("วันรับเค้ก")
    delivery_time = st.time_input("เวลารับเค้ก")
    delivery_option = st.radio("วิธีส่ง:", ["มารับเอง", "รถมอเตอร์ไซต์", "รถยนต์"])
    if delivery_option == "รถมอเตอร์ไซต์":
        st.warning(
            "เนื่องจากเค้กมีความละเอียดในการส่ง รบกวนลูกค้าอ่านรายละเอียดก่อนนะคะ\n"
            "การส่งเค้กของทางร้านใช้บริการจาก lalamove / bolt / grab \n"
            
            "❌ ข้อจำกัดการส่งมอเตอร์ไซต์\n"
            "1. เค้ก 1.5 ปอนด์ขึ้นไปไม่สามารถส่งด้วยมอเตอร์ไซต์ได้\n"
            "2. ไม่แนะนำส่งในระยะทางเกิน 10 กม.\n"
            "3. ไม่แนะนำส่งงาน 3D หรือที่มีความสูง\n"
            "4. ไม่แนะนำส่งงานผลไม้\n"
            "⛔️ ทางร้านไม่รับผิดชอบเค้กที่เสียหายจากการขนส่งในทุกกรณีนะคะ🙏🏻"
        )
    delivery_location = st.text_input("สถานที่ส่ง (หากมารับเองใส่ว่ามารับเอง)", placeholder="สามารถใส่เป็น Google Link หรือชื่อสถานที่ได้")
    
    # Order Confirmation Button
    if st.button("✅ ยืนยันคำสั่งซื้อ"):
        order_summary = f"""
💌 K.{customer_name}
- เบอร์โทร: {phone_number}
- ช่องทางสั่ง : {order_channel}

🍰 รายละเอียดเค้กชิ้น
- จำนวน: {num_pieces} ชิ้น
- รสชาติ:\n{chr(10).join(cake_flavors)}
- วิธีแพ็ค: {packing_option}

🕯️ เทียน 
- เทียน : {candle_type} {num_candles} แท่ง

🚗 ข้อมูลการจัดส่ง
- วันรับเค้ก: {delivery_date}
- เวลา: {delivery_time}
- วิธีจัดส่ง: {delivery_option}
- สถานที่รับ: {delivery_location}
        """
        st.success(order_summary)
        send_line_notification(order_summary)
        send_line_oa_message(order_summary,image_url)