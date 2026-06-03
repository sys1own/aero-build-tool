# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #89 | Milestone Seed: 398
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['true', 'fn', 'return', 'if', 'else', 'let', 'while', 'false']
GENERATION_ROUND_ID = 89
SEED_METRIC_WEIGHT = 398

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.2552474093517214, 4) for x in range(5)]
