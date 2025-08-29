# core/stealth.py
"""Advanced stealth techniques for browser automation"""

import asyncio
from playwright.async_api import BrowserContext

async def stealth_async(context: BrowserContext):
    """Apply stealth techniques to a browser context"""
    await context.add_init_script("""
    // Advanced stealth techniques
    () => {
        // Override webdriver flag
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Override permissions
        const originalQuery = navigator.permissions.query;
        navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // Spoof platform and vendor
        Object.defineProperty(navigator, 'platform', {
            get: () => 'Win32',
        });
        
        Object.defineProperty(navigator, 'vendor', {
            get: () => 'Google Inc.',
        });
        
        // Spoof plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Spoof languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
        
        // Canvas fingerprint spoofing
        const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
        CanvasRenderingContext2D.prototype.getImageData = function(...args) {
            const data = originalGetImageData.apply(this, args);
            if (data && data.data && data.data.length > 1000) {
                for (let i = 0; i < 10; i++) {
                    data.data[i] += Math.random() * 10 - 5;
                }
            }
            return data;
        };
    }
    """)
    
    # Additional stealth options
    await context.add_init_script("""
    // Mock Chrome runtime
    window.chrome = {
        runtime: {
            // Mock chrome runtime API
        }
    };
    """)