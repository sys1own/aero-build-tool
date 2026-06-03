# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #4 | Milestone Seed: 126
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'while', 'if', 'let', 'fn', 'false', 'else', 'true']
GENERATION_ROUND_ID = 4
SEED_METRIC_WEIGHT = 126

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.3224687237329118, 4) for x in range(5)]
