# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #20 | Milestone Seed: 466
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['false', 'if', 'fn', 'let', 'true', 'else', 'while', 'return']
GENERATION_ROUND_ID = 20
SEED_METRIC_WEIGHT = 466

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.4622483970783281, 4) for x in range(5)]
