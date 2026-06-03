# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #52 | Milestone Seed: 444
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['while', 'fn', 'true', 'false', 'if', 'return', 'else', 'let']
GENERATION_ROUND_ID = 52
SEED_METRIC_WEIGHT = 444

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.7374043824074695, 4) for x in range(5)]
