# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #41 | Milestone Seed: 860
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['else', 'fn', 'false', 'while', 'let', 'if', 'true', 'return']
GENERATION_ROUND_ID = 41
SEED_METRIC_WEIGHT = 860

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.5078946023755512, 4) for x in range(5)]
