# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #86 | Milestone Seed: 257
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['true', 'while', 'return', 'if', 'false', 'fn', 'else', 'let']
GENERATION_ROUND_ID = 86
SEED_METRIC_WEIGHT = 257

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.24852447528970134, 4) for x in range(5)]
