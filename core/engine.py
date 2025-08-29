# core/engine.py
import asyncio
import json
import random
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from playwright.async_api import async_playwright, Page, BrowserContext
from .stealth import stealth_async
from .humanizer import Humanizer
from .wallet_handler import WalletHandler

class AutomationEngine:
    """Enhanced automation engine with stealth and humanization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pages: List[Page] = []
        self.contexts: List[BrowserContext] = []
        self.playwright = None
        self.humanizer = Humanizer()
        self.wallet_handler = WalletHandler()
        self.is_running = True
        
    async def start(self):
        """Start the automation engine"""
        self.logger.info("Starting enhanced Chrommin engine...")
        
        # Load configuration
        from config.manager import ConfigManager
        self.config = ConfigManager.load_config()
        
        # Initialize playwright
        self.playwright = await async_playwright().start()
        
        # Create bot profiles
        await self.create_bots()
        
        # Start WebSocket server
        await self.start_websocket_server()
        
        # Main loop
        while self.is_running:
            await asyncio.sleep(1)
            
    async def create_bots(self):
        """Create and configure bot instances"""
        self.logger.info(f"Creating {self.config.num_bots} bot instances...")
        
        for i in range(self.config.num_bots):
            try:
                context = await self.create_bot_context(i)
                page = await self.setup_bot_page(context, i)
                self.contexts.append(context)
                self.pages.append(page)
                self.logger.info(f"Bot {i+1} ready")
                
            except Exception as e:
                self.logger.error(f"Failed to create bot {i+1}: {e}")
                
    async def create_bot_context(self, bot_id: int) -> BrowserContext:
        """Create a browser context for a bot"""
        browser_args = await self.generate_browser_args(bot_id)
        
        context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=f"profiles/bot-{bot_id+1:02d}",
            headless=self.config.headless,
            viewport=self.config.viewport,
            args=browser_args,
            ignore_default_args=["--enable-automation"]
        )
        
        # Apply stealth enhancements
        await stealth_async(context)
        return context
        
    async def generate_browser_args(self, bot_id: int) -> List[str]:
        """Generate browser arguments with fingerprint variation"""
        args = [
            f"--window-size={self.config.viewport['width']},{self.config.viewport['height']}",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--user-agent={self.humanizer.generate_user_agent()}",
            f"--lang={self.humanizer.generate_language()}",
            f"--timezone={self.humanizer.generate_timezone()}"
        ]
        
        # Add extension args if enabled
        if self.config.enable_extensions:
            ext_paths = self.config.get_extension_paths()
            if ext_paths:
                args.append(f"--load-extension={','.join(ext_paths)}")
                
        return args
        
    async def setup_bot_page(self, context: BrowserContext, bot_id: int) -> Page:
        """Set up a page for a bot with enhanced action capture"""
        page = context.pages[0] if context.pages else await context.new_page()
        page._bot_id = bot_id + 1
        
        # Inject enhanced action capture script
        await page.add_init_script(self.get_action_capture_script(bot_id))
        
        # Connect to WebSocket
        await page.evaluate(f"""
            window.chromminBotId = {bot_id + 1};
            window.chromminWS = new WebSocket('ws://{self.config.ws_host}:{self.config.ws_port}');
        """)
        
        return page
        
    def get_action_capture_script(self, bot_id: int) -> str:
        """Return the enhanced action capture JavaScript"""
        return f"""
        // Enhanced Chrommin Action Capture
        (() => {{
            if (window.chromminCaptured) return;
            window.chromminCaptured = true;
            
            const captureAction = (type, data) => {{
                if (window.chromminWS && window.chromminWS.readyState === WebSocket.OPEN) {{
                    const payload = {{
                        t: type, 
                        ...data, 
                        ts: Date.now(), 
                        botId: window.chromminBotId,
                        intent: data.intent || type
                    }};
                    window.chromminWS.send(JSON.stringify(payload));
                }}
            }};
            
            // Enhanced selector generation with intent detection
            const generateSelectorsWithIntent = (el) => {{
                const selectors = [];
                const tagName = el.tagName.toLowerCase();
                const text = (el.textContent || '').trim().substring(0, 50);
                
                // Detect intent based on element properties
                let intent = null;
                
                // Button detection
                if (tagName === 'button' || el.getAttribute('role') === 'button') {{
                    intent = 'click';
                    if (text.includes('Connect') || text.includes('Wallet')) {{
                        intent = 'connect-wallet';
                    }} else if (text.includes('Sign') || text.includes('Confirm')) {{
                        intent = 'sign-transaction';
                    }} else if (text.includes('Submit') || text.includes('Apply')) {{
                        intent = 'submit-form';
                    }}
                }}
                
                // Input detection
                if (tagName === 'input' || tagName === 'textarea') {{
                    intent = 'input';
                    const type = el.getAttribute('type');
                    if (type === 'email') intent = 'input-email';
                    if (type === 'password') intent = 'input-password';
                }}
                
                // Generate selectors
                if (el.id) selectors.push(`#${{el.id}}`);
                if (el.className) {{
                    const classes = el.className.split(' ').filter(c => c);
                    if (classes.length) selectors.push(`${{tagName}}.${{classes.join('.')}}`);
                }}
                
                ['data-testid', 'data-test', 'data-id', 'name', 'aria-label', 'placeholder'].forEach(attr => {{
                    const value = el.getAttribute(attr);
                    if (value) selectors.push(`[${{attr}}="${{value}}"]`);
                }});
                
                if (text) selectors.push(`:has-text("${{text}}")`);
                
                return {{ selectors, intent }};
            }};
            
            // Event listeners with intent capture
            document.addEventListener('click', (e) => {{
                const {{ selectors, intent }} = generateSelectorsWithIntent(e.target);
                captureAction('click', {{
                    x: e.clientX,
                    y: e.clientY,
                    selectors: selectors,
                    tag: e.target.tagName.toLowerCase(),
                    text: (e.target.textContent || '').trim().substring(0, 100),
                    intent: intent
                }});
            }}, true);
            
            // Additional event listeners for input, change, etc.
            document.addEventListener('input', (e) => {{
                if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) {{
                    const {{ selectors, intent }} = generateSelectorsWithIntent(e.target);
                    captureAction('input', {{
                        value: e.target.value,
                        selectors: selectors,
                        tag: e.target.tagName.toLowerCase(),
                        type: e.target.getAttribute('type') || 'text',
                        intent: intent
                    }});
                }}
            }}, true);
            
            // Wallet and popup detection
            const originalOpen = window.open;
            window.open = function(...args) {{
                const popup = originalOpen.apply(this, args);
                captureAction('popup', {{ url: args[0], type: 'window-open' }});
                return popup;
            }};
        }})();
        """
        
    async def start_websocket_server(self):
        """Start WebSocket server for action mirroring"""
        import websockets
        from .action_processor import ActionProcessor
        
        self.action_processor = ActionProcessor(self.pages, self.humanizer, self.wallet_handler)
        
        async def handler(websocket):
            self.logger.info("Client connected to WebSocket")
            async for message in websocket:
                try:
                    action = json.loads(message)
                    await self.action_processor.process_action(action)
                except Exception as e:
                    self.logger.error(f"Error processing action: {e}")
                    
        self.server = await websockets.serve(
            handler, self.config.ws_host, self.config.ws_port
        )
        self.logger.info(f"WebSocket server started on ws://{self.config.ws_host}:{self.config.ws_port}")
        
    async def stop(self):
        """Stop the automation engine"""
        self.is_running = False
        if hasattr(self, 'server'):
            self.server.close()
            await self.server.wait_closed()
            
        for context in self.contexts:
            await context.close()
            
        if self.playwright:
            await self.playwright.stop()