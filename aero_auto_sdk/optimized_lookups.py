# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #66 | Milestone Seed: 459
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['true', 'if', 'let', 'fn', 'while', 'return', 'false', 'else']
GENERATION_ROUND_ID = 66
SEED_METRIC_WEIGHT = 459

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.1276501498840541, 4) for x in range(5)]
