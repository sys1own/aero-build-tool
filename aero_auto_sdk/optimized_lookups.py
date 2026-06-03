# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #47 | Milestone Seed: 871
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['if', 'let', 'while', 'false', 'fn', 'true', 'return', 'else']
GENERATION_ROUND_ID = 47
SEED_METRIC_WEIGHT = 871

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.7713621069888802, 4) for x in range(5)]
