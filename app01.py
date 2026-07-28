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
st.caption("途中で積立を停止したり、途中でまとまった資金をスポット追加した場合の資産推移を試算できます")

# サイドバーに設定フォームを作成
st.sidebar.header("⚙️ 基本パラメーター")

initial_asset = st.sidebar.number_input(
    "初期投資額 (万円)", min_value=0, value=100, step=10
)
monthly_amount = st.sidebar.number_input(
    "毎月の積立額 (万円)", min_value=0.0, value=5.0, step=0.5
)
tsumitate_years = st.sidebar.slider(
    "積立期間 (年)", min_value=1, max_value=40, value=20
)
total_years = st.sidebar.slider(
    "全体の運用期間 (年)",
    min_value=tsumitate_years,
    max_value=50,
    value=30,
)
annual_return = st.sidebar.slider(
    "想定年利 (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1
)

# --- スポット追加投資（最大3回）の設定 ---
st.sidebar.markdown("---")
st.sidebar.subheader("💰 スポット追加投資 (最大3回)")

# スポット1
col_s1_a, col_s1_y = st.sidebar.columns(2)
with col_s1_a:
    spot1_amount = st.number_input(
        "1回目 額(万円)", min_value=0, value=100, step=10
    )
with col_s1_y:
    spot1_year = st.number_input(
        "1回目 何年目", min_value=1, max_value=total_years, value=5
    )

# スポット2
col_s2_a, col_s2_y = st.sidebar.columns(2)
with col_s2_a:
    spot2_amount = st.number_input(
        "2回目 額(万円)", min_value=0, value=0, step=10
    )
with col_s2_y:
    spot2_year = st.number_input(
        "2回目 何年目", min_value=1, max_value=total_years, value=10
    )

# スポット3
col_s3_a, col_s3_y = st.sidebar.columns(2)
with col_s3_a:
    spot3_amount = st.number_input(
        "3回目 額(万円)", min_value=0, value=0, step=10
    )
with col_s3_y:
    spot3_year = st.number_input(
        "3回目 何年目", min_value=1, max_value=total_years, value=15
    )

# ----------------------------------------------------
# 1. シミュレーション計算
# ----------------------------------------------------
monthly_return = (annual_return / 100) / 12
tsumitate_months = tsumitate_years * 12
total_months = total_years * 12

# 各スポット投資の「月数」を計算
spot1_month = spot1_year * 12
spot2_month = spot2_year * 12
spot3_month = spot3_year * 12

current_asset = float(initial_asset * 10000)
total_principal = float(initial_asset * 10000)

data = [{
    "経過年": 0,
    "資産額(万円)": round(current_asset / 10000, 2),
    "投資元本(万円)": round(total_principal / 10000, 2),
}]

for month in range(1, total_months + 1):
    # 通常の毎月積立額
    deposit = (monthly_amount * 10000) if month <= tsumitate_months else 0.0

    # スポット追加投資の判定（該当する月であれば加算）
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

# 最終結果の数値算出
final_asset = int(round(current_asset))
final_principal = int(round(total_principal))
final_profit = final_asset - final_principal

# ----------------------------------------------------
# 2. 結果表示
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