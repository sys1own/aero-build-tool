# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #25 | Milestone Seed: 881
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'let', 'fn', 'true', 'else', 'if', 'false', 'while']
GENERATION_ROUND_ID = 25
SEED_METRIC_WEIGHT = 881

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.44564932687071035, 4) for x in range(5)]
