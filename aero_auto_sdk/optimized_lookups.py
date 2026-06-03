# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #60 | Milestone Seed: 772
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['let', 'return', 'if', 'fn', 'else', 'false', 'true', 'while']
GENERATION_ROUND_ID = 60
SEED_METRIC_WEIGHT = 772

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.1065139295231673, 4) for x in range(5)]
