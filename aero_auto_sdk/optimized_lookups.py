# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #92 | Milestone Seed: 590
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['while', 'fn', 'return', 'true', 'else', 'false', 'let', 'if']
GENERATION_ROUND_ID = 92
SEED_METRIC_WEIGHT = 590

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.9408869071751557, 4) for x in range(5)]
