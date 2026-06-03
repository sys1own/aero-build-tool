# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #27 | Milestone Seed: 300
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'else', 'if', 'false', 'true', 'fn', 'while', 'let']
GENERATION_ROUND_ID = 27
SEED_METRIC_WEIGHT = 300

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.4582226852295075, 4) for x in range(5)]
