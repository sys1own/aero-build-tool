# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #82 | Milestone Seed: 889
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'let', 'true', 'while', 'fn', 'if', 'else', 'false']
GENERATION_ROUND_ID = 82
SEED_METRIC_WEIGHT = 889

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.46720347878752655, 4) for x in range(5)]
