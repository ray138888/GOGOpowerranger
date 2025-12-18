import streamlit as st
import pandas as pd

# 設定頁面資訊
st.set_page_config(page_title="2026 日本滑雪規劃師", layout="wide")

st.title("🏂 SnowPath: 2026 日本滑雪特訓規劃 (14 Days)")
st.markdown("針對目標：**Carving 技術精進** | 時間：**2026年3月**")

# 側邊欄：基本設定
st.sidebar.header("⚙️ 行程參數設定")
location = st.sidebar.selectbox("選擇滑雪區域", ["北海道 (二世谷/留壽都)", "長野 (白馬/志賀高原)"])
days = st.sidebar.slider("天數", 1, 14, 14)
currency_rate = st.sidebar.number_input("日幣匯率 (JPY to TWD)", value=0.22)

# --- TAB 1: 方案比較 ---
tab1, tab2, tab3 = st.tabs(["📊 方案比較與依據", "💰 預算計算機", "📅 14天戰略行程"])

with tab1:
    st.header("三大方案深度對比")
    
    # 建立數據
    data = {
        "比較項目": ["適合對象", "價格 (5天課程)", "師資等級", "Carving 效益", "最大缺點", "推薦指數"],
        "方案 A: 私人教練 (中文)": ["語言不通、需全天保母", "¥400,000+ (極高)", "Lv1-Lv2 (參差不齊)", "⭐⭐⭐ (看教練程度)", "太貴且教練可能不會高階刻滑", "🔴 低"],
        "方案 B: CASI Lv1 課程": ["想考證照、轉職", "¥115,000 (英文) - ¥250,000 (中文)", "Lv2-Lv3 (培訓師)", "⭐⭐ (非考試重點)", "都在練低速搓雪與教學理論", "🟡 中"],
        "方案 C: Riding Camp (推薦)": ["想變強、預算有限、滑行導向", "¥150,000 (高CP值)", "Lv3-Lv4 (考官等級)", "⭐⭐⭐⭐⭐ (專項訓練)", "全英文授課、身體疲勞度高", "🟢 高 (Best Buy)"]
    }
    df = pd.DataFrame(data)
    st.table(df)

    st.info("💡 **決策依據：** 基於 CASI 官方規範，Lv1 考試重點為「基礎搓雪 (Intermediate Sliding)」，而 Riding Camp 使用的是 Lv2/Lv3 的「刻滑標準 (Carved Turns)」。")

# --- TAB 2: 預算計算 ---
with tab2:
    st.header("💸 14天 雙人總預算預估")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("參數輸入")
        # 根據地點調整預設價格
        base_accom = 30000 if "北海道" in location else 20000
        base_lift = 9000 if "北海道" in location else 7000
        
        camp_cost = st.number_input("Camp 課程費用 (每人)", value=150000)
        accom_daily = st.number_input("雙人房每晚房價 (JPY)", value=base_accom)
        flight_cost = st.number_input("機票費用 (每人/台幣)", value=22000)
        food_daily = st.number_input("每日餐費 (每人/JPY)", value=7000)
        lift_daily = st.number_input("每日雪票 (每人/JPY)", value=base_lift)
        
    with col2:
        st.subheader("計算結果 (每人)")
        
        # 計算邏輯
        total_accom_jpy = (accom_daily * (days - 1)) / 2
        total_lift_jpy = lift_daily * (days - 2) # 扣除頭尾移動日
        total_food_jpy = food_daily * days
        total_camp_jpy = camp_cost
        
        total_jpy = total_accom_jpy + total_lift_jpy + total_food_jpy + total_camp_jpy
        total_twd = (total_jpy * currency_rate) + flight_cost
        
        st.metric("每人總花費 (TWD)", f"${int(total_twd):,}")
        st.write(f"🇯🇵 日幣總支出: ¥{int(total_jpy):,}")
        
        # 圓餅圖數據
        cost_data = pd.DataFrame({
            "項目": ["住宿", "雪票", "餐飲", "課程(Camp)", "機票(TWD換算)"],
            "金額(TWD)": [
                total_accom_jpy * currency_rate,
                total_lift_jpy * currency_rate,
                total_food_jpy * currency_rate,
                total_camp_jpy * currency_rate,
                flight_cost
            ]
        })
        st.bar_chart(cost_data.set_index("項目"))

# --- TAB 3: 行程規劃 ---
with tab3:
    st.header("📅 14天 分級特訓行程表")
    
    st.markdown("""
    **核心策略：** * 🟢 **你 (綠線S)：** 參加 Intermediate Camp -> 目標紅線S
    * ⚫ **朋友 (黑線S)：** 參加 Advanced Carving Camp -> 目標高速 Carving
    """)
    
    schedule = {
        "Day": [f"Day {i}" for i in range(1, 15)],
        "主題": [
            "抵達 & 移動", "暖身日 (Warm up)", "Camp Day 1 (基礎)", "Camp Day 2 (進階)", 
            "Camp Day 3 (應用)", "Camp Day 4 (動態)", "Camp Day 5 (結業)", "🛌 完全休息日",
            "自主練習 (模仿)", "自主練習 (挑戰)", "互相錄影日", "半日滑 / 觀光", "Fun Run 驗收", "回程"
        ],
        "重點提示": [
            "入住、租裝備", "適應日本雪況，找回腳感", "分班上課：你修站姿 / 他修細節", "你練膽量 / 他練發力",
            "你練紅線穩定 / 他練施壓", "你練刃咬雪 / 他練 Cross-under", "驗收成果 & 影片分析", "肌肉修復，去泡溫泉",
            "朋友帶你滑，模仿他的新動作", "嘗試更陡的坡 / 更快的速度", "拍攝對比影片 (Day2 vs Day11)", "保留體力，下午逛街",
            "享受滑雪，不練功了！", "前往機場"
        ]
    }
    
    st.dataframe(pd.DataFrame(schedule), hide_index=True, use_container_width=True)
    
    st.warning("⚠️ 注意：3月的日本下午容易出現思樂冰 (Slush)，建議練功集中在 08:30 - 12:30 硬雪時段。")

# Footer
st.markdown("---")
st.caption("Designed by Gemini for 2026 Ski Trip Planning")
