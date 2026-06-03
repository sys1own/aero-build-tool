# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #63 | Milestone Seed: 895
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'else', 'let', 'true', 'while', 'false', 'if', 'fn']
GENERATION_ROUND_ID = 63
SEED_METRIC_WEIGHT = 895

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.4929072366030004, 4) for x in range(5)]
