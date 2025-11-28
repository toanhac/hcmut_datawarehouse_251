#!/usr/bin/env python3
"""
Dashboard Launcher Script
Run this to start the interactive churn analytics dashboard
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.visualization.dashboard import main

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  Bank Customer Churn Analytics Dashboard                ║
    ║  Data Warehouse & Decision Support System                ║
    ╚══════════════════════════════════════════════════════════╝
    
    Starting interactive dashboard...
    """)
    
    main()
