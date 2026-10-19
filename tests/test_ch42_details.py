"""Tests for Part V, Chapter 42 (Rosa's folder). Run with: pytest -q"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / "examples" / "part5_ch42_folder"
sys.path.insert(0, str(HERE))

import folder
from folder import allowed, words
from by_keyword import keyword_search
from by_meaning import meaning_search
from rag import answer, merge, search


def test_words_cleanup():
    assert words("The FX-200 oven, crème brûlée!") == [
        "fx-200", "oven", "creme", "brulee"]


def test_access_filter_hides_manager_documents():
    sources = [d[0] for d in allowed("assistant")]
    assert "flour-contract" not in sources
    assert "flour-contract" in [d[0] for d in allowed("manager")]


def test_search_respects_profile():
    q = "Is there a penalty if the flour is late?"
    assert search(q, "assistant") == []
    assert [e["source"] for e in search(q, "manager")] == ["flour-contract"]


def test_question_without_answer_finds_nothing():
    assert search("Who won the 2002 World Series?", "assistant") == []


def test_stop_words_bug(monkeypatch):
    monkeypatch.setattr(folder, "STOP_WORDS", set())
    docs = allowed("assistant")
    assert keyword_search("Who won the 2002 World Series?", docs) != []


def test_rrf_uses_position_not_score():
    a, b, c = ("a", "", ""), ("b", "", ""), ("c", "", "")
    merged = merge([(a, 99.0), (b, 1.0)], [(b, 0.9), (c, 0.1)])
    assert merged[0] == b


def test_meaning_search_links_different_words():
    docs = allowed("assistant")
    top = meaning_search("How long should it take?", docs)
    assert top and top[0][0][0] in {"carrot-recipe", "oven-manual"}


def test_answer_checks_citations():
    q = "How long does the carrot cake stay in the oven?"
    ok = lambda q, e: "Bake for 40 minutes at 350 degrees Fahrenheit [E1]."
    fake = lambda q, e: "Bake for 50 minutes [E7]."
    none = lambda q, e: "Bake for 50 minutes."
    assert answer(q, "assistant", ok)[0] == "LABELS OK"
    assert answer(q, "assistant", fake)[0] == "ANSWER WITHOUT A VALID SOURCE"
    assert answer(q, "assistant", none)[0] == "ANSWER WITHOUT A VALID SOURCE"


def test_not_found_does_not_call_the_model():
    def boom(q, e):
        raise AssertionError("model must not be called")
    status, _ = answer("Who won the 2002 World Series?", "assistant", boom)
    assert status == "NOT FOUND"


def test_story_output_matches_expected():
    out = subprocess.run([sys.executable, "story.py"], cwd=HERE,
                         capture_output=True, text=True, check=True).stdout
    assert out == (HERE / "expected_output.txt").read_text()
