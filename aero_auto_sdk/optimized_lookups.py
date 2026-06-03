# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #55 | Milestone Seed: 380
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['else', 'false', 'return', 'fn', 'while', 'true', 'if', 'let']
GENERATION_ROUND_ID = 55
SEED_METRIC_WEIGHT = 380

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.5405218316406867, 4) for x in range(5)]
