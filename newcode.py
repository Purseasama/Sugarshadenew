import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image
import csv
import requests
import time, hmac, hashlib, uuid, json, re
from urllib.parse import urlparse
st.write("Secrets currently loaded:", list(st.secrets.keys()))

# Trello credentials
TRELLO_API_KEY = st.secrets["TRELLO_API_KEY"]
TRELLO_TOKEN = st.secrets["TRELLO_TOKEN"]
TRELLO_LIST_ID = "6788e230bfdafa8cb62ad43c"

# Lalamove credentials
LALAMOVE_API_KEY = st.secrets["LALAMOVE_API_KEY"]
LALAMOVE_API_SECRET = st.secrets["LALAMOVE_API_SECRET"]
country = "TH"
base_url = "https://rest.sandbox.lalamove.com"


# Cake shop details
SHOP_NAME  = "Sugar Shade"
SHOP_PHONE = "083-753-4373"
SHOP_ADDR  = "เทอดไท 77, กรุงเทพมหานคร"
SHOP_LAT   = 13.709679
SHOP_LNG   = 100.441462

# Trello function
def create_trello_card_with_image(api_key, token, list_id, title, description, main_image=None, extra_images=None):
    # Create card
    create_url = "https://api.trello.com/1/cards"
    query = {
        'key': api_key,
        'token': token,
        'idList': list_id,
        'name': title,
        'desc': description
    }
    response = requests.post(create_url, params=query)
    if response.status_code != 200:
        return False

    card_id = response.json()['id']

    # Attach main image (design or custom)
    if main_image:
        with open(main_image, 'rb') as f:
            files = {'file': f}
            attach_url = f"https://api.trello.com/1/cards/{card_id}/attachments"
            attach_query = {'key': api_key, 'token': token}
            requests.post(attach_url, files=files, params=attach_query)

    # Attach reference photos (if any)
    if extra_images:
        for photo in extra_images:
            attach_url = f"https://api.trello.com/1/cards/{card_id}/attachments"
            attach_query = {'key': api_key, 'token': token}
            files = {'file': (photo.name, photo.getbuffer())}
            requests.post(attach_url, files=files, params=attach_query)

    return card_id

# Lalamove function

def _now_ms(): return str(int(time.time()*1000))

def _build_signature(secret, method, url, body, ts_ms):
    parsed = urlparse(url)
    path = parsed.path
    payload = json.dumps(body, separators=(",", ":")) if body else ""
    to_sign = f"{ts_ms}\r\n{method.upper()}\r\n{path}\r\n{payload}"
    return hmac.new(secret.encode("utf-8"), to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

def _headers(method, url, body):
    ts = _now_ms()
    sig = _build_signature(LALAMOVE_API_SECRET, method, url, body, ts)
    return {
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json",
        "X-Request-ID": str(uuid.uuid4()),
        "X-LLM-Country": LALAMOVE_COUNTRY,
        "Authorization": f"hmac {LALAMOVE_API_KEY}:{ts}:{sig}",
    }

def lalamove_request(method, path, body=None):
    url = f"{LALAMOVE_BASE_URL}{path}"
    resp = requests.request(method, url, headers=_headers(method, url, body),
                            data=json.dumps(body) if body else None, timeout=30)
    try:
        data = resp.json()
    except Exception:
        resp.raise_for_status()
        return None
    if not resp.ok:
        raise RuntimeError(json.dumps({"status": resp.status_code, "error": data}, ensure_ascii=False))
    return data

def lalamove_get_quotation(stops, service_type, schedule_type="ASAP", pickup_iso=None):
    payload = {
        "serviceType": service_type,
        "stops": stops,
        "schedule": {"type": schedule_type, **({"pickupTime": pickup_iso} if pickup_iso else {})},
    }
    return lalamove_request("POST", "/v3/quotations", payload)

def parse_coords_from_text(text: str):
    if not text: return (None, None)
    m = re.search(r"(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)", text)
    return (float(m.group(1)), float(m.group(2))) if m else (None, None)

def choose_service_type(delivery_option: str, cake_size: str):
    if delivery_option == "รถมอเตอร์ไซต์":
        return "MOTORCYCLE"
    return "CAR"  # default



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
customer_name = st.text_input("💌 ชื่อลูกค้า", placeholder="ใส่ชื่อเดียวกับชื่อ Line/FB/IG ตามช่องทางที่สั่ง")
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
col1, _ = st.columns(2)

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
        "Cake Angel": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/Cakeangel_new.jpg",
        "Cake Super strawberry": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20super%20strawberry.jpg",
        "Cake Floral": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cake%20floral.jpg",
        "Cake Animal Lover(Head)": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/animal_head.jpg",
        "Cake Animal Lover(Body)": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/animal_body.jpg",
        "Cake Animal Lover(Duo)": "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/animal_duo.jpg",
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
        if st.button("Cake Animal Lover(Head)", key="Cake Animal Lover(Head)"):
            st.session_state.cake_design = "Cake Animal Lover(Head)"
        st.image(cake_designs["Cake Animal Lover(Head)"], use_container_width=True)
    
    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("Cake Animal Lover(Body)", key="Cake Animal Lover(Body)"):
            st.session_state.cake_design = "Cake Animal Lover(Body)"
        st.image(cake_designs["Cake Animal Lover(Body)"], use_container_width=True)

    with col8:
        if st.button("Cake Animal Lover(Duo)", key="Cake Animal Lover(Duo)"):
            st.session_state.cake_design = "Cake Animal Lover(Duo)"
        st.image(cake_designs["Cake Animal Lover(Duo)"], use_container_width=True)

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
        cake_filling = st.selectbox("ไส้ (ซอส):", ["🍓 สตรอเบอร์รี่", "🍫 ช็อคโกแลต"])
        cake_size = st.selectbox("ขนาด:", ["0.25 ปอนด์","0.5 ปอนด์", "1 ปอนด์", "1.5 ปอนด์", "2 ปอนด์"])
        cake_color_options = ["ชมพู", "ฟ้า", "ขาว", "ดำ", "ม่วง", "ตามแบบที่แนบ","สีอื่นๆโปรดระบุ"]
        cake_color_choice = st.selectbox("สีเค้ก:", cake_color_options)
        if cake_color_choice == "สีอื่นๆโปรดระบุ":
            custom_cake_color = st.text_input("สีอื่นๆ")
            cake_color = custom_cake_color if custom_cake_color else "Not Specified"
        else:
            cake_color = cake_color_choice
        cake_text = st.text_input("ข้อความที่ต้องการเขียนบนเค้ก/ฐาน", placeholder="เช่น Happy birthday!")
        cake_specification = st.text_input("บรีฟอื่นๆ (หากมี)", placeholder="เช่น ขอเปลี่ยนจากโบว์สีแดงเป็นสีดำ")
        
        # Allow multiple photo uploads
        uploaded_photos = st.file_uploader("เพิ่มรูปภาพเพิ่มเติม (หากมี)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        # Display uploaded images
        if uploaded_photos:
            st.write("Uploaded Images:")
            for photo in uploaded_photos:
                st.image(photo, caption=photo.name, use_container_width=True)

# Selecting package
    st.markdown("<div class='box'><span class='title'> 🧊 ถุงเก็บความเย็น </span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        ice_bag = st.radio("ถุงเก็บความเย็นและไอซ์แพค (ถุงละ 15 บาท):", ["รับ", "❌ไม่รับ"])
    with col2:
        icebag_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/icebag.jpg"
        st.image(icebag_image, use_container_width=True)
        
    # Selecting candle
    st.markdown("<div class='box'><span class='title'>🕯️เทียน </span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        candle_type = st.radio("เทียน (แท่งละ 10 บาท):", ["เทียนเกลียว", "เทียนสั้นสีชมพู", "❌ไม่รับเทียน"])
        num_candles = st.slider("จำนวน (แท่ง):", min_value=1, max_value=10, value=1) if candle_type != "ไม่รับเทียน" else 0
    with col2:
        candle_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/candlesnew.jpg"
        st.image(candle_image, use_container_width=True)

    # Selecting card
    st.markdown("<div class='box'><span class='title'>💌การ์ด </span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        card_type = st.radio("การ์ดเขียนมือ (ใบละ 10 บาท):", ["รับ", "❌ไม่รับ"])
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
        match_box = st.radio("ไม้ขีดไฟ (กล่องละ 15 บาท):", ["รับ", "❌ไม่รับ"])
    with col2:
        matchbox_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/matchboxnew.jpg"
        st.image(matchbox_image, use_container_width=True)

        # Selecting cake knife
    st.markdown("<div class='box'><span class='title'>🔪มีดตัดเค้ก</span></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        cake_knife = st.radio("มีดตัดเค้ก (อันละ 10 บาท):", ["รับ", "❌ไม่รับ"])
    with col2:
        cakeknife_image = "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/cakeknife.jpg"
        st.image(cakeknife_image, use_container_width=True)

    # Delivery details
    st.markdown("<div class='box'><span class='title'>🚗 ข้อมูลการจัดส่ง </span></div>", unsafe_allow_html=True)
    delivery_image= "https://raw.githubusercontent.com/Purseasama/Sugarshadenew/main/delivery.jpg"  
    st.image(delivery_image, use_container_width=True)

    delivery_date = st.date_input("วันรับเค้ก")
    delivery_time = st.time_input("เวลาส่งเค้ก")
    st.caption("เวลาที่ระบุคือเวลาที่ออกจากร้าน ทางร้านเรียกรถก่อนเวลาประมาณ 15 นาที โปรดเช็คระยะทางและเวลาเดินทาง")
    delivery_option = st.radio("วิธีส่ง:", ["มารับเอง", "รถมอเตอร์ไซต์", "รถยนต์"])
    
    if delivery_option == "มารับเอง":
        with st.expander("📍พิกัด"):
            st.markdown(
                """
                เทอดไท 77 ร้านอยู่ตรงข้ามแยก 2 

                <div style="border: 1px solid #d3cce3; border-radius: 8px; padding: 8px 12px; background-color: #f3eaff; display: inline-block; margin: 8px 0;">
                    <a href="https://maps.app.goo.gl/5F2ji976fgUMaFxN6?g_st=com.google.maps.preview.copy" target="_blank" style="text-decoration: none; color: black; font-weight: 500;">
                        📍 Google Maps
                     </a>
                </div> 

                **📞 โทร:** 083-753-4373  

                สามารถเข้ามารับได้เองหรือเรียกรถมารับ  
                
                ❌หากต้องการให้ทางร้านเรียกรถให้ กรุณาเลือกวิธีจัดส่งอื่น (มอเตอร์ไซต์/รถยนต์)
                """,
                unsafe_allow_html=True
        )
            

    if delivery_option == "รถมอเตอร์ไซต์":
        st.warning("""
            ⛔️ โปรดเลือกการส่งให้เหมาะสมกับขนาด ระยะทาง และการจราจร ทางร้านไม่รับผิดชอบเค้กที่เสียหายจากการขนส่งในทุกกรณีนะคะ
            1. เค้ก 1 ปอนด์ขึ้นไปไม่แนะนำส่งด้วยรถมอเตอร์ไซต์
            2. ไม่แนะนำส่งในระยะทางเกิน 10 กม.
            3. ไม่แนะนำส่งงาน 3D หรือที่มีความสูง
            4. ไม่แนะนำส่งงานผลไม้
        """)
    delivery_location = st.text_input("สถานที่ส่ง (หากมารับเองเว้นไว้)", placeholder="สามารถใส่เป็น Google Link หรือชื่อสถานที่ได้")
    

    # Checkbox ถามว่า "ให้ส่งให้ผู้อื่นใช่ไหม"
    send_to_other = st.checkbox("คลิ้กปุ่มนี้หากผู้รับเค้กไม่ใช่ผู้สั่ง (สั่งให้บุคคลอื่น)")
    # ถ้าเลือก ให้แสดงช่องกรอกข้อมูลผู้รับ
    if send_to_other:
        st.markdown(
            "<span style='color:#C71585;'>📦 กรุณาระบุข้อมูลผู้รับเพื่อจัดส่ง</span>",
            unsafe_allow_html=True
        )
        receiver_name = st.text_input("👤 ชื่อผู้รับ")
        receiver_phone = st.text_input("📞 เบอร์โทรผู้รับ")
    else:
        receiver_name = customer_name
        receiver_phone = phone_number

    from datetime import datetime
    if st.button("✅ ยืนยันคำสั่งซื้อ"):
        st.markdown(
    """
    <div style="background-color: black; color: white; padding: 10px; border-radius: 5px; font-size: 16px;">
        <strong>ข้อมูลของคุณเข้าระบบแล้ว</strong><br>
        รอแอดมินส่งข้อมูลเพื่อยืนยันและรวมยอดชำระเงินในแชท
    </div>
    """,
    unsafe_allow_html=True
)
        #Add timestamp
        timestamp = datetime.now().strftime("%d/%m/%y")

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
    - วันที่สั่งซื้อ: {timestamp}

    🎂 ประเภทเค้ก: {st.session_state.cake_type}
    - 🎨 แบบเค้ก: {st.session_state.cake_design}
    - เนื้อเค้ก: {cake_base}
    - ไส้: {cake_filling}
    - ขนาด: {cake_size}
    - สีเค้ก: {cake_color}
    - ข้อความ: {cake_text}
    - บรีฟอื่นๆ: {cake_specification}

    🕯️ เทียนและการ์ด
    - ถุงเก็บความเย็น : {ice_bag}
    - เทียน : {candle_type} {num_candles} แท่ง
    - การ์ด : {card_type} {card_text}
    - ไม้ขีดไฟ : {match_box}
    - มีดตัดเค้ก : {cake_knife}

    🚗 ข้อมูลการจัดส่ง
    - วันรับเค้ก: {delivery_date.strftime('%d/%m/%y')} ({delivery_date.strftime('%A')})
    - เวลาส่ง: {delivery_time}
    - วิธีจัดส่ง: {delivery_option}
    - สถานที่รับ: {delivery_location}
    - ผู้รับ : {receiver_name} {receiver_phone}
     """  


        # ✅ Show Order Summary in Streamlit
        st.success(order_summary)

        # ✅ Always Display the Selected Cake Image in Order Summary
        if selected_cake_image:
            st.image(selected_cake_image, caption="🎂 ดีไซน์เค้กที่เลือก", use_container_width=True)
        
        # Format delivery date and time for Trello card title
        delivery_datetime_str = f"{delivery_date.strftime('%d/%m/%y')}-{delivery_time.strftime('%H.%M')}"
        trello_title = f"{delivery_datetime_str}-{delivery_option}-{customer_name}-{order_channel}"

        import tempfile
        from urllib.request import urlretrieve

        # Handle fallback: if not custom, download design image from URL
        main_image_path = None
        if st.session_state.cake_design == "Cake Custom (แบบอื่นๆ)" and custom_cake_photo:
            main_image_path = image_path  # your local uploaded image
        else:
            design_url = cake_designs.get(st.session_state.cake_design)
            if design_url:
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                urlretrieve(design_url, tmp_file.name)
                main_image_path = tmp_file.name

        # Create Trello card with both main image and reference photos
        create_trello_card_with_image(
            api_key=TRELLO_API_KEY,
            token=TRELLO_TOKEN,
            list_id=TRELLO_LIST_ID,
            title=trello_title,
            description=order_summary,
            main_image=main_image_path,
            extra_images=uploaded_photos if uploaded_photos and len(uploaded_photos) > 0 else None
        )



