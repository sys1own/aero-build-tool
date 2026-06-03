# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #62 | Milestone Seed: 775
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['fn', 'true', 'else', 'return', 'false', 'let', 'while', 'if']
GENERATION_ROUND_ID = 62
SEED_METRIC_WEIGHT = 775

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.5932312842374513, 4) for x in range(5)]
