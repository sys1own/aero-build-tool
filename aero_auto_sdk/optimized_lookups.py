# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #77 | Milestone Seed: 957
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['let', 'if', 'else', 'while', 'return', 'true', 'false', 'fn']
GENERATION_ROUND_ID = 77
SEED_METRIC_WEIGHT = 957

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.46076127243727083, 4) for x in range(5)]
