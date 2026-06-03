# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #101 | Milestone Seed: 505
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['while', 'else', 'true', 'false', 'return', 'fn', 'let', 'if']
GENERATION_ROUND_ID = 101
SEED_METRIC_WEIGHT = 505

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.8802743855921121, 4) for x in range(5)]
