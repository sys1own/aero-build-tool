# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #53 | Milestone Seed: 446
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['let', 'fn', 'true', 'else', 'while', 'if', 'return', 'false']
GENERATION_ROUND_ID = 53
SEED_METRIC_WEIGHT = 446

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.3769745312802063, 4) for x in range(5)]
