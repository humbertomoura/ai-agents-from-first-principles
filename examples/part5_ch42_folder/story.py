from rag import search, answer

def show(question, profile):
    print(f"\n{profile}: {question}")
    evidence = search(question, profile)
    for e in evidence:
        print(f"  [{e['id']}] {e['source']}")
    if not evidence:
        print("  (no evidence)")

show("How long does the carrot cake stay in the oven?",
     "assistant")
show("Is there a penalty if the flour is late?", "assistant")
show("Is there a penalty if the flour is late?", "manager")
show("Who won the 2002 World Series?", "assistant")

def right_model(question, evidence):
    return "Bake for 40 minutes at 350 degrees [E1]."

def making_it_up(question, evidence):
    return "Bake for 50 minutes [E7]."

q = "How long does the carrot cake stay in the oven?"
print()
for generate in (right_model, making_it_up):
    status, text = answer(q, "assistant", generate)
    print(f"{status}: {text}")
status, text = answer("Who won the 2002 World Series?",
                      "assistant", right_model)
print(f"{status}: {text}")
