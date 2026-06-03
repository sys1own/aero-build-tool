# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #34 | Milestone Seed: 385
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['else', 'if', 'fn', 'let', 'return', 'while', 'true', 'false']
GENERATION_ROUND_ID = 34
SEED_METRIC_WEIGHT = 385

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.23456932820689413, 4) for x in range(5)]
