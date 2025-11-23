# llm/genai_guard.py
import time
from typing import Optional

# Updated import: we now use call_llm
from llm.model import call_llm


def safe_generate(
    prompt: str,
    retries: int = 5,
    base_delay: float = 2.0,
    fallback: Optional[str] = None
) -> str:
    """
    Fail-safe wrapper for LLM calls.
    - Retries on 429/RESOURCE_EXHAUSTED errors with exponential-ish backoff.
    - Returns fallback string when retries are exhausted.
    """

    for attempt in range(retries):
        try:
            return call_llm(prompt)  # ← NEW updated function
        except Exception as e:
            err = str(e).lower()

            # retry on quota errors
            if "resource_exhausted" in err or "429" in err or "quota" in err:
                wait = base_delay * (attempt + 1)
                print(f"⚠️ LLM rate-limit detected. Retry #{attempt+1} in {wait}s...")
                time.sleep(wait)
                continue

            # non-retryable error → break and fallback
            print("❌ LLM error:", e)
            break

    # fallback if retries fail
    return fallback if fallback is not None else ""
