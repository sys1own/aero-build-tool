# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #29 | Milestone Seed: 406
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'false', 'if', 'else', 'true', 'let', 'while', 'fn']
GENERATION_ROUND_ID = 29
SEED_METRIC_WEIGHT = 406

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.19819156497887058, 4) for x in range(5)]
