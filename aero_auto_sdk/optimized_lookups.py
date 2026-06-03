# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #83 | Milestone Seed: 609
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['let', 'if', 'else', 'return', 'false', 'true', 'fn', 'while']
GENERATION_ROUND_ID = 83
SEED_METRIC_WEIGHT = 609

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.4755807868550065, 4) for x in range(5)]
