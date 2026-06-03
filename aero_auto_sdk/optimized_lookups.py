# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #93 | Milestone Seed: 156
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['while', 'if', 'else', 'return', 'true', 'fn', 'false', 'let']
GENERATION_ROUND_ID = 93
SEED_METRIC_WEIGHT = 156

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.5294506598167954, 4) for x in range(5)]
