# main.py
#!/usr/bin/env python3
"""
🚀 Chrommin - Advanced Multi-Account Airdrop Automation Engine
================================================================

Enhanced version with:
- Advanced stealth capabilities
- Human-like input behavior
- Wallet automation
- GUI configuration
- One-click installation
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('chrommin.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

async def main():
    """Main application entry point"""
    logger = setup_logging()
    logger.info("Starting Chrommin...")
    
    try:
        # Check if we should show GUI or run in console mode
        if len(sys.argv) > 1 and sys.argv[1] == '--gui':
            from gui.app import ChromminApp
            app = ChromminApp()
            app.run()
        else:
            from core.engine import AutomationEngine
            engine = AutomationEngine()
            await engine.start()
            
    except Exception as e:
        logger.error(f"Failed to start Chrommin: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    # Check for installation requirements
    if not os.path.exists('venv') and 'install' not in sys.argv:
        print("Please run install.py first to set up Chrommin!")
        sys.exit(1)
        
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        from utils.installer import install_chrommin
        install_chrommin()
    else:
        asyncio.run(main())