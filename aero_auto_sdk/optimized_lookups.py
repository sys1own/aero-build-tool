# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #97 | Milestone Seed: 290
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['false', 'while', 'true', 'if', 'else', 'let', 'return', 'fn']
GENERATION_ROUND_ID = 97
SEED_METRIC_WEIGHT = 290

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.38378904826978044, 4) for x in range(5)]
