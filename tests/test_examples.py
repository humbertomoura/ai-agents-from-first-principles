"""Each example must print exactly what appears in the book
(saved in expected_output.txt next to the code)."""
import runpy
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1] / "examples"

EXAMPLES = [
    ("part1_ch08_thermostat", "run.py"),
    ("part2_ch15_assistant", "simulated.py"),
    ("part3_ch24_tools", "story.py"),
    ("part4_ch33_notebook", "story.py"),
    ("part5_ch42_folder", "story.py"),
]


@pytest.mark.parametrize("folder,script", EXAMPLES)
def test_output_matches_the_book(folder, script):
    directory = ROOT / folder
    result = subprocess.run(
        [sys.executable, script], cwd=directory,
        capture_output=True, text=True, check=True)
    expected = (directory / "expected_output.txt").read_text(
        encoding="utf-8")
    assert result.stdout == expected


def test_ch15_real_loop_with_a_fake_client(monkeypatch, capsys):
    """Runs the real loop from Chapter 15 with the API swapped for
    a fake: two calls in one turn, matched by call_id, then done."""
    fakes = Path(__file__).parent / "fakes"
    module = runpy.run_path(str(fakes / "openai_fake.py"))
    fake = type(sys)("openai")
    fake.OpenAI = module["OpenAI"]
    monkeypatch.setitem(sys.modules, "openai", fake)
    directory = ROOT / "part2_ch15_assistant"
    monkeypatch.chdir(directory)
    monkeypatch.syspath_prepend(str(directory))
    runpy.run_path(str(directory / "real.py"), run_name="__main__")
    assert "OK after 3 results" in capsys.readouterr().out


def test_ch33_read_gate_never_leaks_another_customers_notes():
    """Core property of Chapter 33: the read gate never returns
    notes that belong to a different customer."""
    directory = ROOT / "part4_ch33_notebook"
    code = (
        "import sys; sys.path.insert(0, '.');"
        "from notebook import add_note;"
        "from recall import recall;"
        "add_note('A', 'flavor', 'likes chocolate', 'customer');"
        "print(len(recall('B', 'chocolate', today='2026-01-01')))"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], cwd=directory,
        capture_output=True, text=True, check=True)
    assert result.stdout.strip() == "0"


def test_ch42_access_filter_and_citations():
    """Chapter 42: the assistant never sees the manager's contract,
    and an answer citing a label that doesn't exist is rejected."""
    directory = ROOT / "part5_ch42_folder"
    code = (
        "import sys; sys.path.insert(0, '.');"
        "from rag import search, answer;"
        "q = 'Is there a penalty if the flour is late?';"
        "print(len(search(q, 'assistant')), len(search(q, 'manager')));"
        "print(answer('How long does the carrot cake stay in the oven?',"
        " 'assistant', lambda q, e: 'Bake for 50 minutes [E7].')[0])"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], cwd=directory,
        capture_output=True, text=True, check=True)
    assert result.stdout.splitlines() == [
        "0 1", "ANSWER WITHOUT A VALID SOURCE"]
