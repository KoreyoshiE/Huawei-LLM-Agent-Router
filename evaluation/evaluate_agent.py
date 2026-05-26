import argparse
import json
import os
import time
import re
from tqdm import tqdm
import csv
from agent import CustomAgent

TOOL_TAG_RE = re.compile(r"<tool>(.*?)</tool>", re.DOTALL)
FUNC_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)\)", re.DOTALL)

def load_data(path):
    samples = []
    if path.endswith(".jsonl"):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    samples.append(json.loads(line))
    else:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # If top-level is a list
            if isinstance(data, list):
                samples = data
            # If it's a dict with list under some keys
            elif isinstance(data, dict):
                # common keys: "data" or top-level list stored as value
                if "data" in data and isinstance(data["data"], list):
                    samples = data["data"]
                else:
                    # fallback: try to treat dict as single sample
                    samples = [data]
    return samples

def extract_expected_assistant(sample):
    """From sample['data'] choose the expected assistant output(s).
       Return list of assistant contents (order preserved)."""
    data = sample.get("data", [])
    assistant_texts = [turn["content"] for turn in data if turn.get("role") == "assistant"]
    return assistant_texts

def build_user_messages(sample):
    """Return list of messages (role, content) for passing to agent.run"""
    data = sample.get("data", [])
    # Keep roles in order, but agent.run expects [{'role':..., 'content':...}, ...]
    messages = [{"role": turn["role"], "content": turn["content"]} for turn in data]
    # Common evaluation uses only the user portion as input; but we'll pass the whole data if needed.
    # For compatibility with many evals, prefer to pass only user messages (first user message) unless multiple rounds.
    user_msgs = [m for m in messages if m["role"] == "user"]
    if len(user_msgs) == 0:
        # fallback: return whole conversation
        return messages
    # Strategy: if it's single-turn eval, just return the first user turn
    return [user_msgs[0]]

def extract_tool_call_from_response(resp_text):
    """Try to extract a tool call string like ConnectBlueTooth(DeviceType="手机", ActionType=True)
       Returns the first found call (string) or None."""
    if not resp_text:
        return None
    # 1) try <tool>...</tool>
    m = TOOL_TAG_RE.search(resp_text)
    if m:
        inner = m.group(1).strip()
        # remove surrounding quotes/backticks if any
        return inner
    # 2) try to find a function-like pattern
    m2 = FUNC_RE.search(resp_text)
    if m2:
        # Return the matched function with args
        func_name = m2.group(1)
        args = m2.group(2).strip()
        return f"{func_name}({args})"
    # 3) fallback: try to return any uppercase function-like token + parentheses searching
    return None

def parse_func_name(call_str):
    if not call_str:
        return None
    m = FUNC_RE.search(call_str)
    if m:
        return m.group(1)
    return None

def normalize_text(s):
    if s is None:
        return ""
    return re.sub(r"\s+", " ", s.strip())

def evaluate(samples, agent, limit=None, verbose=False):
    results = []
    total_time = 0.0
    n = 0
    for sample in tqdm(samples[:limit] if limit else samples):
        n += 1
        sample_id = sample.get("id", f"idx_{n}")
        # Build user input(s) for agent.run
        user_msgs = build_user_messages(sample)
        expected_assistants = extract_expected_assistant(sample)  # list of strings
        expected_primary = expected_assistants[-1] if expected_assistants else ""
        # Call agent and time it
        start = time.time()
        try:
            response = agent.run(user_msgs)
        except Exception as e:
            response = f"[ERROR] {repr(e)}"
        elapsed = time.time() - start
        total_time += elapsed

        norm_resp = normalize_text(response)
        norm_exp = normalize_text(expected_primary)

        # Extract tool calls
        resp_call = extract_tool_call_from_response(response)
        exp_call = extract_tool_call_from_response(expected_primary) or expected_primary

        resp_fn = parse_func_name(resp_call)
        exp_fn = parse_func_name(exp_call)

        # Metrics
        exact_match = (resp_call is not None and normalize_text(resp_call) == normalize_text(exp_call) and exp_call != "")
        contains_match = (norm_exp != "" and norm_exp in norm_resp) or (exp_call and resp_call and normalize_text(exp_call) in normalize_text(resp_call))
        func_name_match = (resp_fn is not None and exp_fn is not None and resp_fn == exp_fn)

        result = {
            "id": sample_id,
            "user_input": user_msgs,
            "expected_assistant": expected_assistants,
            "expected_primary": expected_primary,
            "response_raw": response,
            "response_call": resp_call,
            "response_func": resp_fn,
            "expected_call": exp_call,
            "expected_func": exp_fn,
            "exact_match": exact_match,
            "contains_match": contains_match,
            "func_name_match": func_name_match,
            "time": elapsed
        }
        results.append(result)
        if verbose and not (exact_match or contains_match or func_name_match):
            print("----- FAILED CASE -----")
            print("id:", sample_id)
            print("user:", user_msgs)
            print("expected:", expected_primary)
            print("response:", response)
            print("-----------------------")
    # compute summary
    total = len(results)
    exact_cnt = sum(1 for r in results if r["exact_match"])
    contains_cnt = sum(1 for r in results if r["contains_match"])
    func_cnt = sum(1 for r in results if r["func_name_match"])
    avg_time = total_time / total if total>0 else 0.0

    summary = {
        "total": total,
        "exact_match_count": exact_cnt,
        "contains_match_count": contains_cnt,
        "func_name_match_count": func_cnt,
        "exact_match_rate": exact_cnt/total if total else 0.0,
        "contains_match_rate": contains_cnt/total if total else 0.0,
        "func_name_match_rate": func_cnt/total if total else 0.0,
        "avg_response_time": avg_time
    }
    return results, summary

def save_results_json(results, summary, out_path):
    payload = {"summary": summary, "results": results}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def save_results_csv(results, csv_path):
    keys = ["id","expected_primary","response_raw","response_call","response_func","expected_call","expected_func","exact_match","contains_match","func_name_match","time"]
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for r in results:
            writer.writerow([r.get(k) if k in r else "" for k in keys])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", "-d", required=True, help="Path to data (.json or .jsonl)")
    parser.add_argument("--out", "-o", default="results.json", help="Output JSON results file")
    parser.add_argument("--csv", default=None, help="Optional CSV output")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of samples (0 = all)")
    parser.add_argument("--verbose", action="store_true", help="Print failed cases inline")
    args = parser.parse_args()

    data_path = args.data
    if not os.path.exists(data_path):
        print("Data file not found:", data_path)
        return

    print("Loading data from:", data_path)
    samples = load_data(data_path)
    print("Loaded samples:", len(samples))

    print("Initializing agent (this may load the model)...")
    agent = CustomAgent()
    print("Agent initialized.")

    limit = args.limit if args.limit>0 else None
    results, summary = evaluate(samples, agent, limit=limit, verbose=args.verbose)

    print("Summary:")
    for k,v in summary.items():
        print(f"  {k}: {v}")

    save_results_json(results, summary, args.out)
    print("Saved JSON results to:", args.out)
    if args.csv:
        save_results_csv(results, args.csv)
        print("Saved CSV results to:", args.csv)

if __name__ == "__main__":
    main()
