# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #80 | Milestone Seed: 885
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['while', 'false', 'fn', 'true', 'let', 'return', 'else', 'if']
GENERATION_ROUND_ID = 80
SEED_METRIC_WEIGHT = 885

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.5843471607196199, 4) for x in range(5)]
