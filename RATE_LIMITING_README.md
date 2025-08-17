# Rate Limiting Implementation for Together AI API

## Overview

This document describes the modifications made to implement rate limiting for the Together AI API to respect the free tier limit of 60 requests per minute.

## Changes Made

### 1. Added RateLimiter Class

**File:** `pipeline/submodules/evaluate_jailbreak.py`

A new `RateLimiter` class was added with the following features:

- **Purpose:** Ensures API calls stay within the 60 requests per minute limit
- **Mechanism:** Tracks request timestamps and calculates wait times before making new requests
- **Safety:** Includes buffer time to prevent edge cases where requests might exceed the limit

### 2. Modified LlamaGuard2Classifier

**Changes:**
- Added rate limiter integration to the constructor
- Modified `classify_responses()` method to check rate limits before making API calls
- Added informative logging about rate limiting status

### 3. Updated llamaguard2_judge_fn Function

**Changes:**
- Reduced batch size from 20 to 10 requests per batch for better rate limit compliance
- Added comprehensive logging to track progress
- Integrated rate limiter for automatic delay management
- Removed manual delays (now handled automatically by the rate limiter)

## How It Works

### Rate Limiting Algorithm

1. **Request Tracking:** The rate limiter maintains a list of timestamps for recent API requests
2. **Cleanup:** Before each new batch, it removes timestamps older than 1 minute
3. **Capacity Check:** Calculates if the new requests would exceed the 60/minute limit
4. **Wait Calculation:** If necessary, calculates the minimum wait time to stay within limits
5. **Automatic Delay:** Sleeps for the calculated time before proceeding

### Processing Flow

```
Start Processing
    ↓
For each batch of 10 requests:
    ↓
Check rate limiter
    ↓
Wait if necessary (automatic)
    ↓
Make API calls
    ↓
Record request timestamps
    ↓
Continue to next batch
```

## Configuration

### Current Settings

- **Max requests per minute:** 60 (matches Together AI free tier)
- **Batch size:** 10 requests per batch
- **Safety buffer:** 1 second added to wait calculations

### Customization

You can adjust the rate limiting by modifying these parameters:

```python
# In llamaguard2_judge_fn function
classifier = LlamaGuard2Classifier(
    os.environ["TOGETHER_API_KEY"], 
    max_requests_per_minute=60  # Adjust this value if needed
)

batch_size = 10  # Adjust batch size if needed
```

## Example Usage

The rate limiter works automatically when you run jailbreak evaluations:

```python
# This will automatically respect rate limits
evaluation = evaluate_jailbreak(
    completions=your_completions,
    methodologies=["llamaguard2"],
    evaluation_path="results.json"
)
```

## Benefits

1. **Automatic Compliance:** No manual timing or delays needed
2. **Efficient Processing:** Uses batching to maximize throughput within limits
3. **Robust Handling:** Handles edge cases and provides clear feedback
4. **Transparent Operation:** Detailed logging shows when rate limiting occurs

## Performance Impact

- **Before:** Risk of hitting rate limits and getting errors
- **After:** Guaranteed compliance with 60 requests/minute limit
- **Processing Time:** May be slightly longer due to automatic delays, but ensures successful completion
- **Batch Processing:** Still efficient with 10-request batches

## Testing

A test script is provided (`test_rate_limiting.py`) to demonstrate the rate limiter functionality with a reduced limit for faster testing.

## Monitoring

The system provides detailed console output including:

- Progress updates for each batch
- Rate limiting status messages
- Wait time notifications when delays are necessary
- Completion confirmations

## Error Handling

The rate limiter includes safeguards for:

- Requests larger than the per-minute limit
- Edge cases around the 1-minute boundary
- Multiple consecutive batches
- System time changes

This implementation ensures your Together AI API usage stays within the free tier limits while maintaining efficient processing of your evaluation tasks.
