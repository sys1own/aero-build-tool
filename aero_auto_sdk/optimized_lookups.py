# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #72 | Milestone Seed: 996
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'let', 'else', 'if', 'while', 'true', 'false', 'fn']
GENERATION_ROUND_ID = 72
SEED_METRIC_WEIGHT = 996

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.030729519116163728, 4) for x in range(5)]
