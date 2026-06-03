# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #1 | Milestone Seed: 450
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['fn', 'let', 'return', 'if', 'false', 'while', 'else', 'true']
GENERATION_ROUND_ID = 1
SEED_METRIC_WEIGHT = 450

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.7638094456552278, 4) for x in range(5)]
