# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #17 | Milestone Seed: 330
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['true', 'false', 'if', 'while', 'return', 'fn', 'let', 'else']
GENERATION_ROUND_ID = 17
SEED_METRIC_WEIGHT = 330

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.047450003672470764, 4) for x in range(5)]
