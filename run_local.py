#!/usr/bin/env python3
"""
Local test runner for the Reddit Scraper Actor.
This script mimics what Apify CLI does for local testing.

Usage:
    python3 run_local.py [input_file.json]
    
If no input file is provided, it will look for test-input.json
"""

import json
import sys
import os
from pathlib import Path

# Set up local storage directory BEFORE any Apify imports
storage_dir = Path(__file__).parent / 'storage'
os.environ['APIFY_LOCAL_STORAGE_DIR'] = str(storage_dir)

# Create storage directory structure
kv_store_dir = storage_dir / 'key_value_stores' / 'default'
kv_store_dir.mkdir(parents=True, exist_ok=True)


def main():
    # Determine input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'test-input.json'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print(f"Usage: python3 {sys.argv[0]} [input_file.json]")
        sys.exit(1)
    
    # Read input file
    try:
        with open(input_file, 'r') as f:
            input_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    # Write input to the location where Actor.get_input() reads it from
    # The Apify SDK reads from storage/key_value_stores/default/INPUT.json
    input_path = kv_store_dir / 'INPUT.json'
    with open(input_path, 'w') as f:
        json.dump(input_data, f, indent=2)
    
    print(f"Running actor with input from: {input_file}")
    print(f"Input: {json.dumps(input_data, indent=2)}")
    print("-" * 50)
    
    # Now import and run the actor
    import asyncio
    from main import main as actor_main
    
    # Run the actor
    try:
        asyncio.run(actor_main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error running actor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
