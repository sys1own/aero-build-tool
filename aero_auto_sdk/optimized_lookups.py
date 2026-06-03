# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #24 | Milestone Seed: 252
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['else', 'fn', 'return', 'while', 'false', 'true', 'if', 'let']
GENERATION_ROUND_ID = 24
SEED_METRIC_WEIGHT = 252

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.12206720029763873, 4) for x in range(5)]
