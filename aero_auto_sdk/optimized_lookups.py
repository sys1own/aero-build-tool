# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #15 | Milestone Seed: 409
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['false', 'true', 'let', 'if', 'while', 'return', 'else', 'fn']
GENERATION_ROUND_ID = 15
SEED_METRIC_WEIGHT = 409

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.5440581082760313, 4) for x in range(5)]
