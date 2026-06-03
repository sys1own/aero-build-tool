# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #14 | Milestone Seed: 453
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'let', 'while', 'true', 'if', 'fn', 'else', 'false']
GENERATION_ROUND_ID = 14
SEED_METRIC_WEIGHT = 453

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.2349791484535062, 4) for x in range(5)]
