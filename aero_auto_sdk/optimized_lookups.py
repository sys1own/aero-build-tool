# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #3 | Milestone Seed: 394
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['let', 'return', 'true', 'if', 'else', 'fn', 'while', 'false']
GENERATION_ROUND_ID = 3
SEED_METRIC_WEIGHT = 394

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.2631158568343931, 4) for x in range(5)]
