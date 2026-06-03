# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #54 | Milestone Seed: 195
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['true', 'else', 'while', 'let', 'fn', 'return', 'if', 'false']
GENERATION_ROUND_ID = 54
SEED_METRIC_WEIGHT = 195

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.5645318552963066, 4) for x in range(5)]
