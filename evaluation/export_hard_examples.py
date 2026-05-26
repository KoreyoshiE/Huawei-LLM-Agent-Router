import argparse
import json
import os
from typing import List

def load_eval(path: str):
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    # payload may contain "results" or be a list
    if isinstance(payload, dict) and "results" in payload:
        return payload["results"], payload.get("summary", {})
    if isinstance(payload, list):
        return payload, {}
    raise ValueError("Unrecognized eval_results.json format")

def first_user_text(user_msgs):
    # user_msgs is a list like [{"role":"user","content":"..."}, ...] or agent stored differently
    if not user_msgs:
        return ""
    # if it's a list of dicts
    if isinstance(user_msgs, list):
        for m in user_msgs:
            if isinstance(m, dict) and m.get("role") == "user":
                return m.get("content","")
        # fallback: if items are strings
        first = user_msgs[0]
        if isinstance(first, dict) and "content" in first:
            return first["content"]
        return str(first)
    # if stored as string
    return str(user_msgs)

def export_failed(eval_results: List[dict], out_path: str, criterion: str = "exact_false", limit: int = 0):
    """
    criterion:
      - exact_false: select records where exact_match == False
      - no_contains: select where contains_match == False
      - func_mismatch: select where func_name_match == False
      - all_failed: not exact_match and not contains_match
    """
    selected = []
    for r in eval_results:
        exact = r.get("exact_match", False)
        contains = r.get("contains_match", False)
        func = r.get("func_name_match", False)

        choose = False
        if criterion == "exact_false":
            choose = not exact
        elif criterion == "no_contains":
            choose = not contains
        elif criterion == "func_mismatch":
            choose = not func
        elif criterion == "all_failed":
            choose = (not exact) and (not contains)
        else:
            choose = not exact

        if choose:
            # Build a training-style record
            user_msgs = r.get("user_input", [])
            if isinstance(user_msgs, list) and len(user_msgs) > 0:
                # try to extract first user content
                inst = first_user_text(user_msgs)
            else:
                inst = r.get("user_input", "")
            expected = r.get("expected_primary", "") or (r.get("expected_assistant", [""])[-1] if r.get("expected_assistant") else "")
            response = r.get("response_raw", "")
            item = {
                "id": r.get("id", ""),
                "instruction": inst,
                "output": expected,
                "response": response
            }
            selected.append(item)
            if limit and len(selected) >= limit:
                break

    # write JSONL
    with open(out_path, "w", encoding="utf-8") as fo:
        for it in selected:
            fo.write(json.dumps(it, ensure_ascii=False) + "\n")
    return len(selected)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval", required=True, help="Path to eval_results.json")
    parser.add_argument("--out", default="hard_examples.jsonl", help="Output jsonl path")
    parser.add_argument("--criterion", choices=["exact_false","no_contains","func_mismatch","all_failed"], default="exact_false", help="Which failed cases to export")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of exported cases (0 = all)")
    args = parser.parse_args()

    if not os.path.exists(args.eval):
        print("Eval results file not found:", args.eval)
        return

    results, summary = load_eval(args.eval)
    total = len(results)
    print(f"Loaded {total} eval records; summary: {summary}")

    count = export_failed(results, args.out, criterion=args.criterion, limit=args.limit)
    print(f"Exported {count} failed cases to {args.out}")

if __name__ == "__main__":
    main()
