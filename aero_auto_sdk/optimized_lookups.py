# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #98 | Milestone Seed: 441
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['fn', 'false', 'let', 'true', 'while', 'return', 'if', 'else']
GENERATION_ROUND_ID = 98
SEED_METRIC_WEIGHT = 441

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.22354404795252036, 4) for x in range(5)]
