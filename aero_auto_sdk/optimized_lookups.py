# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #28 | Milestone Seed: 771
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['let', 'if', 'return', 'fn', 'false', 'true', 'else', 'while']
GENERATION_ROUND_ID = 28
SEED_METRIC_WEIGHT = 771

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.599143594591838, 4) for x in range(5)]
