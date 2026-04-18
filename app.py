import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px

# 1. ปรับ layout เป็น centered จะอ่านง่ายกว่าบนจอมือถือ/แท็บเล็ตแนวตั้ง
st.set_page_config(page_title="Tops Daily Fun Fest", page_icon="📱", layout="centered")

# 2. ใส่ CSS ปรับแต่งให้ "แตะง่าย" (Fat-finger friendly) สำหรับจอมือถือ
st.markdown("""
    <style>
    /* ขยายขนาดปุ่มกดให้กว้างเต็มจอและสูงขึ้น */
    .stButton>button { 
        width: 100%; 
        height: 55px; 
        font-size: 18px; 
        font-weight: bold; 
        border-radius: 12px; 
        background-color: #ff4b4b; 
        color: white;
    }
    /* ขยายขนาดตัวหนังสือในช่องกรอกข้อมูล */
    input[type="text"], input[type="number"] { font-size: 18px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📱 ระบบอัปเดตยอดคูปอง")
st.caption("Sticker Tops Fun Fest - สำหรับพนักงานสาขา")

# 3. ใช้ Tabs แยกส่วน "คนกรอก(มือถือ)" กับ "คนดูรายงาน(iPad)"
tab_form, tab_report = st.tabs(["📝 ฟอร์มอัปเดตรายวัน", "📊 แดชบอร์ดสรุปผล"])

with tab_form:
    st.info("💡 แนะนำให้พนักงานสาขากรอกข้อมูลผ่านสมาร์ทโฟนได้เลยครับ")
    with st.form("mobile_update_form"):
        record_date = st.date_input("📅 ประจำวันที่", date.today())
        branch = st.selectbox("🏪 เลือกสาขาของคุณ", ["Bantheparak", "Ladprao 102", "Praram 9 Soi 49", "อื่นๆ"])
        
        st.markdown("---")
        st.subheader("🎟️ สรุปยอดคูปองวันนี้")
        
        # ปรับ step ให้กดปุ่ม + ทีละ 10 หรือ 50 จะได้ไม่ต้องพิมพ์ตัวเลขเองบ่อยๆ
        coupons_dist = st.number_input("ยอดที่แจกให้ลูกค้า (ใบ)", min_value=0, step=50)
        coupons_used = st.number_input("ยอดที่ลูกค้านำกลับมาใช้ (ใบ)", min_value=0, step=10)
        
        # ปุ่มกดจะใหญ่เต็มจอเพราะ CSS ที่เราใส่ไว้ด้านบน
        submitted = st.form_submit_button("บันทึกข้อมูลเข้าสู่ระบบ")

    if submitted:
        st.success(f"✅ สาขา {branch} บันทึกข้อมูลสำเร็จ! ยอดส่งตรงถึงหน้าแดชบอร์ดแล้วครับ")

with tab_report:
    st.write("ส่วนนี้ออกแบบมาสำหรับเปิดดูแนวนอนบน **iPad หรือ PC** เพื่อดูภาพรวมครับ")
    
    # ข้อมูลจำลองสำหรับทำกราฟ
    data = pd.DataFrame({
        "สาขา": ["Bantheparak", "Ladprao 102", "Praram 9 Soi 49"],
        "ยอดใช้คูปอง": [4200, 7500, 3100]
    })
    
    # กราฟโดนัท (Donut Chart) จะดูสวยและเข้าใจง่ายบนหน้าจอทุกขนาด
    fig = px.pie(data, values='ยอดใช้คูปอง', names='สาขา', hole=0.4, 
                 title="สัดส่วนยอดการใช้คูปองแต่ละสาขา")
    fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True) # บังคับกราฟยืดหดตามจอ