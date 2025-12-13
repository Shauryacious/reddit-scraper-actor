"""
Main entry point for Apify CLI compatibility.
This file uses Actor context manager directly so CLI can detect this as a Python actor.
"""

# Import apify at top level so CLI can detect this as a Python actor
from apify import Actor
import asyncio
from src.main import run_scraper

async def main():
    """Main entry point with Actor context manager"""
    async with Actor:
        # Get input configuration
        input_data = await Actor.get_input()
        # Run the scraper logic
        await run_scraper(input_data)

if __name__ == "__main__":
    asyncio.run(main())

