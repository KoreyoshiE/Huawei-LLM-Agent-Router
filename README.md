# Huawei LLM Agent Competition: Adaptive Hardware-Agnostic Tool Calling Router Framework

This repository documents the production-grade deployment architecture developed for the Huawei LLM Agent Development Competition. The project implements a lightweight, zero-dependency tool-calling orchestration framework engineered around the Qwen3 large language model family, featuring native multi-platform hardware acceleration mapping and object-oriented dynamic interface routing.

## Project Vision and Engineering Constraints
Modern enterprise agent toolkits (e.g., LangChain) often introduce substantial token inflation, framework overhead, and excessive network latencies, rendering them unsuited for latency-critical or edge deployment environments. This system addresses these limitations by achieving sub-millisecond function-routing processing speeds through compiled regular expression pattern matching over structured XML tags, backed by strict Object-Oriented Programming (OOP) engineering boundaries.

## Production-Ready Directory Structure
The workspace is stratified into independent lifecycle domains to optimize maintainability and facilitate modular code inspections:
```text
Huawei-LLM-Agent-Router/
├── README.md                      # Architectural overview and platform deployment specifications
├── main.py                        # Interactive runtime assessment pipeline
├── agent.py                       # Runtime CustomAgent core and multi-hardware driver abstract layer
├── detect.py                      # Automated diagnostic dependency and runtime validator
├── .vscode/                       # Standardized workspace parameters and compilation settings
│   ├── c_cpp_properties.json
│   ├── launch.json
│   └── settings.json
├── config/                        # Decoupled business rules and tool schema catalog
│   └── tools_v0.json              # Declarative JSON-Schema specifications for tool entities
├── tests/                         # Automated verification and isolation scripts
│   └── test_agent_detection.py    # Declarative regression unit testing ledger
└── scripts/                       # Cross-platform orchestration automation wrappers
    ├── start.sh                   # POSIX-compliant automated environment initialization
    └── Lanuch_main.command       # macOS double-click deployment shortcut
