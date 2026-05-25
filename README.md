Huawei-LLM-Agent-Router/
├── .gitignore                     # Prevents tracking compiled bytes and OS metadata
├── README.md                      # Unified master repository documentation
├── detect.py                      # Pre-flight hardware and dependency validator
├── environment.yaml               # Conda environment manifest for cluster replication
├── main.py                        # Standalone interactive CLI user interface loop
├── .vscode/                       # Standardized workspace configurations
│   ├── c_cpp_properties.json
│   ├── launch.json
│   └── settings.json
├── config/                        # Schema catalogs and declarations
│   └── tools_v0.json              # Structured hierarchical intent system definitions
├── core/                          # Core execution engines and agent bindings
│   ├── agent.py                   # High-performance adaptive hardware routing layer
│   └── demo_agent.py              # Baseline architecture (Direct vs. Hierarchical)
├── data/                          # Unified evaluation and fine-tuning datasets
│   ├── train_data.json            # Base training data payload
│   ├── train_data_50.json         # Partitioned training data slice
│   ├── smoke_test_100.json        # Base smoke test definition matrix
│   ├── single_turn_smoke_test.jsonl # Normalized from 'µ•¬÷-√∞—Ã≤‚ ‘ºØ.jsonl'
│   ├── multi_turn_smoke_test.jsonl  # Normalized from '∂‡¬÷-√∞—Ã≤‚ ‘ºØ.jsonl'
│   ├── eval_train.jsonl           # Structured validation training vectors
│   ├── eval_test.jsonl            # Comprehensive test dataset
│   ├── eval_test_small10.jsonl    # Accelerated validation testing slice
│   └── hard_examples.jsonl        # Discovered low-confidence exception data
├── evaluation/                    # Analytics engines and verification runners
│   ├── evaluate_agent.py          # Master analytical evaluation pipeline execution harness
│   ├── bash_run.py                # Batch dataset testing pipeline orchestration entry
│   ├── analyze_eval_csv.py        # Log processor and function alias suggestion engine
│   ├── analyze_failures.py        # Failure classification engine (mismatches vs. missing)
│   └── export_hard_examples.py    # Discrepancy isolation and extraction script
├── generators/                    # Synthetic data generation and utility engines
│   ├── Generate.py                # Single-turn procedural data synthesis engine
│   ├── Generate2.py               # Complex multi-tier hierarchical prompt generator
│   └── Study.py                   # Sandbox utility and script validation suite
├── logs/                          # System telemetry and validation benchmarks
│   ├── eval_results.json          # Master run performance metrics matrix
│   ├── eval_results.csv           # Tabular formatting of current validation round
│   ├── eval_20251022_211206.log   # Raw system trace logs
│   ├── eval_run_20251022_214904.log # Low-level checkpoint memory shards loading trace
│   ├── eval_details_20251027_213114.csv
│   └── eval_details_20251027_223945.csv
└── scripts/                       # Native environment execution tooling
    ├── download.sh                # Automated ModelScope model shard ingestion script
    ├── start.sh                   # POSIX system background execution engine
    └── Lanuch_main.command       # macOS Finder automation executable
