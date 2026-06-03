# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #2 | Milestone Seed: 821
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['fn', 'else', 'while', 'return', 'let', 'if', 'true', 'false']
GENERATION_ROUND_ID = 2
SEED_METRIC_WEIGHT = 821

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.3151781926294409, 4) for x in range(5)]
