import streamlit as st
import pandas as pd

# --- 1. 頁面基礎設定 (必須放在第一行) ---
st.set_page_config(
    page_title="滑雪攻略與預算助手",
    page_icon="🏂",
    layout="centered", # 手機版建議用 centered，閱讀體驗較佳
    initial_sidebar_state="auto"
)

# --- 2. 全域設定 ---
EXCHANGE_RATE = 0.22  # JPY to TWD
WINNER_MARK = " 🏆"

# --- 功能 A: 課程比較 (CASI vs 私教 vs Camp) ---
def show_ski_comparison():
    st.header("🏂 課程大比拼")
    st.caption("CASI vs. 私教 vs. Camp | 2024-25 日本行情")

    data = [
        {
            "比較項目": "1. 核心目的",
            "CASI (證照課)": "學怎麼「教人」\n修正滑行基礎",
            "私教 (Private)": "解決個人疑難雜症\n客製化修整",
            "訓練營 (Camp)": f"提升能力 + 社交\n密集訓練技巧{WINNER_MARK}"
        },
        {
            "比較項目": "2. 平均日價",
            "CASI (證照課)": f"低\n約 ¥18,000{WINNER_MARK}",
            "私教 (Private)": "高\n約 ¥90,000 (全日)",
            "訓練營 (Camp)": "中\n約 ¥35,000"
        },
        {
            "比較項目": "3. 客製化",
            "CASI (證照課)": "低 (趕進度)",
            "私教 (Private)": f"高 (完全客製){WINNER_MARK}",
            "訓練營 (Camp)": "中 (小班制)"
        },
        {
            "比較項目": "4. 技術方向",
            "CASI (證照課)": "標準化 (Demo)",
            "私教 (Private)": "個人風格 (Style)",
            "訓練營 (Camp)": f"綜合地形能力{WINNER_MARK}"
        },
        {
            "比較項目": "5. 社交氛圍",
            "CASI (證照課)": "高壓 / 競爭",
            "私教 (Private)": "封閉 / 專注",
            "訓練營 (Camp)": f"熱血 / 交友{WINNER_MARK}"
        },
        {
            "比較項目": "6. 語言門檻",
            "CASI (證照課)": "高 (全英文)",
            "私教 (Private)": f"無 (中文優){WINNER_MARK}",
            "訓練營 (Camp)": "中 (有華人團)"
        },
        {
            "比較項目": "7. 錄影分析",
            "CASI (證照課)": "有 (看標準度)",
            "私教 (Private)": "視教練而定",
            "訓練營 (Camp)": f"極詳盡 (晚間檢討){WINNER_MARK}"
        },
        {
            "比較項目": "8. 壓力值",
            "CASI (證照課)": "高 (怕Fail)",
            "私教 (Private)": f"低 (鼓勵為主){WINNER_MARK}",
            "訓練營 (Camp)": "中 (同儕激勵)"
        }
    ]

    # 手機優先視圖 (Tabs 切換)
    view_mode = st.radio("檢視模式", ["📱 卡片模式 (手機推薦)", "💻 表格模式"], horizontal=True)

    if "卡片" in view_mode:
        for item in data:
            with st.expander(f"📌 {item['比較項目']}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.info(f"**CASI**\n\n{item['CASI (證照課)']}")
                with c2:
                    st.warning(f"**私教**\n\n{item['私教 (Private)']}")
                with c3:
                    st.success(f"**Camp**\n\n{item['訓練營 (Camp)']}")
    else:
        df = pd.DataFrame(data)
        st.markdown(df.to_markdown(index=False))


# --- 功能 B: 組合推薦 (Green S + Black S) ---
def show_recommendation_matrix():
    st.header("🤝 雙人組合推薦方案")
    st.caption("針對 Green S (你) + Black S (朋友) 的最佳解")

    strategies = [
        {
            "title": f"A. 滑雪訓練營 (Camp){WINNER_MARK}",
            "star": "⭐⭐⭐⭐⭐",
            "desc": "白天分組練，晚上一起嗨。解決程度不一的最佳解。",
            "green": "無壓力進步，跟同程度的一起摔。",
            "black": "遇強則強，挑戰樹林與粉雪組。",
            "price": "中 (約 ¥70,000/人)",
            "type": "success"
        },
        {
            "title": "B. 全日私教 (拆單戰術)",
            "star": "⭐⭐⭐⭐",
            "desc": "買一位全日教練，上午教你，下午教朋友 (3+3小時)。",
            "green": "效率最高，1對1修姿勢。但下午要自己練。",
            "black": "教練點撥高階技巧，不用整天陪滑綠線。",
            "price": "高 (約 ¥90,000/雙人)",
            "type": "warning"
        },
        {
            "title": "C. CASI 考證 + 特訓",
            "star": "⭐⭐⭐",
            "desc": "朋友去考證照，你去上考前衝刺班。",
            "green": "打掉重練，壓力較大，姿勢要求嚴格。",
            "black": "腦力激盪，學習怎麼「教滑雪」。",
            "price": "低/中 (各自報名)",
            "type": "info"
        }
    ]

    for s in strategies:
        # 使用不同顏色的容器區分推薦度
        if s['type'] == 'success':
            container = st.success
        elif s['type'] == 'warning':
            container = st.warning
        else:
            container = st.info
        
        with container():
            st.subheader(s['title'])
            st.write(f"推薦度：{s['star']}")
            st.markdown(f"**🛠️ 策略：** {s['desc']}")
            
            # 手機版左右並排對照
            c1, c2 = st.columns(2)
            c1.markdown(f"**🟢 對你 (Green):**\n\n{s['green']}")
            c2.markdown(f"**⚫ 對友 (Black):**\n\n{s['black']}")
            st.caption(f"💰 預估費用：{s['price']}")
            st.divider()


# --- 功能 C: 3月雪場指南 ---
def show_resort_guide():
    st.header("🏔️ 3月初：北海道 vs. 長野")
    
    tab1, tab2 = st.tabs(["⚔️ 區域大PK", "🎯 推薦雪場"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.info("### ❄️ 北海道")
            st.markdown("""
            * **優勢:** 3月仍有粉雪、雪道全開。
            * **劣勢:** 交通貴、住宿貴。
            * **適合:** 想要最好雪質的你們。
            """)
        with c2:
            st.warning("### ☀️ 長野")
            st.markdown("""
            * **優勢:** 晴天率高、交通方便(新幹線)。
            * **劣勢:** 山腳可能是思樂冰(濕雪)。
            * **適合:** 想要觀光+滑雪的你們。
            """)

    with tab2:
        resorts = [
            {"name": "北海道 - 留壽都", "rank": "⭐⭐⭐⭐⭐", "text": "壓雪與樹林並存，最不吵架的雪場。"},
            {"name": "北海道 - 二世谷", "rank": "⭐⭐⭐⭐", "text": "夜生活豐富，外國人多，但人擠人。"},
            {"name": "長野 - 志賀高原", "rank": "⭐⭐⭐⭐", "text": "海拔最高，3月長野雪質擔當。"},
            {"name": "長野 - 白馬栂池", "rank": "⭐⭐⭐", "text": "超寬緩坡適合新手，但3月雪況較濕。"},
        ]
        
        for r in resorts:
            with st.expander(f"{r['name']} ({r['rank']})"):
                st.write(r['text'])


# --- 功能 D: 預算計算機 (New!) ---
def show_budget_calculator():
    st.header("💰 滑雪預算計算機")
    st.caption("快速計算雙人日本滑雪總花費")

    with st.form("budget_form"):
        st.subheader("1. 基礎設定")
        c1, c2 = st.columns(2)
        days = c1.number_input("滑雪天數", min_value=1, value=5)
        people = c2.number_input("人數", min_value=1, value=2)

        st.subheader("2. 費用估算 (單人/單位: TWD/JPY)")
        
        # 機票 (台幣)
        flight_twd = st.number_input("✈️ 來回機票 (TWD/人)", value=20000, step=1000)
        
        # 住宿 (日幣)
        hotel_jpy = st.number_input("🏨 住宿每晚 (JPY/人)", value=15000, step=1000, help="二世谷約2萬，長野約1-1.5萬")
        
        # 雪票 (日幣)
        lift_jpy = st.number_input("🎫 雪票每日 (JPY/人)", value=8000, step=500)

        # 餐飲 (日幣)
        food_jpy = st.number_input("🍜 餐飲每日 (JPY/人)", value=5000, step=500)

        # 課程選擇
        st.subheader("3. 課程費用")
        lesson_type = st.selectbox("選擇課程方案", ["不請教練", "A. 訓練營 (Camp)", "B. 全日私教 (拆單)", "C. CASI 考證團"])
        
        lesson_cost_jpy = 0
        if lesson_type == "A. 訓練營 (Camp)":
            lesson_cost_jpy = st.number_input("Camp 總費用 (JPY/人)", value=70000)
            st.caption("Camp 通常是算總價 (含多日教學)")
        elif lesson_type == "B. 全日私教 (拆單)":
            daily_rate = st.number_input("私教每日費用 (JPY/教練)", value=90000)
            lesson_days = st.number_input("請教練天數", min_value=1, max_value=days, value=2)
            # 私教是「總價除以人數」
            lesson_cost_jpy = (daily_rate * lesson_days) / people
            st.caption(f"說明：{daily_rate} x {lesson_days}天 ÷ {people}人 = {lesson_cost_jpy:.0f}/人")
        elif lesson_type == "C. CASI 考證團":
            lesson_cost_jpy = st.number_input("課程報名費 (JPY/人)", value=25000)

        submitted = st.form_submit_button("開始計算 🧮")

    if submitted:
        # 計算邏輯
        total_jpy_per_person = (hotel_jpy * days) + (lift_jpy * days) + (food_jpy * days) + lesson_cost_jpy
        total_twd_per_person = flight_twd + (total_jpy_per_person * EXCHANGE_RATE)
        grand_total_twd = total_twd_per_person * people

        st.divider()
        st.markdown(f"### 📊 計算結果 (匯率 {EXCHANGE_RATE})")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("每人總花費 (TWD)", f"${total_twd_per_person:,.0f}")
        m2.metric("雙人總預算 (TWD)", f"${grand_total_twd:,.0f}")
        m3.metric("課程佔比", f"{(lesson_cost_jpy * EXCHANGE_RATE / total_twd_per_person):.1%}")

        # 顯示詳細清單
        with st.expander("查看詳細費用結構"):
            details = {
                "項目": ["機票", "住宿", "雪票", "餐飲", "課程"],
                "金額 (TWD/人)": [
                    flight_twd,
                    hotel_jpy * days * EXCHANGE_RATE,
                    lift_jpy * days * EXCHANGE_RATE,
                    food_jpy * days * EXCHANGE_RATE,
                    lesson_cost_jpy * EXCHANGE_RATE
                ]
            }
            st.dataframe(pd.DataFrame(details))


# --- 主程式導航 ---
def main():
    # 側邊欄選單
    st.sidebar.title("功能選單")
    page = st.sidebar.radio(
        "前往",
        ["首頁", "1. 課程大比拼", "2. 雙人組合推薦", "3. 雪場指南", "4. 預算計算機"]
    )

    if page == "首頁":
        st.title("⛷️ 雙人滑雪攻略 App")
        st.write("歡迎！這是專為 **Green S (你)** 與 **Black S (朋友)** 設計的滑雪決策助手。")
        st.info("👈 請點擊左側選單開始規劃你的 3 月滑雪行！")
        
        st.markdown("### 快速檢視你的狀態")
        c1, c2 = st.columns(2)
        c1.success("**你 (Green S)**\n\n目標：建立信心、進階紅線、修正站姿")
        c2.error("**朋友 (Black S)**\n\n目標：樹林滑行、刻滑風格、教學挑戰")

    elif page == "1. 課程大比拼":
        show_ski_comparison()
    
    elif page == "2. 雙人組合推薦":
        show_recommendation_matrix()
    
    elif page == "3. 雪場指南":
        show_resort_guide()
        
    elif page == "4. 預算計算機":
        show_budget_calculator()

if __name__ == "__main__":
    main()
