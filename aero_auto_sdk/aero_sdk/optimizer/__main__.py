"""Run a full self-optimization cycle: ``python -m aero_sdk.optimizer``."""

import sys

from aero_sdk.optimizer.pipeline import main

if __name__ == "__main__":
    sys.exit(main())
