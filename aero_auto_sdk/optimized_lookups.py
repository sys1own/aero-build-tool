# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #9 | Milestone Seed: 221
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['fn', 'return', 'true', 'false', 'let', 'if', 'else', 'while']
GENERATION_ROUND_ID = 9
SEED_METRIC_WEIGHT = 221

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.07278587764070243, 4) for x in range(5)]
