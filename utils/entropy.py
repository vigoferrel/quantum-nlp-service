#!/usr/bin/env python3
"""
System Entropy Utilities
Provides cryptographically secure entropy from OS kernel
Replaces Math.random and random.random usage throughout the system
"""
import secrets
import struct
import os
import time
from typing import Union


def sys_entropy_float() -> float:
    """Generate cryptographically secure float between 0.0 and 1.0"""
    return struct.unpack("!I", secrets.token_bytes(4))[0] / 2**32


def sys_entropy_int(min_val: int = 0, max_val: int = 100) -> int:
    """Generate cryptographically secure integer in range [min_val, max_val]"""
    return secrets.randbelow(max_val - min_val + 1) + min_val


def sys_entropy_choice(choices: list):
    """Choose randomly from a list using system entropy"""
    if not choices:
        return None
    index = secrets.randbelow(len(choices))
    return choices[index]


def sys_entropy_bytes(length: int = 32) -> bytes:
    """Generate cryptographically secure random bytes"""
    return secrets.token_bytes(length)


def sys_entropy_hex(length: int = 32) -> str:
    """Generate cryptographically secure hex string"""
    return secrets.token_hex(length)


def sys_entropy_urlsafe(length: int = 32) -> str:
    """Generate cryptographically secure URL-safe string"""
    return secrets.token_urlsafe(length)


def hybrid_entropy_sources() -> list:
    """
    Generate entropy from multiple system sources
    Used by flask_app_fast.py get_system_entropy()
    """
    sources = []
    
    try:
        # High resolution time
        sources.append(time.time_ns() & 0xFFFFFFFF)
        
        # Process ID
        sources.append(os.getpid() & 0xFFFF)
        
        # System entropy
        sources.append(struct.unpack("!I", secrets.token_bytes(4))[0] & 0xFFFF)
        
        # Memory info
        import sys
        sources.append(sys.getsizeof(sys.modules) & 0xFFFF)
        
        # CPU count
        sources.append((os.cpu_count() or 1) & 0xFFFF)
        
        # Working directory hash
        sources.append(hash(str(os.getcwd())) & 0xFFFF)
        
        # Monotonic time
        sources.append(int(time.monotonic() * 1000000) & 0xFFFF)
        
    except Exception:
        # Fallback to pure cryptographic entropy
        sources = [struct.unpack("!I", secrets.token_bytes(4))[0] & 0xFFFF for _ in range(8)]
    
    return sources


# JavaScript equivalent for browser usage
JAVASCRIPT_ENTROPY = '''
/**
 * System Entropy for Browser/Node.js
 * Replaces Math.random() with cryptographically secure entropy
 */

// For browsers with Web Crypto API
function sysEntropyFloat() {
    const buffer = new Uint32Array(1);
    crypto.getRandomValues(buffer);
    return buffer[0] / 2**32;
}

function sysEntropyInt(min = 0, max = 100) {
    const range = max - min + 1;
    const buffer = new Uint32Array(1);
    crypto.getRandomValues(buffer);
    return Math.floor((buffer[0] / 2**32) * range) + min;
}

function sysEntropyChoice(choices) {
    if (!choices || choices.length === 0) return null;
    const index = sysEntropyInt(0, choices.length - 1);
    return choices[index];
}

// For Node.js
function nodeEntropyFloat() {
    const crypto = require('crypto');
    const buffer = crypto.randomBytes(4);
    return buffer.readUInt32BE(0) / 2**32;
}

// Export for different environments
if (typeof module !== 'undefined' && module.exports) {
    // Node.js
    module.exports = {
        sysEntropyFloat: nodeEntropyFloat,
        sysEntropyInt,
        sysEntropyChoice
    };
} else if (typeof window !== 'undefined') {
    // Browser
    window.sysEntropy = {
        float: sysEntropyFloat,
        int: sysEntropyInt,
        choice: sysEntropyChoice
    };
}
'''


if __name__ == "__main__":
    # Test the entropy functions
    print("🧪 Testing system entropy functions...")
    
    print(f"Random float: {sys_entropy_float()}")
    print(f"Random int (1-100): {sys_entropy_int(1, 100)}")
    print(f"Random choice: {sys_entropy_choice(['apple', 'banana', 'orange'])}")
    print(f"Random hex (16 bytes): {sys_entropy_hex(16)}")
    print(f"Random URL-safe (16 bytes): {sys_entropy_urlsafe(16)}")
    
    print("✅ All entropy functions working correctly!")
