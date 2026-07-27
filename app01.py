import pandas as pd
import streamlit as st

# 画面のタイトル設定
st.title("📈 積立＆据置運用シミュレーター")
st.caption("途中で積立を停止し、そのまま運用（放置）した場合の資産推移を試算できます")

# サイドバーに設定フォームを作成
st.sidebar.header("⚙️ 設定パラメーター")

initial_asset = st.sidebar.number_input(
    "初期投資額 (万円)", min_value=0, value=400, step=10
)
monthly_amount = st.sidebar.number_input(
    "毎月の積立額 (万円)", min_value=0.0, value=9.5, step=0.5
)
tsumitate_years = st.sidebar.slider(
    "積立期間 (年)", min_value=1, max_value=40, value=10
)
total_years = st.sidebar.slider(
    "全体の運用期間 (年)",
    min_value=tsumitate_years,
    max_value=50,
    value=20,
)
annual_return = st.sidebar.slider(
    "想定年利 (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.1
)

# ----------------------------------------------------
# 1. シミュレーション計算
# ----------------------------------------------------
monthly_return = (annual_return / 100) / 12
tsumitate_months = tsumitate_years * 12
total_months = total_years * 12

current_asset = float(initial_asset * 10000)
total_principal = float(initial_asset * 10000)

data = [{
    "経過年": 0,
    "資産額(万円)": round(current_asset / 10000, 2),
    "投資元本(万円)": round(total_principal / 10000, 2),
}]

for month in range(1, total_months + 1):
    deposit = (monthly_amount * 10000) if month <= tsumitate_months else 0.0
    total_principal += deposit
    current_asset = (current_asset + deposit) * (1 + monthly_return)

    if month % 12 == 0:
        data.append({
            "経過年": month // 12,
            "資産額(万円)": round(current_asset / 10000, 2),
            "投資元本(万円)": round(total_principal / 10000, 2),
        })

df = pd.DataFrame(data)

# 最終結果の数値算出
final_asset = int(round(current_asset))
final_principal = int(round(total_principal))
final_profit = final_asset - final_principal

# ----------------------------------------------------
# 2. カスタムカードUI表示（はみ出し・文字化け防止）
# ----------------------------------------------------
col1, col2, col3 = st.columns(3)

card_style = """
<div style="
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 12px 10px;
    text-align: center;
    border: 1px solid #e9ecef;
">
    <div style="font-size: 0.85rem; color: #6c757d; font-weight: bold; margin-bottom: 4px;">{label}</div>
    <div style="font-size: 1.15rem; color: #212529; font-weight: bold; word-break: break-all;">{value}</div>
    {sub}
</div>
"""

with col1:
    st.html(
        card_style.format(
            label="最終予想資産額", value=f"{final_asset:,}円", sub=""
        )
    )

with col2:
    st.html(
        card_style.format(
            label="投資元本累計", value=f"{final_principal:,}円", sub=""
        )
    )

with col3:
    sub_html = (
        f'<div style="font-size: 0.8rem; color: #28a745; margin-top: 2px;">+{final_profit:,}円</div>'
        if final_profit >= 0
        else ""
    )
    st.html(
        card_style.format(
            label="運用益", value=f"{final_profit:,}円", sub=sub_html
        )
    )

st.markdown("<br>", unsafe_allow_html=True)

# グラフ表示
st.subheader("📊 資産推移グラフ")
st.line_chart(df, x="経過年", y=["資産額(万円)", "投資元本(万円)"])

# 詳細データ表示
if st.checkbox("年ごとの詳細データを表示"):
    st.dataframe(df, use_container_width=True)