# core/command_executor.py
"""Execute commands with human-like behavior"""

import asyncio
import random
import logging
from typing import Dict, List
from playwright.async_api import Page

from .humanizer import Humanizer

class CommandExecutor:
    """Execute commands with human-like behavior"""
    
    def __init__(self, humanizer: Humanizer):
        self.humanizer = humanizer
        self.logger = logging.getLogger(__name__)
        
    async def execute_command(self, page: Page, command: Dict):
        """Execute a command on a page"""
        cmd_type = command.get('type')
        
        try:
            if cmd_type == 'click':
                await self.execute_click(page, command)
            elif cmd_type == 'input':
                await self.execute_input(page, command)
            elif cmd_type == 'navigate':
                await self.execute_navigate(page, command)
            elif cmd_type == 'scroll':
                await self.execute_scroll(page, command)
            elif cmd_type == 'wait':
                await self.execute_wait(page, command)
            else:
                self.logger.warning(f"Unknown command type: {cmd_type}")
                
        except Exception as e:
            self.logger.error(f"Failed to execute command: {e}")
            
    async def execute_click(self, page: Page, command: Dict):
        """Execute a click command"""
        selector = command.get('selector')
        if not selector:
            return
            
        # Add random delay before action
        await asyncio.sleep(random.uniform(0.1, 1.0))
        
        # Use human-like click
        await self.humanizer.human_click(page, selector)
        
    async def execute_input(self, page: Page, command: Dict):
        """Execute an input command"""
        selector = command.get('selector')
        text = command.get('text', '')
        
        if not selector:
            return
            
        # Add random delay before action
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        # Use human-like typing
        await self.humanizer.human_type(page, selector, text)
        
    async def execute_navigate(self, page: Page, command: Dict):
        """Execute a navigation command"""
        url = command.get('url')
        if url:
            await page.goto(url, wait_until='domcontentloaded')
            
    async def execute_scroll(self, page: Page, command: Dict):
        """Execute a scroll command"""
        x = command.get('x', 0)
        y = command.get('y', 0)
        
        await page.evaluate(f"window.scrollTo({x}, {y})")
        
    async def execute_wait(self, page: Page, command: Dict):
        """Execute a wait command"""
        duration = command.get('duration', 1)
        await asyncio.sleep(duration)