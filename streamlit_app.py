import random

import streamlit as st

from word_builder_component import render_word_builder

# ------------------------------
# ページ設定
# ------------------------------
st.set_page_config(page_title="英単語分解学習", page_icon="📚", layout="centered")

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
# 語彙データ
# ------------------------------
WORDS = [
    {"word": "unhappy", "meaning": "不幸な", "prefix": "un-", "root": "happy", "suffix": ""},
    {"word": "disagree", "meaning": "同意しない", "prefix": "dis-", "root": "agree", "suffix": ""},
    {"word": "replay", "meaning": "再生する・やり直す", "prefix": "re-", "root": "play", "suffix": ""},
    {"word": "preview", "meaning": "予告・下見", "prefix": "pre-", "root": "view", "suffix": ""},
    {"word": "misunderstand", "meaning": "誤解する", "prefix": "mis-", "root": "understand", "suffix": ""},
    {"word": "impossible", "meaning": "不可能な", "prefix": "im-", "root": "poss", "suffix": "-ible"},
    {"word": "transport", "meaning": "輸送する", "prefix": "trans-", "root": "port", "suffix": ""},
    {"word": "submarine", "meaning": "潜水艦", "prefix": "sub-", "root": "marine", "suffix": ""},
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
    st.session_state.current_index = random.randrange(len(WORDS))
    st.session_state.guess_input = ""
    st.session_state.show_answer = False
    st.session_state.assembled_word = ""


def build_memory_cards():
    pairs = random.sample(WORDS, 4)
    cards = []
    for entry in pairs:
        cards.append(
            {
                "id": f"{entry['word']}_hint",
                "text": f"{entry['prefix'] or '・'} + {entry['root']} + {entry['suffix'] or '・'}",
                "pair": entry["word"],
            }
        )
        cards.append(
            {
                "id": f"{entry['word']}_word",
                "text": entry["word"],
                "pair": entry["word"],
            }
        )
    random.shuffle(cards)
    return cards


def start_memory_game():
    st.session_state.memory_cards = build_memory_cards()
    st.session_state.memory_selected = []
    st.session_state.memory_matched = set()
    st.session_state.memory_message = ""


def normalize_text(text):
    return " ".join(text.strip().lower().split())


def get_parts(entry):
    parts = []
    if entry["prefix"]:
        parts.append(entry["prefix"])
    if entry["root"]:
        parts.append(entry["root"])
    if entry["suffix"]:
        parts.append(entry["suffix"])
    return parts


if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "guess_input" not in st.session_state:
    st.session_state.guess_input = ""
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "assembled_word" not in st.session_state:
    st.session_state.assembled_word = ""
if "memory_cards" not in st.session_state:
    start_memory_game()
if "memory_selected" not in st.session_state:
    st.session_state.memory_selected = []
if "memory_matched" not in st.session_state:
    st.session_state.memory_matched = set()
if "memory_message" not in st.session_state:
    st.session_state.memory_message = ""


# ------------------------------
# UI
# ------------------------------
st.title("📚 接頭語・語根・接尾語で英単語を覚える")
st.write("接頭語・語根・接尾語の分解から英単語を推測する暗記法を中心にし、英単語神経衰弱をミニゲームとして楽しめます。")

with st.sidebar:
    st.header("覚え方のコツ")
    st.write("• 接頭語は意味の方向を示します")
    st.write("• 語根は中心的な意味の核です")
    st.write("• 接尾語は品詞や意味の変化を表します")
    st.divider()
    st.header("接頭語一覧")
    st.write(", ".join(COMMON_PREFIXES))
    st.divider()
    if st.button("次の単語", use_container_width=True):
        pick_new_word()
    if st.button("ゲームをやり直す", use_container_width=True):
        start_memory_game()

learn_tab, game_tab = st.tabs(["暗記法", "英単語神経衰弱"])

with learn_tab:
    entry = WORDS[st.session_state.current_index]
    st.subheader(f"今の単語: {entry['word']}")

    st.info("接頭語・語根・接尾語をドラッグして、英単語を組み立てましょう。")

    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown("**分解**")
        st.write(f"接頭語: {entry['prefix'] or 'なし'}")
        st.write(f"語根: {entry['root']}")
        st.write(f"接尾語: {entry['suffix'] or 'なし'}")

    with col2:
        st.markdown("**英単語を組み立てる**")
        parts = get_parts(entry)
        component_value = render_word_builder(parts, key=f"builder_{st.session_state.current_index}")
        if component_value:
            st.session_state.assembled_word = component_value

        assembled_word = st.session_state.get("assembled_word", "")
        if assembled_word:
            st.write(f"現在の組み立て: {assembled_word}")

        meaning_guess = st.text_input("意味を答えてください", value=st.session_state.guess_input)
        if st.button("意味を確認"):
            st.session_state.guess_input = meaning_guess
            st.session_state.show_answer = True

        if st.session_state.show_answer:
            if assembled_word.strip().lower() == entry["word"].lower() and normalize_text(meaning_guess) == normalize_text(entry["meaning"]):
                st.success("正解です！英単語と意味の両方を覚えられています。")
            elif assembled_word.strip().lower() == entry["word"].lower():
                st.warning(f"単語は正解です。意味は「{entry['meaning']}」です。")
            else:
                st.error(f"単語は不正解です。正解は {entry['word']} です。意味は「{entry['meaning']}」です。")

        st.caption("例: un- + happy = unhappy")

with game_tab:
    st.write("カードをめくって、分解のヒントと英単語を対応させましょう。")
    if st.button("カードをシャッフル"):
        start_memory_game()

    if st.session_state.memory_message:
        st.info(st.session_state.memory_message)

    if len(st.session_state.memory_matched) == len(st.session_state.memory_cards):
        st.balloons()
        st.success("すべてそろいました！分解のつながりを覚えられています。")

    cards = st.session_state.memory_cards
    cols = st.columns(4)
    for index, card in enumerate(cards):
        with cols[index % 4]:
            card_id = card["id"]
            is_matched = card_id in st.session_state.memory_matched
            is_selected = card_id in st.session_state.memory_selected

            if is_matched:
                st.button(card["text"], key=f"memory_{card_id}", disabled=True)
            else:
                label = card["text"] if is_selected else "？"
                if st.button(label, key=f"memory_{card_id}"):
                    if card_id in st.session_state.memory_selected:
                        st.session_state.memory_selected.remove(card_id)
                    elif len(st.session_state.memory_selected) < 2:
                        st.session_state.memory_selected.append(card_id)

                        if len(st.session_state.memory_selected) == 2:
                            first_id = st.session_state.memory_selected[0]
                            second_id = st.session_state.memory_selected[1]
                            first_card = next(item for item in cards if item["id"] == first_id)
                            second_card = next(item for item in cards if item["id"] == second_id)

                            if first_card["pair"] == second_card["pair"]:
                                st.session_state.memory_matched.update({first_id, second_id})
                                st.session_state.memory_message = "一致しました！"
                            else:
                                st.session_state.memory_message = "違います。もう一度選んでみましょう。"

                            st.session_state.memory_selected = []

st.divider()
st.caption("英単語は分解のつながりを意識すると覚えやすくなります。次は自分で接頭語・語根・接尾語を見つけてみましょう。")
