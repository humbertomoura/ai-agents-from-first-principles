from types import SimpleNamespace as N
class _R:
    def __init__(s): s.n=0
    def create(s, **kw):
        s.n+=1
        if s.n==1:
            return N(output=[N(type="function_call",name="check_calendar",arguments='{"day":"Saturday"}',call_id="c1"),
                             N(type="function_call",name="check_price",arguments='{"product":"carrot cake"}',call_id="c2")],output_text="")
        if s.n==2:
            return N(output=[N(type="function_call",name="check_calendar",arguments='{"day":"Friday"}',call_id="c3")],output_text="")
        outs=[h for h in kw["input"] if isinstance(h,dict) and h.get("type")=="function_call_output"]
        return N(output=[N(type="message")],output_text="OK after "+str(len(outs))+" results: "+outs[-1]["output"])
class OpenAI:
    def __init__(s): s.responses=_R()
