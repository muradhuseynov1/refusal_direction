#!/usr/bin/env python3
"""
Test script to demonstrate the rate limiting functionality.
This script simulates API calls to show how the rate limiter works.
"""

import sys
import os
import time
from datetime import datetime

# Add the pipeline directory to the path so we can import the rate limiter
sys.path.append(os.path.join(os.path.dirname(__file__), 'pipeline'))

# Import the RateLimiter class from the evaluate_jailbreak module
try:
    from pipeline.submodules.evaluate_jailbreak import RateLimiter
except ImportError:
    print("Could not import RateLimiter. Please run this script from the project root directory.")
    sys.exit(1)

def simulate_api_call(call_id, delay=0.1):
    """Simulate an API call with a small delay."""
    print(f"  Making API call {call_id}... ", end="", flush=True)
    time.sleep(delay)  # Simulate API processing time
    print("✓")

def test_rate_limiter():
    """Test the rate limiter with various scenarios."""
    print("Testing Rate Limiter for Together AI API (60 requests/minute)")
    print("=" * 60)
    
    # Create a rate limiter with a lower limit for testing (6 requests per minute = 1 per 10 seconds)
    # This makes the test faster while demonstrating the same behavior
    test_rate_limiter = RateLimiter(max_requests_per_minute=6)
    
    print("\nTest 1: Making 3 requests (should work immediately)")
    print("-" * 50)
    start_time = datetime.now()
    
    test_rate_limiter.wait_if_needed(3)
    for i in range(3):
        simulate_api_call(i + 1)
    
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"Completed in {elapsed:.1f} seconds\n")
    
    print("Test 2: Making 4 more requests (should trigger rate limiting)")
    print("-" * 50)
    start_time = datetime.now()
    
    test_rate_limiter.wait_if_needed(4)
    for i in range(4):
        simulate_api_call(i + 4)
    
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"Completed in {elapsed:.1f} seconds\n")
    
    print("Test 3: Making requests individually")
    print("-" * 50)
    start_time = datetime.now()
    
    for i in range(3):
        print(f"Request {i + 8}:")
        test_rate_limiter.wait_if_needed(1)
        simulate_api_call(i + 8)
    
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"Completed in {elapsed:.1f} seconds\n")
    
    print("Rate limiting test completed!")
    print("\nFor production usage with Together AI:")
    print("- The actual rate limiter uses 60 requests per minute")
    print("- Batch size is set to 10 requests per batch")
    print("- This ensures you stay within the API limits")

if __name__ == "__main__":
    test_rate_limiter()
