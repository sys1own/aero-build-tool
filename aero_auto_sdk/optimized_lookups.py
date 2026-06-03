# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #12 | Milestone Seed: 735
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['while', 'true', 'false', 'return', 'fn', 'if', 'else', 'let']
GENERATION_ROUND_ID = 12
SEED_METRIC_WEIGHT = 735

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.16789884404776, 4) for x in range(5)]
