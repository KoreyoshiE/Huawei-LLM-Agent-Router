# analyze_failures.py
import json
import re
from collections import defaultdict
import argparse
import os

FUNC_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.DOTALL)

def load_jsonl(p):
    out=[]
    with open(p,"r",encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if line:
                out.append(json.loads(line))
    return out

def detect_type(item):
    # item has keys: id,instruction,output,response
    expected = item.get("output","")
    resp = item.get("response","")
    # check if model used tool (starts with 模型决定调用工具： or contains function pattern)
    if isinstance(resp,str) and ("模型决定调用工具" in resp or "<tool>" in resp or "(" in resp):
        # try extract function names
        m_e = FUNC_RE.search(expected)
        m_r = FUNC_RE.search(resp)
        fn_e = m_e.group(1) if m_e else None
        fn_r = m_r.group(1) if m_r else None
        if fn_e and fn_r:
            if fn_e == fn_r:
                # same function name -> parameter issue vs formatting
                # check if args text equal ignoring quotes and spacing
                e_args = expected[expected.find("(")+1:expected.rfind(")")] if "(" in expected else ""
                r_args = resp[resp.find("(")+1:resp.rfind(")")] if "(" in resp else ""
                norm_e = re.sub(r"[\s'\"]+","",e_args)
                norm_r = re.sub(r"[\s'\"]+","",r_args)
                if norm_e == norm_r:
                    return "format_diff"  # same content, just formatting (quotes/ordering)
                else:
                    # check missing keys
                    keys_e = re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", e_args)
                    keys_r = re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", r_args)
                    if set(keys_e) == set(keys_r):
                        return "param_value_diff"
                    elif set(keys_r).issubset(set(keys_e)):
                        return "param_missing"
                    else:
                        return "param_mismatch"
            else:
                return "fn_name_mismatch"
        else:
            return "unknown_tool_format"
    else:
        # model didn't use tool (natural language reply)
        return "no_tool_used"

def summarize(items):
    stats = defaultdict(list)
    for it in items:
        t = detect_type(it)
        stats[t].append(it)
    return stats

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True, help="hard_examples.jsonl")
    args=parser.parse_args()
    p=args.inp
    if not os.path.exists(p):
        print("文件不存在:",p); return
    items = load_jsonl(p)
    stats = summarize(items)
    print("总样本数:", len(items))
    for k,v in sorted(stats.items(), key=lambda x:-len(x[1])):
        print(f"{k}: {len(v)}")
    print("\n各类示例（每类最多 3 条）：")
    for k,v in stats.items():
        print("\n===",k,"===")
        for ex in v[:3]:
            print(json.dumps(ex, ensure_ascii=False))
    # write per-type files
    base = os.path.splitext(p)[0]
    for k,v in stats.items():
        out = base + f".{k}.jsonl"
        with open(out,"w",encoding="utf-8") as f:
            for it in v:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
        print("wrote", out)

if __name__=="__main__":
    main()
