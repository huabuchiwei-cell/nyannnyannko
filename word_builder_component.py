from pathlib import Path

import streamlit.components.v1 as components

_component_path = Path(__file__).parent

word_builder = components.declare_component(
    name="word_builder",
    path=str(_component_path),
)


def render_word_builder(parts, key=None):
    return word_builder(mode="builder", parts=parts, key=key, default="")


def render_memory_game(cards, selected, matched, message, key=None):
    return word_builder(
        mode="memory",
        cards=cards,
        selected=selected,
        matched=matched,
        message=message,
        key=key,
        default={},
    )
