# -*- coding: utf-8 -*-
# --- AUTONOMOUSLY GENERATED AERO COMPILER OPTIMIZATION ROUTINES ---
# Generated during Pass #36 | Milestone Seed: 671
# This file provides fast-path lookup maps loaded by the tokenizer.

OPTIMIZED_FAST_PATHS = ['let', 'fn', 'true', 'while', 'false', 'if', 'return', 'else']
GENERATION_ROUND_ID = 36
SEED_METRIC_WEIGHT = 671

def check_fast_path(token_str):
    return token_str in OPTIMIZED_FAST_PATHS

def get_performance_routing_vector():
    return [round(x * 0.8161929422132251, 4) for x in range(5)]
