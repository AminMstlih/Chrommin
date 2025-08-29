# core/action_processor.py
"""Process and execute actions across all bots"""

import asyncio
import logging
from typing import List, Dict, Any
from playwright.async_api import Page

from .humanizer import Humanizer
from .wallet_handler import WalletHandler

class ActionProcessor:
    """Process actions and execute them across all bots"""
    
    def __init__(self, pages: List[Page], humanizer: Humanizer, wallet_handler: WalletHandler):
        self.pages = pages
        self.humanizer = humanizer
        self.wallet_handler = wallet_handler
        self.logger = logging.getLogger(__name__)
        
    async def process_action(self, action: Dict[str, Any]):
        """Process a single action across all bots"""
        action_type = action.get('t')
        bot_id = action.get('botId')
        
        self.logger.info(f"Processing {action_type} action from bot {bot_id}")
        
        # Add random delays to simulate human timing
        delays = [random.uniform(0.1, 2.0) for _ in self.pages]
        tasks = []
        
        for i, page in enumerate(self.pages):
            if i + 1 == bot_id:
                continue  # Skip the source bot
                
            task = self.execute_action(page, action, delays[i])
            tasks.append(task)
            
        await asyncio.gather(*tasks, return_exceptions=True)
        
    async def execute_action(self, page: Page, action: Dict, delay: float):
        """Execute an action on a specific page"""
        await asyncio.sleep(delay)
        
        action_type = action.get('t')
        selectors = action.get('selectors', [])
        
        try:
            if action_type == 'click':
                # Try wallet handling first for specific intents
                if not await self.wallet_handler.detect_and_handle_wallet(page, action):
                    # Fall back to regular click
                    for selector in selectors:
                        try:
                            await self.humanizer.human_click(page, selector)
                            break
                        except Exception:
                            continue
                            
            elif action_type == 'input':
                value = action.get('value', '')
                for selector in selectors:
                    try:
                        await self.humanizer.human_type(page, selector, value)
                        break
                    except Exception:
                        continue
                        
            elif action_type == 'nav':
                url = action.get('href')
                if url:
                    await page.goto(url, wait_until='domcontentloaded')
                    
            elif action_type == 'scroll':
                xn = action.get('xn', 0)
                yn = action.get('yn', 0)
                await page.evaluate(f"window.scrollTo({xn} * document.body.scrollWidth, {yn} * document.body.scrollHeight)")
                
        except Exception as e:
            self.logger.error(f"Failed to execute action on bot {getattr(page, '_bot_id', 'unknown')}: {e}")