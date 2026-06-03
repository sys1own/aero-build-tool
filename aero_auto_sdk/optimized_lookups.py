# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #74 | Milestone Seed: 190
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['false', 'let', 'fn', 'if', 'else', 'while', 'true', 'return']
GENERATION_ROUND_ID = 74
SEED_METRIC_WEIGHT = 190

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.7296548909494214, 4) for x in range(5)]
