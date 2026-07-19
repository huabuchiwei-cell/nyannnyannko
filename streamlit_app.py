import json
import random

import streamlit as st
import streamlit.components.v1 as components
import word_builder_component as wb_component

# ------------------------------
# ページ設定
# ------------------------------
st.set_page_config(page_title="英単語分解学習", page_icon="📚", layout="wide")

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
    st.session_state.assembled_parts = []


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
if "assembled_parts" not in st.session_state:
    st.session_state.assembled_parts = []
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
st.title("📚 英単語を分解して覚える")
st.write("接頭語・語根・接尾語を使って英単語の意味をつかみ、神経衰弱で復習できる学習アプリです。")

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

learn_tab, game_tab = st.tabs(["英単語を暗記する", "神経衰弱"])

with learn_tab:
    entry = WORDS[st.session_state.current_index]
    st.subheader(f"今の単語: {entry['word']}")

    st.info("接頭語・語根・接尾語をクリックして、英単語を組み立てましょう。")

    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown("**分解**")
        st.write(f"接頭語: {entry['prefix'] or 'なし'}")
        st.write(f"語根: {entry['root']}")
        st.write(f"接尾語: {entry['suffix'] or 'なし'}")

    with col2:
        st.markdown("**英単語を組み立てる**")
        parts = get_parts(entry)
        
        # パーツ選択ボタン
        st.write("**パーツを選択:**")
        cols_buttons = st.columns(len(parts))
        for idx, part in enumerate(parts):
            with cols_buttons[idx]:
                if st.button(part, key=f"part_{st.session_state.current_index}_{idx}", use_container_width=True):
                    st.session_state.assembled_parts.append(part)
        
        # 組み立てられた単語の表示
        if st.session_state.assembled_parts:
            assembled_word = "".join(st.session_state.assembled_parts)
            st.write(f"**現在の組み立て:** {assembled_word}")
            
            col_undo, col_clear = st.columns(2)
            with col_undo:
                if st.button("最後を取り消す", use_container_width=True):
                    st.session_state.assembled_parts.pop()
                    st.rerun()
            with col_clear:
                if st.button("すべてクリア", use_container_width=True):
                    st.session_state.assembled_parts = []
                    st.rerun()
        else:
            assembled_word = ""
            st.write("**現在の組み立て:** (なし)")

        # 意味入力
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
    selected_ids = list(st.session_state.memory_selected)
    matched_ids = list(st.session_state.memory_matched)

    memory_action = wb_component.render_memory_game(
        cards=cards,
        selected=selected_ids,
        matched=matched_ids,
        message=st.session_state.memory_message,
        key="memory_game",
    )

    if memory_action and isinstance(memory_action, dict):
        action = memory_action.get("action")
        card_id = memory_action.get("id")
        click_id = memory_action.get("clickId")

        if action == "select" and card_id and click_id:
            if st.session_state.get("last_memory_click") != click_id:
                st.session_state.last_memory_click = click_id
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
                st.experimental_rerun()

st.divider()
st.caption("英単語は分解のつながりを意識すると覚えやすくなります。次は自分で接頭語・語根・接尾語を見つけてみましょう。")
