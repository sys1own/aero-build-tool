# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #5 | Milestone Seed: 283
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['if', 'false', 'else', 'fn', 'let', 'return', 'while', 'true']
GENERATION_ROUND_ID = 5
SEED_METRIC_WEIGHT = 283

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.18082005025939263, 4) for x in range(5)]
