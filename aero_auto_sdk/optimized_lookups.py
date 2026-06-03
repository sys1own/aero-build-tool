# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #38 | Milestone Seed: 249
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'while', 'if', 'false', 'else', 'let', 'fn', 'true']
GENERATION_ROUND_ID = 38
SEED_METRIC_WEIGHT = 249

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.4542292503965787, 4) for x in range(5)]
