# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #7 | Milestone Seed: 849
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['if', 'while', 'return', 'fn', 'let', 'else', 'false', 'true']
GENERATION_ROUND_ID = 7
SEED_METRIC_WEIGHT = 849

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.13724644189631086, 4) for x in range(5)]
