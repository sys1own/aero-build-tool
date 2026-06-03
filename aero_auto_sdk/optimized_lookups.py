# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #40 | Milestone Seed: 266
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['while', 'fn', 'true', 'false', 'return', 'else', 'let', 'if']
GENERATION_ROUND_ID = 40
SEED_METRIC_WEIGHT = 266

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.47904801886055737, 4) for x in range(5)]
