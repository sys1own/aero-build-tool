# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #76 | Milestone Seed: 627
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['let', 'while', 'if', 'true', 'return', 'else', 'fn', 'false']
GENERATION_ROUND_ID = 76
SEED_METRIC_WEIGHT = 627

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.8609291612120673, 4) for x in range(5)]
