# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #23 | Milestone Seed: 781
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'else', 'if', 'true', 'fn', 'let', 'false', 'while']
GENERATION_ROUND_ID = 23
SEED_METRIC_WEIGHT = 781

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.17218584783014845, 4) for x in range(5)]
