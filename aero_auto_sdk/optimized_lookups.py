# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #100 | Milestone Seed: 350
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['return', 'if', 'else', 'let', 'while', 'true', 'false', 'fn']
GENERATION_ROUND_ID = 100
SEED_METRIC_WEIGHT = 350

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.21931092647940864, 4) for x in range(5)]
