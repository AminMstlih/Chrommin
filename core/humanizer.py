# core/humanizer.py
"""Human-like input behavior simulation"""

import random
import asyncio
from typing import Dict, List, Tuple
from playwright.async_api import Page

class Humanizer:
    """Simulate human-like behavior for inputs"""
    
    def __init__(self):
        self.mouse_movements = []
        self.typing_profiles = self.generate_typing_profiles()
        
    def generate_user_agent(self) -> str:
        """Generate a random user agent"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        return random.choice(user_agents)
        
    def generate_language(self) -> str:
        """Generate random language preference"""
        languages = ["en-US,en", "en-GB,en", "en-CA,en", "en-AU,en"]
        return random.choice(languages)
        
    def generate_timezone(self) -> str:
        """Generate random timezone"""
        timezones = ["America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney"]
        return random.choice(timezones)
        
    def generate_typing_profiles(self) -> List[Dict]:
        """Generate different typing speed profiles"""
        return [
            {"wpm": 40, "accuracy": 0.95, "mistake_chance": 0.1},
            {"wpm": 60, "accuracy": 0.98, "mistake_chance": 0.05},
            {"wpm": 80, "accuracy": 0.99, "mistake_chance": 0.02},
            {"wpm": 100, "accuracy": 0.995, "mistake_chance": 0.01}
        ]
        
    async def human_click(self, page: Page, selector: str):
        """Simulate human-like click with mouse movement"""
        # Get element position
        rect = await page.evaluate(f"""(() => {{
            const el = document.querySelector('{selector}');
            if (!el) return null;
            const rect = el.getBoundingClientRect();
            return {{
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2,
                width: rect.width,
                height: rect.height
            }};
        }})()""")
        
        if not rect:
            return await page.click(selector)
            
        # Generate human-like mouse path
        target_x = rect['x']
        target_y = rect['y']
        
        # Move mouse in curved path
        await page.mouse.move(
            random.randint(0, 100),
            random.randint(0, 100)
        )
        
        # Move to target with intermediate points
        steps = random.randint(3, 8)
        for i in range(steps):
            progress = (i + 1) / steps
            curve_x = target_x * progress + random.randint(-20, 20)
            curve_y = target_y * progress + random.randint(-20, 20)
            await page.mouse.move(curve_x, curve_y)
            
        # Add slight hesitation before click
        await asyncio.sleep(random.uniform(0.1, 0.3))
        
        # Click with slight offset to mimic human imprecision
        click_x = target_x + random.randint(-5, 5)
        click_y = target_y + random.randint(-5, 5)
        await page.mouse.click(click_x, click_y)
        
    async def human_type(self, page: Page, selector: str, text: str):
        """Simulate human-like typing"""
        profile = random.choice(self.typing_profiles)
        chars_per_ms = profile['wpm'] * 5 / 60000  # chars per millisecond
        
        # Focus on the element
        await page.focus(selector)
        
        # Type with variable speed and occasional mistakes
        for char in text:
            # Variable delay between keystrokes
            delay_ms = random.randint(50, 200) / chars_per_ms
            await asyncio.sleep(delay_ms / 1000)
            
            # Occasional typos
            if random.random() < profile['mistake_chance']:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                await page.keyboard.press(wrong_char)
                await asyncio.sleep(random.randint(100, 300) / 1000)
                await page.keyboard.press('Backspace')
                await asyncio.sleep(random.randint(100, 300) / 1000)
                
            await page.keyboard.press(char)