import json
import random

import pandas as pd
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
    .stButton>button { background-color: #f8f9fa; border-radius: 16px; min-height: 92px; border: 2px solid #cbd5e1; }
    .stButton>button:hover { border-color: #2563eb; transform: translateY(-1px); }
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
    st.session_state.card_stage = 0
    st.session_state.answer_recorded = False
    st.session_state.answer_feedback = ""


def record_answer(is_correct):
    entry = WORDS[st.session_state.current_index]
    st.session_state.answer_results.append(
        {
            "word": entry["word"],
            "correct": is_correct,
        }
    )
    st.session_state.answer_feedback = "正解として記録しました。" if is_correct else "不正解として記録しました。"
    st.session_state.answer_recorded = True


def get_accuracy_data():
    results = st.session_state.get("answer_results", [])
    if not results:
        return pd.DataFrame({"回数": [], "正答率(%)": []})

    cumulative_correct = 0
    rows = []
    for index, result in enumerate(results, start=1):
        cumulative_correct += 1 if result["correct"] else 0
        rows.append({"回数": index, "正答率(%)": round(cumulative_correct / index * 100, 1)})
    return pd.DataFrame(rows)


def go_to_next_word():
    next_index = (st.session_state.current_index + 1) % len(WORDS)
    st.session_state.current_index = next_index
    st.session_state.card_stage = 0


def go_to_previous_word():
    prev_index = (st.session_state.current_index - 1) % len(WORDS)
    st.session_state.current_index = prev_index
    st.session_state.card_stage = 0


def build_memory_cards():
    pairs = random.sample(WORDS, 8)
    cards = []
    for entry in pairs:
        cards.append(
            {
                "id": f"{entry['word']}_word",
                "text": entry["word"],
                "pair": entry["word"],
                "kind": "word",
            }
        )
        cards.append(
            {
                "id": f"{entry['word']}_meaning",
                "text": entry["meaning"],
                "pair": entry["word"],
                "kind": "meaning",
            }
        )
    random.shuffle(cards)
    return cards


def start_memory_game():
    st.session_state.memory_cards = build_memory_cards()
    st.session_state.memory_selected = []
    st.session_state.memory_matched = set()
    st.session_state.memory_message = ""
    st.session_state.memory_pending_clear_ids = []


def normalize_text(text):
    return " ".join(text.strip().lower().split())


def get_part_translation(part):
    prefix_map = {
        "un-": "〜でない・否定",
        "dis-": "〜でない・反対",
        "re-": "もう一度・再び",
        "pre-": "前に・予め",
        "mis-": "誤って・間違って",
        "im-": "〜でない・不",
        "trans-": "向こうへ・越えて",
        "sub-": "下に・低い",
        "tele-": "遠く",
        "auto-": "自動の",
        "bio-": "生命・生物",
        "inter-": "間に・相互に",
        "anti-": "反対の・抗",
        "en-": "〜に・〜を",
        "com-": "一緒に・共に",
        "de-": "下へ・離れて",
        "con-": "一緒に",
        "ex-": "外へ・出て",
        "per-": "完全に・徹底的に",
        "sur-": "上に・超えて",
        "ob-": "向かって・反対に",
    }
    suffix_map = {
        "-able": "〜できる",
        "-al": "〜の",
        "-ion": "〜の状態",
        "-tic": "〜の",
        "-sion": "〜の状態",
        "-ant": "〜の",
        "-ible": "〜できる",
    }
    if part in prefix_map:
        return prefix_map[part]
    if part in suffix_map:
        return suffix_map[part]
    return "意味の核"


def get_parts(entry):
    parts = []
    if entry["prefix"]:
        parts.append(entry["prefix"])
    if entry["root"]:
        parts.append(entry["root"])
    if entry["suffix"]:
        parts.append(entry["suffix"])
    return parts


def save_word_memo(word, text):
    cleaned = text.strip()
    if cleaned:
        st.session_state.word_memos[word] = cleaned
    else:
        st.session_state.word_memos.pop(word, None)
    st.session_state.memo_feedback = "メモを保存しました。" if cleaned else "メモを削除しました。"
    st.session_state.memo_target_word = word


def get_memo_for_word(word):
    return st.session_state.word_memos.get(word, "")


def get_current_memo():
    return get_memo_for_word(st.session_state.memo_target_word)


if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "card_stage" not in st.session_state:
    st.session_state.card_stage = 0
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
if "memory_pending_clear_ids" not in st.session_state:
    st.session_state.memory_pending_clear_ids = []
if "answer_results" not in st.session_state:
    st.session_state.answer_results = []
if "answer_feedback" not in st.session_state:
    st.session_state.answer_feedback = ""
if "answer_recorded" not in st.session_state:
    st.session_state.answer_recorded = False
if "word_memos" not in st.session_state:
    st.session_state.word_memos = {}
if "memo_feedback" not in st.session_state:
    st.session_state.memo_feedback = ""
if "memo_target_word" not in st.session_state:
    st.session_state.memo_target_word = WORDS[0]["word"]


# ------------------------------
# UI
# ------------------------------
def render_card(title, content, accent="white"):
    background = "#ffffff" if accent == "white" else "#fef3c7"
    border = "#d1d5db" if accent == "white" else "#f59e0b"
    st.markdown(
        f"""
        <div style="background:{background}; border:1px solid {border}; border-radius:16px; padding:20px 22px; margin-bottom:16px; box-shadow:0 2px 10px rgba(15,23,42,0.06);">
          <div style="font-size:0.85rem; font-weight:700; color:#6b7280; margin-bottom:8px;">{title}</div>
          <div style="font-size:1.05rem; line-height:1.7;">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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

    st.divider()
    st.header("単語検索")
    search_query = st.text_input("単語を検索", placeholder="例: happy")
    matched_words = [entry["word"] for entry in WORDS if search_query.lower() in entry["word"].lower()]
    if matched_words:
        selected_word = st.selectbox("検索結果", matched_words, key="memo_search_word")
        if st.button("この単語をメモ編集", use_container_width=True):
            st.session_state.memo_target_word = selected_word
            st.session_state.current_index = next(i for i, entry in enumerate(WORDS) if entry["word"] == selected_word)
            st.session_state.card_stage = 0
            st.rerun()
    elif search_query:
        st.info("一致する単語はありません。")

learn_tab, game_tab, record_tab, memo_tab = st.tabs(["英単語を暗記する", "神経衰弱", "学習記録", "覚え方メモ"])

with learn_tab:
    entry = WORDS[st.session_state.current_index]
    stage = st.session_state.card_stage

    st.subheader(f"今の単語: {entry['word']}")
    st.caption("カードをめくって、1枚ずつ内容を確認してください。")
    st.caption(f"カード {stage + 1}/3")

    if stage == 0:
        render_card("1枚目", f"<div style='font-size:2rem; font-weight:700; color:#111827;'>{entry['word']}</div>")
    elif stage == 1:
        part_lines = []
        if entry["prefix"]:
            part_lines.append(f"接頭語: {entry['prefix']}（{get_part_translation(entry['prefix'])}）")
        if entry["root"]:
            part_lines.append(f"語幹: {entry['root']}（{get_part_translation(entry['root'])}）")
        if entry["suffix"]:
            part_lines.append(f"接尾語: {entry['suffix']}（{get_part_translation(entry['suffix'])}）")
        current_memo = get_current_memo()
        if current_memo:
            part_lines.append(f"<br>覚え方メモ: {current_memo}")
        render_card(
            "2枚目",
            f"<div>{'<br>'.join(part_lines)}</div>",
            accent="yellow",
        )
    else:
        render_card("3枚目", f"<div style='font-size:1.3rem; font-weight:700; color:#111827;'>英単語の日本語訳: {entry['meaning']}</div>")

    if stage == 2:
        if st.session_state.answer_feedback:
            st.success(st.session_state.answer_feedback)

        answer_col1, answer_col2 = st.columns(2)
        with answer_col1:
            if st.button("正解", use_container_width=True):
                record_answer(True)
                st.rerun()
        with answer_col2:
            if st.button("不正解", use_container_width=True):
                record_answer(False)
                st.rerun()

    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("もどる", use_container_width=True):
            if stage == 0:
                go_to_previous_word()
            else:
                st.session_state.card_stage = max(0, stage - 1)
            st.rerun()
    with col_next:
        if st.button("めくる", use_container_width=True):
            if stage == 2:
                if not st.session_state.answer_recorded:
                    st.warning("3枚目の日本語訳で正解・不正解を選んでください。")
                else:
                    go_to_next_word()
                    st.rerun()
            else:
                st.session_state.card_stage = min(2, stage + 1)
                st.rerun()

with game_tab:
    st.write("英単語と日本語訳のカードをめくって、8セットをそろえましょう。")
    if st.button("カードをシャッフル", use_container_width=True):
        start_memory_game()

    if st.session_state.memory_message:
        st.info(st.session_state.memory_message)

    if len(st.session_state.memory_matched) == len(st.session_state.memory_cards):
        st.balloons()
        st.success("すべてそろいました！英単語と意味のつながりを覚えられています。")

    cards = st.session_state.memory_cards
    selected_ids = list(st.session_state.memory_selected)
    matched_ids = set(st.session_state.memory_matched)

    cols = st.columns(4)
    for index, card in enumerate(cards):
        with cols[index % 4]:
            is_revealed = card["id"] in selected_ids or card["id"] in matched_ids
            if is_revealed:
                label = card["text"]
                card_kind = "英単語" if card["kind"] == "word" else "日本語訳"
            else:
                label = "？"
                card_kind = "裏面"

            if st.button(
                label,
                key=f"memory_card_{card['id']}",
                use_container_width=True,
            ):
                if st.session_state.get("memory_pending_clear_ids"):
                    st.session_state.memory_selected = []
                    st.session_state.memory_pending_clear_ids = []
                    st.session_state.memory_message = ""

                if card["id"] in matched_ids:
                    st.session_state.memory_message = "すでにそろっています。"
                elif card["id"] in st.session_state.memory_selected:
                    st.session_state.memory_selected.remove(card["id"])
                    st.session_state.memory_message = ""
                elif len(st.session_state.memory_selected) < 2:
                    st.session_state.memory_selected.append(card["id"])
                    if len(st.session_state.memory_selected) == 2:
                        first_id = st.session_state.memory_selected[0]
                        second_id = st.session_state.memory_selected[1]
                        first_card = next(item for item in cards if item["id"] == first_id)
                        second_card = next(item for item in cards if item["id"] == second_id)

                        if first_card["pair"] == second_card["pair"]:
                            st.session_state.memory_matched.update({first_id, second_id})
                            st.session_state.memory_message = "一致しました！"
                            st.session_state.memory_pending_clear_ids = []
                            st.session_state.memory_selected = []
                        else:
                            st.session_state.memory_message = "違います。もう一度選んでみましょう。"
                            st.session_state.memory_pending_clear_ids = [first_id, second_id]
                    st.rerun()
                else:
                    st.session_state.memory_message = "2枚まで選べます。"

            if is_revealed:
                st.caption(f"{card_kind}")
            else:
                st.caption("裏面")

with record_tab:
    st.subheader("回数ごとの正答率")
    chart_data = get_accuracy_data()
    if chart_data.empty:
        st.info("まだ回答がありません。英単語カードで正解・不正解を記録してください。")
    else:
        st.line_chart(chart_data.set_index("回数")["正答率(%)"])
        total_attempts = len(st.session_state.answer_results)
        correct_count = sum(1 for item in st.session_state.answer_results if item["correct"])
        st.metric("総回答数", total_attempts)
        st.metric("正答率", f"{round(correct_count / total_attempts * 100, 1)}%")

        history_df = pd.DataFrame(st.session_state.answer_results)
        history_df["結果"] = history_df["correct"].map({True: "正解", False: "不正解"})
        st.dataframe(history_df[["word", "結果"]], use_container_width=True, hide_index=True)

with memo_tab:
    entry = WORDS[st.session_state.current_index]
    st.subheader(f"{entry['word']} の覚え方メモ")
    st.caption("収録されている単語を選んで、覚え方メモを残しましょう。")

    word_options = [item["word"] for item in WORDS]
    selected_word = st.selectbox("単語を選ぶ", word_options, index=word_options.index(st.session_state.memo_target_word))
    if selected_word != st.session_state.memo_target_word:
        st.session_state.memo_target_word = selected_word
        st.session_state.current_index = next(i for i, entry in enumerate(WORDS) if entry["word"] == selected_word)
        st.session_state.card_stage = 0
        st.rerun()

    current_memo = get_memo_for_word(selected_word)
    memo_text = st.text_area("メモを入力", value=current_memo, height=180)
    if st.button("メモを保存", use_container_width=True):
        save_word_memo(selected_word, memo_text)
        st.rerun()

    if st.session_state.memo_feedback:
        st.success(st.session_state.memo_feedback)

    if current_memo:
        st.info("保存済みのメモ")
        st.write(current_memo)

st.divider()
st.caption("英単語は分解のつながりを意識すると覚えやすくなります。次は自分で接頭語・語根・接尾語を見つけてみましょう。")
