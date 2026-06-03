# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #94 | Milestone Seed: 408
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['true', 'else', 'while', 'fn', 'false', 'if', 'let', 'return']
GENERATION_ROUND_ID = 94
SEED_METRIC_WEIGHT = 408

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.3571219903827214, 4) for x in range(5)]
