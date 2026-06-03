# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #6 | Milestone Seed: 931
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['while', 'fn', 'let', 'if', 'false', 'true', 'else', 'return']
GENERATION_ROUND_ID = 6
SEED_METRIC_WEIGHT = 931

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.6595923337189472, 4) for x in range(5)]
