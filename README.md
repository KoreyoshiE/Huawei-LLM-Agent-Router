# Huawei LLM Agent Competition: Hardware-Adaptive Orchestration and Tool-Calling Router Framework

This repository documents the production-grade deployment architecture, synthetic data lifecycle, and automated evaluation pipeline developed for the Huawei LLM Agent Development Competition. Engineered around the Qwen3 large language model family (specifically optimized for Qwen3-4B-Instruct), the framework delivers sub-millisecond intent-routing speeds, zero-dependency XML-bounded tool calling, heterogeneous hardware accelerator auto-mapping, and automated multi-turn regression testing.

## Core Engineering Paradigm
Industrial tool-calling applications frequently suffer from severe token inflation, excessive execution latency, and parsing vulnerabilities when dependent on bulky enterprise frameworks like LangChain. These challenges are magnified when deploying on local edge infrastructure or specialized domestic hardware clusters. 

This framework bypasses third-party abstract layers by establishing a lean, high-performance orchestration core. It utilizes a pre-compiled Regular Expression extraction pipeline over explicitly structured XML tokens, backed by rigorous Object-Oriented Programming (OOP) type validation. This design choice guarantees absolute structural enforcement and predictable handling of complex slot dependencies within tight latency bounds.

## Technical Stack Architecture
* **Core Language Model:** Qwen3-4B-Instruct-2507
* **Runtime Environment:** Python 3.13 / PyTorch / Conda Deployment Environment
* **Hardware Interoperability Layer:** Huawei Ascend NPU (`torch_npu`), NVIDIA CUDA, Apple Silicon MPS
* **Ecosystem Utilities:** Transformers, PEFT, ModelScope, Core Python Regex Engines

---

## Workspace Directory Topology
The repository is strictly stratified into isolated, independent functional domains to enforce clean separation of concerns and support industrial product data management (PDM) standards:

```text
Huawei-LLM-Agent-Router/
├── .gitignore                     # Excludes temporary bytecode, local logs, and large weights
├── README.md                      # Unified master technical repository documentation
├── detect.py                      # Pre-flight hardware architecture and dependency validator
├── environment.yaml               # Declarative Conda manifest for cluster replication
├── main.py                        # Standalone interactive CLI shell and smoke test coordinator
├── .vscode/                       # Standardized cross-platform development workspaces
│   ├── c_cpp_properties.json     # IntelliSense workspace specifications
│   ├── launch.json                # Runtime execution and debugging profiles
│   └── settings.json              # Workspace-specific editor formatting variables
├── config/                        # Decoupled system blueprints and declarative definitions
│   └── tools_v0.json              # Hierarchical tool schema definitions and slot constraints
├── core/                          # Core orchestration engines and execution models
│   ├── agent.py                   # High-performance adaptive hardware routing layer
│   └── demo_agent.py              # Baseline architectures (Direct vs. Hierarchical methods)
├── data/                          # Normalized tracking data, smoke arrays, and fine-tuning sets
│   ├── train_data.json            # Base training data payload
│   ├── train_data_50.json         # Partitioned training data slice
│   ├── smoke_test_100.json        # Base smoke test definition matrix
│   ├── single_turn_smoke_test.jsonl # Cleaned single-turn execution traces
│   ├── multi_turn_smoke_test.jsonl  # Cleaned multi-turn dialogue traces
│   ├── eval_train.jsonl           # Structured validation training vectors
│   ├── eval_test.jsonl            # Master analytical testing array
│   ├── eval_test_small10.jsonl    # Accelerated evaluation test grid
│   └── hard_examples.jsonl        # Discovered low-confidence exception data
├── evaluation/                    # Analytics infrastructure and automated testing engines
│   ├── evaluate_agent.py          # Master analytical evaluation pipeline harness
│   ├── bash_run.py                # Batch execution loop runner for test traces
│   ├── analyze_eval_csv.py        # Error log parsing and function alias suggestion utility
│   ├── analyze_failures.py        # Failure taxonomy classifier (mismatches vs. missing slots)
│   └── export_hard_examples.py    # Discrepancy extraction and regression harvesting tool
├── generators/                    # Data synthesis utilities and developer sandboxes
│   ├── Generate.py                # Single-turn procedural data synthesis engine
│   ├── Generate2.py               # Complex multi-tier hierarchical intent prompt generator
│   └── Study.py                   # Sandbox testing utility and syntax validation file
└── logs/                          # System telemetry, evaluation checkpoints, and metrics
    ├── eval_results.json          # Master run evaluation metrics summary
    ├── eval_results.csv           # Tabular structural formatting of current evaluation rounds
    ├── eval_20251022_211206.log   # Raw runtime system execution logs
    └── eval_run_20251022_214904.log # Low-level checkpoint memory shard loading trace
