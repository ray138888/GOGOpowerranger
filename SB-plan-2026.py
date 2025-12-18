import streamlit as st
import pandas as pd

# --- 1. 頁面設定 ---
# 使用 centered 佈局在手機上閱讀體驗較好，但為了容納電腦版資訊，我們用 wide 搭配 columns
st.set_page_config(page_title="2026 日本滑雪規劃師", layout="wide", page_icon="🏂")

# 自定義 CSS 來優化手機版體驗 (隱藏不必要的留白，加大字體)
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; }
    div[data-testid="stExpander"] div[role="button"] p { font-size: 1.1rem; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

st.title("🏂 SnowPath: 2026 日本滑雪特訓")
st.caption("RWD Mobile-First Edition | 時間：2026年3月")

# --- 側邊欄：全域設定 ---
with st.sidebar:
    st.header("⚙️ 設定")
    location = st.selectbox("📍 選擇區域", ["北海道 (二世谷/留壽都)", "長野 (白馬/志賀高原)"])
    days = st.slider("📅 天數", 5, 14, 14)
    currency_rate = st.number_input("💱 匯率 (JPY>TWD)", value=0.22, step=0.01)
    st.divider()
    st.info(f"目前設定：{location} / {days}天")

# --- TAB 分頁設定 ---
tab1, tab2, tab3 = st.tabs(["📊 方案比較", "💰 預算計算", "📅 每日行程"])

# ==========================================
# TAB 1: 方案比較 (RWD 優化：表格變卡片)
# ==========================================
with tab1:
    st.markdown("### 🏆 三大方案深度對比")
    st.caption("手機版自動切換為卡片模式，電腦版自動並排")

    # 定義資料
    plans = [
        {
            "name": "方案 A: 私人教練 (中文)",
            "icon": "🔴",
            "price": "¥400,000+",
            "suit": "語言不通、需全天保母",
            "pros": "溝通無障礙、服務好",
            "cons": "價格極高、教練程度參差不齊",
            "star": "⭐⭐⭐",
            "rec": "低"
        },
        {
            "name": "方案 B: CASI Lv1 課程",
            "icon": "🟡",
            "price": "¥115k - ¥250k",
            "suit": "想考證照、轉職",
            "pros": "獲得國際證照、基礎紮實",
            "cons": "重點在低速搓雪，非Carving",
            "star": "⭐⭐",
            "rec": "中"
        },
        {
            "name": "方案 C: Riding Camp",
            "icon": "🟢",
            "price": "¥150,000 (Best Buy)",
            "suit": "預算有限、想變強",
            "pros": "高CP值、考官級師資、專練刻滑",
            "cons": "全英文授課、體能消耗大",
            "star": "⭐⭐⭐⭐⭐",
            "rec": "高"
        }
    ]

    # 使用 columns 來做 RWD
    # 在電腦上是 3 欄並排，在手機上 Streamlit 會自動把它們變成 1 欄堆疊 (Stack)
    cols = st.columns(3)

    for i, plan in enumerate(plans):
        with cols[i]:
            # 使用 container 加上 border 形成卡片視覺
            with st.container(border=True):
                st.subheader(f"{plan['icon']} {plan['name']}")
                st.markdown(f"**💰 價格：** `{plan['price']}`")
                st.markdown(f"**🎯 對象：** {plan['suit']}")
                
                # 使用 expander 收納細節，讓手機版面不雜亂
                with st.expander("查看優缺點與評價", expanded=(i==2)): # 預設展開推薦的方案
                    st.write(f"**✅ 優勢：** {plan['pros']}")
                    st.write(f"**❌ 缺點：** {plan['cons']}")
                    st.divider()
                    st.write(f"**推薦指數：** {plan['star']}")
    
    st.info("💡 **決策關鍵：** 若目標是「Carving (刻滑)」，Riding Camp 的訓練內容 (Lv3 Riding) 遠比 CASI Lv1 (Lv1 Teaching) 更符合需求。")

# ==========================================
# TAB 2: 預算計算 (RWD 優化：直覺輸入)
# ==========================================
with tab2:
    st.markdown("### 💸 預算試算 (每人)")
    
    # 根據地點調整預設價格
    is_hokkaido = "北海道" in location
    base_accom = 30000 if is_hokkaido else 20000
    base_lift = 9000 if is_hokkaido else 7000

    # RWD 佈局：主要輸入區
    with st.container(border=True):
        st.subheader("1. 參數設定")
        c1, c2 = st.columns(2)
        with c1:
            camp_cost = st.number_input("Camp 課程費 (JPY)", value=150000, step=10000)
            accom_daily = st.number_input("每晚房價 (JPY/人)", value=base_accom//2, help="假設雙人房平分")
            lift_daily = st.number_input("每日雪票 (JPY)", value=base_lift)
        with c2:
            food_daily = st.number_input("每日餐費 (JPY)", value=7000)
            flight_cost = st.number_input("機票 (TWD)", value=22000 if is_hokkaido else 18000)
            misc_cost = st.number_input("雜支/交通 (JPY)", value=20000)

    # 計算邏輯
    total_accom_jpy = accom_daily * (days - 1)
    total_lift_jpy = lift_daily * (days - 2) # 扣除頭尾
    total_food_jpy = food_daily * days
    total_jpy = total_accom_jpy + total_lift_jpy + total_food_jpy + camp_cost + misc_cost
    total_twd = (total_jpy * currency_rate) + flight_cost

    st.divider()

    # RWD 佈局：結果展示 (Metrics)
    st.subheader("2. 計算結果")
    m1, m2, m3 = st.columns(3)
    m1.metric("總預算 (TWD)", f"${int(total_twd):,}", delta="含機票")
    m2.metric("日幣總支出", f"¥{int(total_jpy):,}")
    m3.metric("課程佔比", f"{int((camp_cost/total_jpy)*100)}%", help="課程費用佔總日幣支出的比例")

    # 圖表
    with st.expander("📊 查看費用結構圖表", expanded=True):
        cost_data = pd.DataFrame({
            "類別": ["住宿", "雪票", "餐飲", "課程", "交通雜支"],
            "金額(JPY)": [total_accom_jpy, total_lift_jpy, total_food_jpy, camp_cost, misc_cost]
        })
        st.bar_chart(cost_data.set_index("類別"), color="#29b5e8")

# ==========================================
# TAB 3: 每日行程 (RWD 優化：時間軸 Expanders)
# ==========================================
with tab3:
    st.markdown("### 📅 14天戰略行程表")
    st.caption("點擊下方天數查看詳細策略")

    # 資料結構
    schedule_data = [
        {"day": 1, "title": "抵達 & 移動", "icon": "✈️", "desc": "抵達機場，搭乘巴士前往雪場，入住並租賃裝備。", "tips": "早點休息，適應溫差。"},
        {"day": 2, "title": "暖身日 (Warm up)", "icon": "🏂", "desc": "自主滑行，找回腳感，適應日本雪況。", "tips": "不要衝太快，檢查裝備設定。"},
        {"day": 3, "title": "Camp Day 1 (基礎)", "icon": "🏫", "desc": "Camp 開始！上午分班測試。你修正站姿 (Stance)，朋友修正細節。", "tips": "心態歸零，聽教練指令。"},
        {"day": 4, "title": "Camp Day 2 (進階)", "icon": "📈", "desc": "針對彎形 (Turn Shape) 進行調整。你練膽量，他練發力。", "tips": "錄影檢視自己的動作。"},
        {"day": 5, "title": "Camp Day 3 (應用)", "icon": "🏔️", "desc": "地形適應。你練紅線穩定度，他練板刃施壓 (Pressure)。", "tips": "腿會很酸，晚上多伸展。"},
        {"day": 6, "title": "Camp Day 4 (動態)", "icon": "🌪️", "desc": "動態滑行 (Dynamics)。你練刃咬雪，他練 Cross-under。", "tips": "嘗試加快節奏。"},
        {"day": 7, "title": "Camp Day 5 (結業)", "icon": "🎓", "desc": "最終驗收 & 影片分析。教練給予未來練習建議。", "tips": "跟同學教練交換聯絡方式。"},
        {"day": 8, "title": "完全休息日", "icon": "🛌", "desc": "肌肉修復日。睡到飽，去鎮上逛逛，泡溫泉。", "tips": "這天絕對不要滑雪！"},
        {"day": 9, "title": "自主練習 (模仿)", "icon": "👯", "desc": "朋友帶你滑。嘗試模仿朋友在 Camp 學到的新動作。", "tips": "由朋友充當一日教練。"},
        {"day": 10, "title": "自主練習 (挑戰)", "icon": "🚀", "desc": "去挑戰 Camp 期間不敢去的陡坡。", "tips": "注意安全，不要受傷。"},
        {"day": 11, "title": "互相錄影日", "icon": "📹", "desc": "拍攝「After」影片，與 Day 2 的影片做對比。", "tips": "找光線好、人少的地方拍。"},
        {"day": 12, "title": "半日滑 / 觀光", "icon": "🛍️", "desc": "早上滑雪，下午保留體力去買伴手禮或裝備。", "tips": "雪具店通常這時候有折扣。"},
        {"day": 13, "title": "Fun Run 驗收", "icon": "🎉", "desc": "不練功了！單純享受滑雪的樂趣。", "tips": "Enjoy the ride!"},
        {"day": 14, "title": "回程", "icon": "👋", "desc": "搭乘巴士前往機場，回家。", "tips": "檢查護照、手機、錢包。"}
    ]

    # 使用迴圈產生 Expanders
    for item in schedule_data:
        # 根據天數給予不同顏色的標題提示
        label = f"Day {item['day']} | {item['icon']} {item['title']}"
        
        # 預設展開「今天」或前幾天 (這裡範例全收合，保持整潔)
        with st.expander(label, expanded=False):
            st.markdown(f"**📝 內容：** {item['desc']}")
            st.info(f"💡 **Tips:** {item['tips']}")

    st.warning("⚠️ **3月雪況提醒：** 下午容易出現思樂冰 (Slush)，建議練功集中在 08:30 - 12:30 硬雪時段。")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Designed for 2026 Ski Trip | Powered by Streamlit</div>", unsafe_allow_html=True)
