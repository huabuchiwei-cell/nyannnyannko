import streamlit as st
import random

# ------------------------------
# ページ設定（白基調）
# ------------------------------
st.set_page_config(page_title="英検2級 単語分解学習アプリ", page_icon="📚", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: white; color: #111; }
    .stButton>button { background-color: #f8f9fa; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# 英検2級レベルの語彙データ（簡易：接頭辞・語根・接尾語を分割）
# 必要なら語彙を追加してください
# ------------------------------
WORDS = [
    {"word": "unhappy", "meaning": "不幸な", "prefix": "un-", "root": "happy", "suffix": ""},
    {"word": "disagree", "meaning": "同意しない", "prefix": "dis-", "root": "agree", "suffix": ""},
    {"word": "replay", "meaning": "再生する・やり直す", "prefix": "re-", "root": "play", "suffix": ""},
    {"word": "preview", "meaning": "予告・下見", "prefix": "pre-", "root": "view", "suffix": ""},
    {"word": "misunderstand", "meaning": "誤解する", "prefix": "mis-", "root": "understand", "suffix": ""},
    {"word": "impossible", "meaning": "不可能な", "prefix": "im-", "root": "poss", "suffix": "-ible"},
    {"word": "transport", "meaning": "輸送する", "prefix": "trans-", "root": "port", "suffix": ""},
    {"word": "submarine", "meaning": "潜水艦", "prefix": "sub-", "root": "marin", "suffix": "-e"},
    {"word": "telephone", "meaning": "電話", "prefix": "tele-", "root": "phone", "suffix": ""},
    {"word": "autograph", "meaning": "署名", "prefix": "auto-", "root": "graph", "suffix": ""},
    {"word": "biology", "meaning": "生物学", "prefix": "bio-", "root": "logy", "suffix": ""},
    {"word": "international", "meaning": "国際的な", "prefix": "inter-", "root": "nation", "suffix": "-al"},
    {"word": "antibiotic", "meaning": "抗生物質", "prefix": "anti-", "root": "bio", "suffix": "-tic"},
    {"word": "reaction", "meaning": "反応", "prefix": "re-", "root": "act", "suffix": "-ion"},
    {"word": "encourage", "meaning": "勇気づける", "prefix": "en-", "root": "courage", "suffix": ""},
    {"word": "comfortable", "meaning": "快適な", "prefix": "com-", "root": "fort", "suffix": "-able"},
    {"word": "predict", "meaning": "予測する", "prefix": "pre-", "root": "dict", "suffix": ""},
    {"word": "decision", "meaning": "決定", "prefix": "de-", "root": "cid", "suffix": "-sion"},
    {"word": "discover", "meaning": "発見する", "prefix": "dis-", "root": "cover", "suffix": ""},
    {"word": "return", "meaning": "戻る", "prefix": "re-", "root": "turn", "suffix": ""},
    {"word": "continue", "meaning": "続ける", "prefix": "con-", "root": "tinue", "suffix": ""},
    {"word": "imagine", "meaning": "想像する", "prefix": "im-", "root": "agine", "suffix": ""},
    {"word": "export", "meaning": "輸出する", "prefix": "ex-", "root": "port", "suffix": ""},
    {"word": "important", "meaning": "重要な", "prefix": "im-", "root": "port", "suffix": "-ant"},
    {"word": "perform", "meaning": "演じる・行う", "prefix": "per-", "root": "form", "suffix": ""},
    {"word": "prepare", "meaning": "準備する", "prefix": "pre-", "root": "pare", "suffix": ""},
    {"word": "prevent", "meaning": "妨げる", "prefix": "pre-", "root": "vent", "suffix": ""},
    {"word": "surprise", "meaning": "驚かせる", "prefix": "sur-", "root": "prise", "suffix": ""},
    {"word": "observe", "meaning": "観察する", "prefix": "ob-", "root": "serve", "suffix": ""},
]

COMMON_PREFIXES = [
    "un-", "dis-", "re-", "pre-", "mis-", "im-", "trans-", "sub-", "tele-", "auto-",
    "bio-", "inter-", "anti-", "en-", "com-", "de-", "con-", "ex-", "per-", "sur-", "ob-",
]


def pick_new_word():
    st.session_state.current = random.randrange(len(WORDS))


def reset_progress():
    st.session_state.current = None


if "current" not in st.session_state:
    st.session_state.current = None


# ------------------------------
# UI
# ------------------------------
st.title("📚 英検2級 — 接頭辞・語根・接尾語で覚える単語アプリ")
st.write("白基調でシンプルに、接頭辞をヒントに単語を分解して覚えます。")

with st.sidebar:
    st.header("ヒント: 接頭辞一覧")
    st.write(", ".join(COMMON_PREFIXES))
    st.divider()
    if st.button("次の単語", use_container_width=True):
        pick_new_word()
        st.experimental_rerun()
    if st.button("リセット", use_container_width=True):
        reset_progress()
        st.experimental_rerun()

mode = st.radio("モードを選択", ("学習モード", "テストモード"))

if st.session_state.current is None:
    pick_new_word()

entry = WORDS[st.session_state.current]

st.subheader(f"単語: {entry['word']}")

col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("**ヒント（接頭辞）**")
    # 接頭辞をヒントとして表示
    prefix_hint = entry.get("prefix", "")
    if prefix_hint:
        st.info(prefix_hint)
    else:
        st.info("接頭辞なし")

    if st.button("構成要素を表示する"):
        st.success(f"接頭辞: {entry['prefix'] or '(なし)'}  — 語根: {entry['root'] or '(不明)'}  — 接尾語: {entry['suffix'] or '(なし)'}")

with col2:
    if mode == "学習モード":
        if st.checkbox("意味を表示する"):
            st.write("意味: ", entry["meaning"])
        st.write("---")
        st.write("練習: 接頭辞を見て、語根や接尾語を確認しましょう。")
    else:
        st.write("---")
        st.write("テスト: 各要素を入力してください（空白可）。正解は小文字でチェックします。")
        p = st.text_input("接頭辞", key="pref_input")
        r = st.text_input("語根", key="root_input")
        s = st.text_input("接尾語", key="suf_input")
        if st.button("採点する"):
            correct = True
            msgs = []
            if p.strip().lower() != (entry['prefix'] or "").lower():
                correct = False
                msgs.append(f"接頭辞: 正解は {entry['prefix'] or '(なし)'}")
            else:
                msgs.append("接頭辞: 正解")

            if r.strip().lower() != (entry['root'] or "").lower():
                correct = False
                msgs.append(f"語根: 正解は {entry['root'] or '(不明)'}")
            else:
                msgs.append("語根: 正解")

            if s.strip().lower() != (entry['suffix'] or "").lower():
                correct = False
                msgs.append(f"接尾語: 正解は {entry['suffix'] or '(なし)'}")
            else:
                msgs.append("接尾語: 正解")

            if correct:
                st.balloons()
                st.success("すべて正解！よくできました！")
            for m in msgs:
                st.write(m)

st.divider()
st.caption("必要なら語彙を追加したり、問題数を増やして拡張できます。要望があれば教えてください。")
