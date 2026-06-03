# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #91 | Milestone Seed: 155
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['while', 'return', 'let', 'true', 'fn', 'else', 'false', 'if']
GENERATION_ROUND_ID = 91
SEED_METRIC_WEIGHT = 155

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.049352001696005066, 4) for x in range(5)]
