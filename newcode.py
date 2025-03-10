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
logo_url = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/sugarshadelogo.jpeg"

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

# Initialize cake_type in session state
if "cake_type" not in st.session_state:
    st.session_state.cake_type = None

# Apply CSS styling for big buttons
st.markdown(
    """
    <style>
        .cake-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 10px;
        }
        .cake-option {
            background-color: white;
            border: 3px solid #A48DFF;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #333;
            width: 100%;
            cursor: pointer;
            transition: 0.3s;
        }
        .cake-option:hover {
            background-color: #A48DFF;
            color: white;
        }
        .cake-selected {
            background-color: #A48DFF !important;
            color: black !important;
            border: 3px solid #A48DFF;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Cake Type Selection Header
st.markdown("<div class='box'><span class='title'>🎂 ประเภทเค้ก</span></div>", unsafe_allow_html=True)

# Create layout with two big buttons
col1, col2 = st.columns(2)

# Function to update selection
def select_cake(cake):
    st.session_state.cake_type = cake

# Display big buttons for selection
with col1:
    if st.button(
        "🎂 เค้กปอนด์",
        key="pound_cake",
        use_container_width=True,
    ):
        select_cake("เค้กปอนด์ 🎂")

with col2:
    if st.button(
        "🍰 เค้กชิ้น",
        key="slice_cake",
        use_container_width=True,
    ):
        select_cake("เค้กชิ้น 🍰")

# Apply JavaScript for dynamic styling
if st.session_state.cake_type:
    selected_cake = st.session_state.cake_type
    st.markdown(
        f"""
        <script>
            var buttons = window.parent.document.querySelectorAll('button');
            buttons.forEach(btn => {{
                if (btn.innerText.includes('{selected_cake}')) {{
                    btn.style.backgroundColor = '#A48DFF';
                    btn.style.color = 'black';
                }}
            }});
        </script>
        """,
        unsafe_allow_html=True,
    )

# Ensure session state is initialized
if "cake_type" not in st.session_state:
    st.session_state.cake_type = None
if "cake_design" not in st.session_state:
    st.session_state.cake_design = None

# 🔹 Display the next section based on selection
if st.session_state.cake_type == "เค้กปอนด์ 🎂":
    st.markdown("<div class='box'><span class='title'>🎨 เลือกดีไซน์เค้ก</span></div>", unsafe_allow_html=True)

    # Cake Design Options (Images)
    cake_designs = {
        "Cake Queen": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20queen.jpg",
        "Cake Princess": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20princess.jpg",
        "Cake Angel": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20angel.jpg",
        "Cake Super strawberry": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20super%20strawberry.jpg",
        "Cake Floral": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20floral.jpg",
        "Cake Glam": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20glam.jpg",
        "Cake Strawberry lover": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20strawberry%20lover.jpg",
        "Cake Cherry": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20cherry.jpg",
        "Cake Custom (แบบอื่นๆ)": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20custom.jpg"
    }

    # Display clickable images
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Cake Queen", key="Cake Queen"):
            st.session_state.cake_design = "Cake Queen"
        st.image(cake_designs["Cake Queen"], use_container_width=True)

    with col2:
        if st.button("Cake Princess", key="Cake Princess"):
            st.session_state.cake_design = "Cake Princess"
        st.image(cake_designs["Cake Princess"], use_container_width=True)

    with col3:
        if st.button("Cake Angel", key="Cake Angel"):
            st.session_state.cake_design = "Cake Angel"
        st.image(cake_designs["Cake Angel"], use_container_width=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("Cake Super strawberry", key="Cake Super strawberry"):
            st.session_state.cake_design = "Cake Super strawberry"
        st.image(cake_designs["Cake Super strawberry"], use_container_width=True)

    with col5:
        if st.button("Cake Floral", key="Cake Floral"):
            st.session_state.cake_design = "Cake Floral"
        st.image(cake_designs["Cake Floral"], use_container_width=True)

    with col6:
        if st.button("Cake Glam", key="Cake Glam"):
            st.session_state.cake_design = "Cake Glam"
        st.image(cake_designs["Cake Glam"], use_container_width=True)
    
    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("Cake Strawberry lover", key="Cake Strawberry lover"):
            st.session_state.cake_design = "Cake Strawberry lover"
        st.image(cake_designs["Cake Strawberry lover"], use_container_width=True)

    with col8:
        if st.button("Cake Cherry", key="Cake Cherry"):
            st.session_state.cake_design = "Cake Cherry"
        st.image(cake_designs["Cake Cherry"], use_container_width=True)

    with col9:
        if st.button("Cake Custom (แบบอื่นๆ)", key="Cake Custom (แบบอื่นๆ)"):
            st.session_state.cake_design = "Cake Custom (แบบอื่นๆ)"
        st.image(cake_designs["Cake Custom (แบบอื่นๆ)"], use_container_width=True)
    
    # If "Cake Custom (แบบอื่นๆ)" is selected, allow photo upload
    if st.session_state.cake_design == "Cake Custom (แบบอื่นๆ)":
        custom_cake_photo = st.file_uploader("📷 อัพโหลดแบบเค้ก", type=["jpg", "png", "jpeg"])

        # Ensure the file is uploaded before proceeding
        if custom_cake_photo:
            # Create directory if not exists
            os.makedirs("uploaded_images", exist_ok=True)

            # Save the file
            image_path = os.path.join("uploaded_images", custom_cake_photo.name)
            with open(image_path, "wb") as f:
                f.write(custom_cake_photo.getbuffer())

            # Display uploaded image
            st.image(image_path, caption="📷 ตัวอย่างเค้กของคุณ", use_container_width=True)

            # Store image path in session state for later use
            st.session_state.custom_cake_image_path = image_path
        else:
            st.warning("📌 กรุณาอัปโหลดรูปเค้กของคุณ")  # Show warning if no file is uploaded



    st.markdown("<div class='box'><span class='title'>🎂 รายละเอียดเค้ก</span></div>", unsafe_allow_html=True)
    # Ensure session state for cake design selection
    if "cake_design" not in st.session_state:
        st.session_state.cake_design = None
    
    # Display selected cake design first
    if st.session_state.cake_design:
        st.write(f" **แบบเค้ก:** {st.session_state.cake_design}")
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

    # Selecting candle
    st.markdown("<div class='box'><span class='title'>🕯️เทียน </span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        candle_type = st.radio("เทียน (แท่งละ 10 บาท):", ["เทียนเกลียว", "เทียนสั้นสีชมพู", "ไม่รับเทียน"])
        num_candles = st.slider("จำนวน (แท่ง):", min_value=1, max_value=10, value=1) if candle_type != "ไม่รับเทียน" else 0
    with col2:
        candle_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/candlesnew.jpg"
        st.image(candle_image, use_container_width=True)

    # Selecting card
    st.markdown("<div class='box'><span class='title'>💌การ์ด </span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        card_type = st.radio("การ์ด (ใบละ 10 บาท):", ["รับ", "ไม่รับ"])
    if card_type == "รับ":
        card_text = st.text_input("ข้อความบนการ์ด:")
    else:
        card_text = "ไม่มีรับการ์ด" 
    with col2:
        card_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cardsnew.jpg"
        st.image(card_image, use_container_width=True)
    
       # Selecting matchbox
    st.markdown("<div class='box'><span class='title'>🧨ไม้ขีดไฟ </span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        match_box = st.radio("ไม้ขีดไฟ (กล่องละ 10 บาท):", ["รับ", "ไม่รับ"])
    with col2:
        matchbox_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/matchboxnew.jpg"
        st.image(matchbox_image, use_container_width=True)

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
   
    if st.button("✅ ยืนยันคำสั่งซื้อ"):
        # Determine selected cake image for display
        selected_cake_image = cake_designs.get(st.session_state.cake_design, None)

        # If "Cake Custom (แบบอื่นๆ)" is selected and an image is uploaded, save it
        image_path = None
        if st.session_state.cake_design == "Cake Custom (แบบอื่นๆ)" and custom_cake_photo:
            os.makedirs("uploaded_images", exist_ok=True)
            image_path = os.path.join("uploaded_images", custom_cake_photo.name)
            with open(image_path, "wb") as f:
                f.write(custom_cake_photo.getbuffer())
            selected_cake_image = image_path  # Use uploaded image

        # Construct Order Summary
        order_summary = f"""
    💌 K.{customer_name}
    - เบอร์โทร: {phone_number}
    - ช่องทางสั่ง : {order_channel}

    🎂 ประเภทเค้ก: {st.session_state.cake_type}
    - 🎨 แบบเค้ก: {st.session_state.cake_design}
    - เนื้อเค้ก: {cake_base}
    - ไส้: {cake_filling}
    - ขนาด: {cake_size}
    - สีเค้ก: {cake_color}
    - ข้อความ: {cake_text}
    - บรีฟอื่นๆ: {cake_specification}

    🕯️ เทียนและการ์ด
    - เทียน : {candle_type} {num_candles} แท่ง
    - การ์ด : {card_type} {card_text}
    - ไม้ขีดไฟ : {match_box}

    🚗 ข้อมูลการจัดส่ง
    - วันรับเค้ก: {delivery_date}
    - เวลา: {delivery_time}
    - วิธีจัดส่ง: {delivery_option}
    - สถานที่รับ: {delivery_location}
     """

        # ✅ Show Order Summary in Streamlit
        st.success(order_summary)

        # ✅ Always Display the Selected Cake Image in Order Summary
        if selected_cake_image:
            st.image(selected_cake_image, caption="🎂 ดีไซน์เค้กที่เลือก", use_container_width=True)

        # ✅ FIX: Send image **only if "Cake Custom (แบบอื่นๆ)" is selected**
        if st.session_state.cake_design == "Cake Custom (แบบอื่นๆ)" and image_path:
            send_line_notification(order_summary, image_path)  # Send local file
            send_telegram_photo(order_summary, image_path)  # Send local file
        else:
            send_line_notification(order_summary)  # Send text only
            send_telegram_message(order_summary)  # Send text only 



elif st.session_state.cake_type == "เค้กชิ้น 🍰":
    st.markdown("<div class='box'><span class='title'>🍰 เค้กชิ้น</span></div>", unsafe_allow_html=True)
    
    # Cake flavor images
    cake_flavor_images = {
        "สตรอเบอร์รี่": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/mini%20strawberry.jpg",
        "บลูเบอร์รี่": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/mini%20blueberry.jpg",
        "องุ่น": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/mini%20grape.jpg",
        "ส้ม": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/mini%20orange.jpg",
        "เลมอน": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/mini%20lemon.jpg",
        "บานอฟฟี่": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/mini%20banoffee.jpg",
        "ช็อคโกแลต": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/mini%20choc.jpg",
        "คาราเมล": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/mini%20caramel.jpg",
    }

    # Display cake images before selection
    st.markdown("<div class='box'><span class='title'>🖼️ เลือกรสชาติเค้ก</span></div>", unsafe_allow_html=True)

    cols = st.columns(4)  # Create columns to display images in a grid format
    
    # Display images of cake flavors
    for index, (flavor, image_url) in enumerate(cake_flavor_images.items()):
        with cols[index % 4]:  # Distribute images across columns
            st.image(image_url, caption=flavor, use_container_width=True)

    # Selection process after images are shown
    num_pieces = st.selectbox("🧁 จำนวนชิ้น:", list(range(1, 101)))

  # Allow selecting the same flavor multiple times
    cake_flavors = []
    for i in range(num_pieces):
        selected_flavor = st.selectbox(f"เลือกไส้เค้กชิ้นที่ {i+1}", list(cake_flavor_images.keys()), key=f"flavor_{i}")
        cake_flavors.append(selected_flavor) 

    # Packing choice for 4 or 6 pieces
    packing_option = st.radio("เลือกวิธีแพ็ค:", ["แยกชิ้น", "รวมกล่องเดียวกัน"]) if num_pieces in [4, 6] else "แยกชิ้น"

    # Selecting candle
    st.markdown("<div class='box'><span class='title'>🕯️เทียน </span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        candle_type = st.radio("เทียน (แท่งละ 10 บาท):", ["เทียนเกลียว", "เทียนสั้นสีชมพู", "ไม่รับเทียน"])
        num_candles = st.slider("จำนวน (แท่ง):", min_value=1, max_value=10, value=1) if candle_type != "ไม่รับเทียน" else 0
    with col2:
        candle_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/candlesnew.jpg"
        st.image(candle_image, use_container_width=True)

    # Selecting card
    st.markdown("<div class='box'><span class='title'>💌การ์ด </span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        card_type = st.radio("การ์ด (ใบละ 10 บาท):", ["รับ", "ไม่รับ"])
    if card_type == "รับ":
        card_text = st.text_input("ข้อความบนการ์ด:")
    else:
        card_text = "ไม่มีรับการ์ด" 
    with col2:
        card_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cardsnew.jpg"
        st.image(card_image, use_container_width=True)
    
       # Selecting matchbox
    st.markdown("<div class='box'><span class='title'>🧨ไม้ขีดไฟ </span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        match_box = st.radio("ไม้ขีดไฟ (กล่องละ 10 บาท):", ["รับ", "ไม่รับ"])
    with col2:
        matchbox_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/matchboxnew.jpg"
        st.image(matchbox_image, use_container_width=True)
    
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

🎂 ประเภทเค้ก: {st.session_state.cake_type}
- จำนวน: {num_pieces} ชิ้น
- รสชาติ:\n{chr(10).join(cake_flavors)}
- วิธีแพ็ค: {packing_option}

🕯️ เทียนและการ์ด
- เทียน : {candle_type} {num_candles} แท่ง
- การ์ด : {card_type} {card_text}
- ไม้ขีดไฟ : {match_box}

🚗 ข้อมูลการจัดส่ง
- วันรับเค้ก: {delivery_date}
- เวลา: {delivery_time}
- วิธีจัดส่ง: {delivery_option}
- สถานที่รับ: {delivery_location}
        """
        st.success(order_summary)
        
        send_line_notification(order_summary)
        send_telegram_message(order_summary)
        