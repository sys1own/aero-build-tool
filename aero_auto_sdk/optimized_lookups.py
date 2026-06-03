# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #45 | Milestone Seed: 599
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['if', 'true', 'let', 'false', 'return', 'else', 'fn', 'while']
GENERATION_ROUND_ID = 45
SEED_METRIC_WEIGHT = 599

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.4032648749902552, 4) for x in range(5)]
