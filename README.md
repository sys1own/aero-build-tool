# Aero Build Tool

A zero-dependency, concurrent build orchestrator and task runner written entirely in pure Python.

Aero is designed for developers who need a lightweight, hyper-fast way to run build pipelines and task graphs without bloating their codebases or CI/CD environments with heavy external runtimes or third-party packages.

---

## Key Features

- **Zero Dependencies:** Built strictly on the Python standard library (`hashlib`, `concurrent.futures`, `json`, etc.). No `pip install` required for core features.
- **Smart Concurrency (DAG Execution):** Models your tasks as a Directed Acyclic Graph (DAG) and executes independent branches concurrently using dynamic thread pools.
- **Cycle Interception:** Uses a robust 3-state graph coloring algorithm to detect and stop circular dependencies before execution starts.
- **Incremental Rebuilds:** Calculates SHA-256 cryptographic hashes of your input files to monitor on-disk deltas. Tasks are short-circuited and skipped if neither they nor their upstream dependencies have changed.
- **Clean Command Line Interface:** Built-in CLI commands to run builds, check execution state, and inspect your pipeline.

---

## How It Works

Aero evaluates your project's pipeline as a topological graph:
