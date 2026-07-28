import pandas as pd
import streamlit as st

# ブラウザの自動翻訳対策
st.markdown(
    """
    <html lang="ja">
    <head>
        <meta name="google" content="notranslate">
    </head>
""",
    unsafe_allow_html=True,
)

# 画面のタイトル設定
st.title("📈 積立＆据置運用シミュレーター")
st.caption(
    "途中で積立を停止したり、途中でまとまった資金をスポット追加した場合の資産推移を試算できます"
)

# ----------------------------------------------------
# 設定フォーム（メイン画面上の折りたたみメニューに移動）
# ----------------------------------------------------
with st.expander("⚙️ 設定パラメーターを変更する", expanded=True):
    col_a, col_b = st.columns(2)

    with col_a:
        initial_asset = st.number_input(
            "初期投資額 (万円)", min_value=0, value=100, step=10
        )
        monthly_amount = st.number_input(
            "毎月の積立額 (万円)", min_value=0.0, value=5.0, step=0.5
        )
        annual_return = st.number_input(
            "想定年利 (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1
        )

    with col_b:
        tsumitate_years = st.number_input(
            "積立期間 (年)", min_value=1, max_value=40, value=20, step=1
        )
        total_years = st.number_input(
            "全体の運用期間 (年)",
            min_value=int(tsumitate_years),
            max_value=50,
            value=30,
            step=1,
        )

    st.markdown("---")
    st.subheader("💰 スポット追加投資 (最大3回)")

    # スポット1
    col_s1_a, col_s1_y = st.columns(2)
    with col_s1_a:
        spot1_amount = st.number_input(
            "1回目 額(万円)", min_value=0, value=10, step=10
        )
    with col_s1_y:
        spot1_year = st.number_input(
            "1回目 何年目", min_value=1, max_value=int(total_years), value=5
        )

    # スポット2
    col_s2_a, col_s2_y = st.columns(2)
    with col_s2_a:
        spot2_amount = st.number_input(
            "2回目 額(万円)", min_value=0, value=50, step=10
        )
    with col_s2_y:
        spot2_year = st.number_input(
            "2回目 何年目", min_value=1, max_value=int(total_years), value=8
        )

    # スポット3
    col_s3_a, col_s3_y = st.columns(2)
    with col_s3_a:
        spot3_amount = st.number_input(
            "3回目 額(万円)", min_value=0, value=0, step=10
        )
    with col_s3_y:
        spot3_year = st.number_input(
            "3回目 何年目", min_value=1, max_value=int(total_years), value=15
        )

# ----------------------------------------------------
# 1. シミュレーション計算
# ----------------------------------------------------
monthly_return = (annual_return / 100) / 12
tsumitate_months = int(tsumitate_years * 12)
total_months = int(total_years * 12)

spot1_month = int(spot1_year * 12)
spot2_month = int(spot2_year * 12)
spot3_month = int(spot3_year * 12)

current_asset = float(initial_asset * 10000)
total_principal = float(initial_asset * 10000)

data = [{
    "経過年": 0,
    "資産額(万円)": round(current_asset / 10000, 2),
    "投資元本(万円)": round(total_principal / 10000, 2),
}]

for month in range(1, total_months + 1):
    deposit = (monthly_amount * 10000) if month <= tsumitate_months else 0.0

    if month == spot1_month and spot1_amount > 0:
        deposit += spot1_amount * 10000
    if month == spot2_month and spot2_amount > 0:
        deposit += spot2_amount * 10000
    if month == spot3_month and spot3_amount > 0:
        deposit += spot3_amount * 10000

    total_principal += deposit
    current_asset = (current_asset + deposit) * (1 + monthly_return)

    if month % 12 == 0:
        data.append({
            "経過年": month // 12,
            "資産額(万円)": round(current_asset / 10000, 2),
            "投資元本(万円)": round(total_principal / 10000, 2),
        })

df = pd.DataFrame(data)

final_asset = int(round(current_asset))
final_principal = int(round(total_principal))
final_profit = final_asset - final_principal

# ----------------------------------------------------
# 2. 結果表示
# ----------------------------------------------------
st.markdown("---")
col1, col2, col3 = st.columns(3)

card_style = """
<div style="
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 8px 4px;
    text-align: center;
    border: 1px solid #e9ecef;
">
    <div style="font-size: 0.75rem; color: #6c757d; font-weight: bold; margin-bottom: 2px;">{label}</div>
    <div style="font-size: 0.95rem; color: #212529; font-weight: bold; word-break: break-all;">{value}</div>
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
        f'<div style="font-size: 0.75rem; color: #28a745; margin-top: 2px;">+{final_profit:,}円</div>'
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