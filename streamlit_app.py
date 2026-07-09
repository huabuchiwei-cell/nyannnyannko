import streamlit as st
import random

# ------------------------------
# ページ設定
# ------------------------------
st.set_page_config(page_title="英単語 神経衰弱ゲーム", page_icon="🃏", layout="centered")

# ------------------------------
# 単語データ（英単語 ⇔ 日本語の意味のペア）
# ------------------------------
WORD_PAIRS = [
    ("apple", "りんご"),
    ("dog", "犬"),
    ("book", "本"),
    ("water", "水"),
    ("friend", "友達"),
    ("school", "学校"),
    ("happy", "幸せな"),
    ("river", "川"),
    ("mountain", "山"),
    ("music", "音楽"),
]


def init_game(num_pairs=8):
    """ゲームの初期化。カードをシャッフルして配置する"""
    pairs = random.sample(WORD_PAIRS, num_pairs)

    cards = []
    for pair_id, (en, jp) in enumerate(pairs):
        cards.append({"pair_id": pair_id, "text": en, "type": "en"})
        cards.append({"pair_id": pair_id, "text": jp, "type": "jp"})

    random.shuffle(cards)

    st.session_state.cards = cards
    st.session_state.revealed = [False] * len(cards)
    st.session_state.matched = [False] * len(cards)
    st.session_state.selected = []          # 現在選択中のカードのインデックス（最大2枚）
    st.session_state.pending_mismatch = []  # 直前にミスマッチしたカードのインデックス
    st.session_state.attempts = 0
    st.session_state.matches_found = 0
    st.session_state.game_over = False


def handle_card_click(idx):
    # 直前にミスマッチしたカードが表示されたままなら、まず裏返す
    if st.session_state.pending_mismatch:
        for i in st.session_state.pending_mismatch:
            st.session_state.revealed[i] = False
        st.session_state.pending_mismatch = []

    # 既にマッチ済み・選択済み・2枚選択中なら何もしない
    if st.session_state.matched[idx] or st.session_state.revealed[idx]:
        return
    if len(st.session_state.selected) >= 2:
        return

    st.session_state.revealed[idx] = True
    st.session_state.selected.append(idx)

    if len(st.session_state.selected) == 2:
        i1, i2 = st.session_state.selected
        st.session_state.attempts += 1

        card1 = st.session_state.cards[i1]
        card2 = st.session_state.cards[i2]

        if card1["pair_id"] == card2["pair_id"] and card1["type"] != card2["type"]:
            # マッチ成功
            st.session_state.matched[i1] = True
            st.session_state.matched[i2] = True
            st.session_state.matches_found += 1
            st.session_state.selected = []

            if all(st.session_state.matched):
                st.session_state.game_over = True
        else:
            # ミスマッチ → 次のクリックまで表示しておく
            st.session_state.pending_mismatch = [i1, i2]
            st.session_state.selected = []


# ------------------------------
# メイン画面
# ------------------------------
st.title("🃏 英単語 神経衰弱ゲーム")
st.caption("英単語とその日本語の意味が書かれたカードをめくって、ペアを探そう！")

if "cards" not in st.session_state:
    init_game()

# サイドバー：設定・リセット
with st.sidebar:
    st.header("⚙️ 設定")
    num_pairs = st.slider("ペア数（難易度）", min_value=4, max_value=len(WORD_PAIRS), value=8)
    if st.button("🔄 新しいゲームを始める", use_container_width=True):
        init_game(num_pairs)
        st.rerun()

    st.divider()
    st.metric("試行回数", st.session_state.attempts)
    st.metric("見つけたペア", f"{st.session_state.matches_found} / {len(st.session_state.cards)//2}")

# ゲームクリア表示
if st.session_state.game_over:
    st.balloons()
    st.success(f"🎉 クリア！ 全ペアを {st.session_state.attempts} 回の試行で見つけました！")

# カードをグリッド表示（4列）
cols_per_row = 4
cards = st.session_state.cards
num_cards = len(cards)

for row_start in range(0, num_cards, cols_per_row):
    cols = st.columns(cols_per_row)
    for col_offset, idx in enumerate(range(row_start, min(row_start + cols_per_row, num_cards))):
        with cols[col_offset]:
            card = cards[idx]
            is_revealed = st.session_state.revealed[idx]
            is_matched = st.session_state.matched[idx]

            if is_matched:
                # マッチ済みは常に表示、色を変える
                st.button(
                    f"✅ {card['text']}",
                    key=f"card_{idx}",
                    disabled=True,
                    use_container_width=True,
                )
            elif is_revealed:
                st.button(
                    card["text"],
                    key=f"card_{idx}",
                    disabled=True,
                    use_container_width=True,
                )
            else:
                if st.button("❓", key=f"card_{idx}", use_container_width=True):
                    handle_card_click(idx)
                    st.rerun()

st.divider()
st.caption("💡 ヒント: 英単語カードと、それに対応する日本語の意味カードのペアを見つけてください。")