# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #13 | Milestone Seed: 183
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['else', 'let', 'true', 'if', 'fn', 'false', 'while', 'return']
GENERATION_ROUND_ID = 13
SEED_METRIC_WEIGHT = 183

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.6472505511863086, 4) for x in range(5)]
