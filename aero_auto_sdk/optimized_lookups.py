# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #35 | Milestone Seed: 790
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['false', 'while', 'let', 'else', 'return', 'fn', 'if', 'true']
GENERATION_ROUND_ID = 35
SEED_METRIC_WEIGHT = 790

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.5888616916909478, 4) for x in range(5)]
