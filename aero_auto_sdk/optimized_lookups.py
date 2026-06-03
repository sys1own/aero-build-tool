# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #90 | Milestone Seed: 135
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['else', 'while', 'if', 'true', 'let', 'fn', 'false', 'return']
GENERATION_ROUND_ID = 90
SEED_METRIC_WEIGHT = 135

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.6362358091471916, 4) for x in range(5)]
