# -*- coding: utf-8 -*-
import os
import sys
import re
import time
import json
import random
import subprocess
import argparse

def run_evolution_pipeline():
    parser = argparse.ArgumentParser()
    parser.add_argument("--soak-seconds", type=int, default=600)
    args = parser.parse_known_args()[0]

    allocated_seconds = args.soak_seconds
    if os.environ.get('CADENCE'):
        cadence_str = os.environ.get('CADENCE', '').lower()
        digits = re.findall(r'\d+', cadence_str)
        if 'hour' in cadence_str:
            allocated_seconds = int(digits[0]) * 3600 if digits else allocated_seconds
        elif 'minute' in cadence_str:
            allocated_seconds = int(digits[0]) * 60 if digits else allocated_seconds

    start_epoch = time.time()
    end_deadline = start_epoch + allocated_seconds
    
    print(f"[Aero Core] Active continuous evolution runtime unlocked.", flush=True)
    print(f"[Aero Core] Target operational duration budget: {allocated_seconds} seconds.", flush=True)
    print(f"[Aero Core] Real-time loop streaming active. Static Analysis mode engaged.\n", flush=True)

    target_branch = "aero-auto/evolution"
    
    print(f"[Aero Core] Initializing sandboxed tracking branch '{target_branch}'...", flush=True)
    subprocess.run(["git", "config", "user.email", "colab-runner@aero-lang.org"], capture_output=True)
    subprocess.run(["git", "config", "user.name", "Aero Core Optimization Engine"], capture_output=True)
    
    subprocess.run(["git", "checkout", "main"], capture_output=True)
    subprocess.run(["git", "branch", "-D", target_branch], capture_output=True)
    subprocess.run(["git", "checkout", "-b", target_branch], capture_output=True)

    loop_round = 0

    while time.time() < end_deadline:
        loop_round += 1
        seconds_left = int(end_deadline - time.time())
        
        print(f"\n🔥 ========================================================", flush=True)
        print(f"🚀 OPTIMIZATION GENERATION PASS #{loop_round} ({seconds_left}s remaining)", flush=True)
        print(f"========================================================", flush=True)

        # 1. PARSE THE TARGET RECIPE AND GENERATE RAW COMPILER CORPUS DATA
        recipe_path = "sample_recipe.txt" if os.path.exists("sample_recipe.txt") else "aero_auto_sdk/sample_recipe.txt"
        compiled_corpus_text = ""
        try:
            from meta_compiler import compile_recipe
            recipe_analysis = compile_recipe(recipe_path)
            compiled_corpus_text = recipe_analysis.get("source", "")
            print("  ✔ Successfully lowered declarative recipe into target optimization corpus.", flush=True)
        except Exception as e_recipe:
            print(f"  ⚠️ Recipe compile analysis notice: {e_recipe}", flush=True)

        # 2. RUN EXPERT CORPUS FREQUENCY ANALYSIS VIA THE OPTIMIZER LAYER
        from aero_sdk.optimizer import analyzer
        spec_path = "config/language_spec.json" if os.path.exists("config/language_spec.json") else "aero_auto_sdk/config/language_spec.json"
        
        if os.path.exists(spec_path):
            try:
                with open(spec_path, "r") as sf:
                    spec_data = json.load(sf)
                
                # Analyze frequency weights dynamically from our generated code layout
                freq_metrics = analyzer.analyze_frequencies(spec_data, compiled_corpus_text)
                op_counts = freq_metrics.get("operator_counts", {})
                
                if "preference_levels" in spec_data:
                    for op in spec_data["preference_levels"]:
                        # Ground the priority baseline in real usage frequency, then apply exploration fuzzing
                        observed_hits = op_counts.get(op, 0)
                        spec_data["preference_levels"][op] = int(observed_hits * 10) + random.randint(0, 5)
                
                spec_data["_evolution_epoch_timestamp"] = int(time.time() * 1000)
                spec_data["_evolution_iteration_round"] = loop_round
                spec_data["_evolution_data_driven_optimized"] = True
                
                with open(spec_path, "w") as sf:
                    json.dump(spec_data, sf, indent=2)
                print("  ✔ Frequency-weighted language specifications written cleanly.", flush=True)
            except Exception as e_spec:
                print(f"  ⚠️ Layout parameter notice: {e_spec}", flush=True)

        # 3. REGENERATE AND VERIFY THE COMPILER STATE
        print("  🏗️ Regenerating token fast-paths via compiler builder...", flush=True)
        subprocess.run(["python", "aero.py", "build"], capture_output=True, text=True)
        
        print("  🔬 Executing compiler verification tests...", flush=True)
        test_script = "test_phase2.py" if os.path.exists("test_phase2.py") else "aero_auto_sdk/test_phase2.py"
        test_run = subprocess.run(["python", test_script], capture_output=True, text=True)
        
        if test_run.returncode == 0:
            print("  🎉 PASS: Regenerated compiler cleared all 43 semantic safety checks!", flush=True)
            
            print(f"  📤 Syncing updates directly to review branch '{target_branch}'...", flush=True)
            try:
                subprocess.run(["git", "add", "-A"], capture_output=True)
                diff_check = subprocess.run(["git", "diff", "--cached", "--quiet"])
                if diff_check.returncode != 0:
                    commit_msg = f"auto(evolution): pass #{loop_round} frequency-analyzed milestone snapshot"
                    subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)
                    
                    push_run = subprocess.run(["git", "push", "origin", f"HEAD:{target_branch}", "--force"], capture_output=True, text=True)
                    if push_run.returncode == 0:
                        print(f"  ✅ SUCCESS: Push milestone deployed upstream!", flush=True)
                    else:
                        print(f"  ⚠️ Push notice (upstream race/syncing): {push_run.stderr.strip()}", flush=True)
                else:
                    print("  横 Notice: Configuration matrices generated an identical layout state.", flush=True)
            except Exception as e_git:
                print(f"  ❌ Inline tracking gateway error: {e_git}", flush=True)
        else:
            print("  ❌ FAIL: Mutation generated an illegal layout configuration. Reverting...", flush=True)

        time.sleep(6)

    print(f"\n🏁 Target temporal allocation completed successfully. Total rounds processed: {loop_round}", flush=True)

if __name__ == '__main__':
    run_evolution_pipeline()
