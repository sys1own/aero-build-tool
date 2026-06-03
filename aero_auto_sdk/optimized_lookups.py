# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #26 | Milestone Seed: 499
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['if', 'false', 'true', 'let', 'while', 'return', 'else', 'fn']
GENERATION_ROUND_ID = 26
SEED_METRIC_WEIGHT = 499

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.025667956847130302, 4) for x in range(5)]
