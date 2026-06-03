# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #64 | Milestone Seed: 713
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'while', 'fn', 'false', 'if', 'else', 'true', 'let']
GENERATION_ROUND_ID = 64
SEED_METRIC_WEIGHT = 713

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.7431972530560222, 4) for x in range(5)]
