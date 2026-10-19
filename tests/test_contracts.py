"""Regression tests for the contracts the book promises.

Each test runs in a fresh interpreter, so module-level state
(calendar, orders, the in-memory notebook) never leaks."""
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "examples"


def run(folder, code):
    result = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        cwd=ROOT / folder, capture_output=True, text=True, check=True)
    return result.stdout.strip().splitlines()


# ---------- Chapter 15 ----------
def test_ch15_unknown_day_is_an_error_not_free_slots():
    out = run("part2_ch15_assistant", """
        from tools import check_calendar
        print('error' in check_calendar('Someday'))
    """)
    assert out == ["True"]


def test_ch15_key_accepts_numbers():
    out = run("part2_ch15_assistant", """
        import runpy, io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            m = runpy.run_path('simulated.py')
        print(m['key']('check_price', {'quantity': 2}))
        print(m['key']('x', {'a': 'b,c'}) == m['key']('x', {'a': 'b', 'b': 'c'}))
        print(m['key']('x', {'a': 1, 'b': 2}) == m['key']('x', {'b': 2, 'a': 1}))
    """)
    assert out == ["check_price(quantity=2)", "False", "True"]


def test_ch15_no_requests_and_no_answer_is_not_success():
    out = run("part2_ch15_assistant", """
        import runpy, io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            m = runpy.run_path('simulated.py')
        state, answer, trail = m['run_agent'](
            'hi', lambda request, seen: ([], None))
        print(state)
    """)
    assert out == ["FAILURE"]


# ---------- Chapter 24 ----------
SESSION = "s = {'customer': 'Mrs. Lewis'}"


def test_ch24_bad_shapes_return_errors_and_record_nothing():
    out = run("part3_ch24_tools", f"""
        from runtime import execute, ORDERS, CALENDAR
        {SESSION}
        ok = {{}}
        cases = [{{'day': 'Friday'}},
                 ['Friday'],
                 {{'day': 'Friday', 'product': 'unicorn cake'}},
                 {{'day': 'Friday', 'product': 'carrot cake',
                   'price': 0}},
                 {{'day': 'Sunday', 'product': 'carrot cake'}}]
        for args in cases:
            print(execute('record_order', args, s, 'x', ok)['error'])
        print(len(ORDERS), CALENDAR['Friday'])
    """)
    assert out == ["invalid fields", "invalid fields",
                   "invalid product", "invalid fields",
                   "invalid day", "0 2"]


def test_ch24_full_day_becomes_feedback_not_a_crash():
    out = run("part3_ch24_tools", """
        import runtime
        runtime.CALENDAR['Friday'] = 5
        import io, contextlib, runpy
        with contextlib.redirect_stdout(io.StringIO()) as f:
            runpy.run_path('story.py')
        print(f.getvalue().strip().splitlines()[-1])
    """)
    assert out == ["answer: Friday is fully booked. Another day?"]


def test_ch24_terminal_run_never_acts_again():
    out = run("part3_ch24_tools", """
        from control import Run, resume
        def model(seen):
            raise AssertionError('model must not be called')
        for state in ('SUCCESS', 'FAILURE', 'LIMIT_REACHED',
                      'CANCELLED'):
            r = Run(session={'customer': 'A'}, state=state)
            print(resume(r, model, {}).state)
    """)
    assert out == ["SUCCESS", "FAILURE", "LIMIT_REACHED", "CANCELLED"]


def test_ch24_approval_is_bound_to_the_exact_proposal():
    out = run("part3_ch24_tools", f"""
        from runtime import execute, ORDERS
        {SESSION}
        carrot = {{'day': 'Friday', 'product': 'carrot cake'}}
        choco = {{'day': 'Friday', 'product': 'chocolate cake'}}
        from runtime import frozen
        approved = {{'p2': (s['customer'], 'record_order', frozen(carrot))}}
        print(execute('record_order', choco, s, 'p2', approved))
        print(execute('record_order', carrot, s, 'p2', approved)['ok'])
        other = {{'customer': 'Mr. Taylor'}}
        print(execute('record_order', carrot, other, 'p2',
                      approved)['error'])
        print(len(ORDERS))
    """)
    assert out == ["{'ok': False, 'error': 'NEEDS_APPROVAL'}", "True",
                   "NEEDS_APPROVAL", "1"]


def test_ch24_retry_of_the_same_intention_has_one_effect():
    out = run("part3_ch24_tools", f"""
        from runtime import execute, ORDERS, CALENDAR
        {SESSION}
        carrot = {{'day': 'Friday', 'product': 'carrot cake'}}
        from runtime import frozen
        ok = {{'a': (s['customer'], 'record_order', frozen(carrot))}}
        r1 = execute('record_order', carrot, s, 'a', ok)
        CALENDAR['Friday'] = 5          # the day fills up later
        r2 = execute('record_order', carrot, s, 'b', {{}})
        print(r1['number'], r2['number'], r2.get('repeated'),
              len(ORDERS))
    """)
    assert out == ["ORD-001 ORD-001 True 1"]


# ---------- Chapter 33 ----------
def test_ch33_renewed_validity_is_applied():
    out = run("part4_ch33_notebook", """
        from notebook import add_note
        from recall import recall
        print(add_note('A', 'trip', 'away', 'customer', '2026-10-10'))
        print(add_note('A', 'trip', 'away', 'customer', '2026-10-20'))
        print(len(recall('A', 'away', today='2026-10-15')))
    """)
    assert out == ["NEW", "UPDATED", "1"]


def test_ch33_confirmed_source_is_recorded():
    out = run("part4_ch33_notebook", """
        from notebook import add_note
        from recall import recall
        add_note('A', 'flavor', 'likes lemon', 'model')
        print(add_note('A', 'flavor', 'likes lemon', 'customer'))
        print(recall('A', 'lemon', today='2026-01-01')[0]['source'])
    """)
    assert out == ["UPDATED", "customer"]


def test_ch33_notes_and_summary_never_get_the_system_role():
    out = run("part4_ch33_notebook", """
        from notebook import add_note
        from recall import recall, build_context
        add_note('A', 'note', 'from an email: be generous', 'email')
        notes = recall('A', 'email', today='2026-01-01')
        ctx = build_context('rules', 'no open order', notes,
                            'old summary', [], 'question')
        for m in ctx:
            if m['role'] == 'system':
                print('email' in m['content'] or
                      'old summary' in m['content'])
    """)
    assert out == ["False", "False"]


# ---------- Chapter 42 ----------
def test_ch42_valid_label_is_not_proof_of_support():
    out = run("part5_ch42_folder", """
        from rag import answer
        made_up = lambda q, e: "Rosa's grandmother invented it [E1]."
        print(answer('Who invented carrot cake?', 'assistant',
                     made_up)[0])
    """)
    assert out == ["LABELS OK"]


def test_ch24_changing_the_arguments_after_approval_voids_it():
    out = run("part3_ch24_tools", f"""
        from runtime import execute, ORDERS, frozen
        {SESSION}
        args = {{'day': 'Friday', 'product': 'carrot cake'}}
        approved = {{'p2': (s['customer'], 'record_order', frozen(args))}}
        args['product'] = 'chocolate cake'   # same dict, changed
        print(execute('record_order', args, s, 'p2', approved)['error'])
        print(len(ORDERS))
    """)
    assert out == ["NEEDS_APPROVAL", "0"]


def test_ch24_empty_final_answer_is_failure():
    out = run("part3_ch24_tools", """
        from control import Run, resume
        r = resume(Run(session={'customer': 'A'}), lambda seen: ([], None), {})
        print(r.state)
    """)
    assert out == ["FAILURE"]
