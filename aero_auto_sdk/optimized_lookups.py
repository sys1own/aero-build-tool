# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #95 | Milestone Seed: 519
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['else', 'fn', 'let', 'true', 'false', 'while', 'if', 'return']
GENERATION_ROUND_ID = 95
SEED_METRIC_WEIGHT = 519

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.8294395892115662, 4) for x in range(5)]
