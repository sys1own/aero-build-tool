# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #37 | Milestone Seed: 207
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['fn', 'while', 'false', 'return', 'let', 'else', 'if', 'true']
GENERATION_ROUND_ID = 37
SEED_METRIC_WEIGHT = 207

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.6114961602752489, 4) for x in range(5)]
