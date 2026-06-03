# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #48 | Milestone Seed: 214
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['if', 'return', 'fn', 'false', 'let', 'else', 'while', 'true']
GENERATION_ROUND_ID = 48
SEED_METRIC_WEIGHT = 214

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.18998641437795827, 4) for x in range(5)]
