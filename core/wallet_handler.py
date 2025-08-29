# core/wallet_handler.py
"""Handle wallet interactions and popups"""

import asyncio
import logging
from typing import Dict, List
from playwright.async_api import Page

class WalletHandler:
    """Handle wallet interactions and transactions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.wallet_configs = {
            'metamask': {
                'selectors': {
                    'password_input': '#password',
                    'unlock_button': 'button[data-testid="unlock-submit"]',
                    'next_button': 'button[data-testid="page-container-footer-next"]',
                    'connect_button': 'button[data-testid="page-container-footer-next"]',
                    'confirm_button': 'button[data-testid="page-container-footer-next"]',
                    'sign_button': 'button[data-testid="page-container-footer-next"]'
                },
                'flow': ['password_input', 'unlock_button', 'next_button', 'connect_button', 'confirm_button', 'sign_button']
            },
            'phantom': {
                'selectors': {
                    'password_input': '#password',
                    'unlock_button': 'button[type="submit"]',
                    'approve_button': 'button:has-text("Approve")',
                    'confirm_button': 'button:has-text("Confirm")',
                    'connect_button': 'button:has-text("Connect")'
                },
                'flow': ['password_input', 'unlock_button', 'connect_button', 'approve_button', 'confirm_button']
            }
        }
        
    async def handle_wallet_popup(self, page: Page, wallet_type: str = 'metamask'):
        """Handle wallet popup interactions"""
        self.logger.info(f"Handling {wallet_type} popup")
        
        # Wait for popup to appear
        try:
            popup = await page.wait_for_event('popup', timeout=10000)
            await popup.bring_to_front()
            
            # Execute wallet-specific flow
            config = self.wallet_configs.get(wallet_type)
            if config:
                for step in config['flow']:
                    selector = config['selectors'][step]
                    try:
                        await popup.wait_for_selector(selector, timeout=5000)
                        await popup.click(selector)
                        await asyncio.sleep(1)  # Brief pause between actions
                    except Exception as e:
                        self.logger.warning(f"Failed step {step}: {e}")
                        continue
                        
            await popup.close()
            await page.bring_to_front()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to handle wallet popup: {e}")
            return False
            
    async def detect_and_handle_wallet(self, page: Page, action: Dict):
        """Detect wallet-related actions and handle them"""
        intent = action.get('intent', '')
        
        if intent in ['connect-wallet', 'sign-transaction']:
            # Determine wallet type based on page content or configuration
            wallet_type = 'metamask'  # Default, could be detected
            
            # Perform the original action first
            if intent == 'connect-wallet':
                await page.click(action['selectors'][0])
            elif intent == 'sign-transaction':
                await page.click(action['selectors'][0])
                
            # Then handle the popup
            return await self.handle_wallet_popup(page, wallet_type)
            
        return False
    
    async def detect_wallet_type(self, page: Page) -> str:
        """Detect the wallet type based on page content"""
        # Check for MetaMask
        try:
            await page.wait_for_selector('meta[name="wallet"][content*="metamask"]', timeout=1000)
            return 'metamask'
        except:
            pass
            
        # Check for Phantom
        try:
            await page.wait_for_selector('meta[name="wallet"][content*="phantom"]', timeout=1000)
            return 'phantom'
        except:
            pass
            
        # Default to MetaMask
        return 'metamask'
        
    async def setup_wallet_profiles(self):
        """Set up wallet profiles with credentials"""
        # This would load wallet credentials from a secure storage
        # For now, we'll use placeholder data
        self.wallet_profiles = {
            i: {
                'metamask': {'password': f'password{i}'},
                'phantom': {'password': f'password{i}'}
            } for i in range(1, 101)  # Assuming up to 100 bots
        }