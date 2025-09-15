#!/usr/bin/env python3
"""
Unit tests for quantum image processor fixes
Tests the safe_mean and small image handling functionality
"""
import pytest
import numpy as np
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from quantum_image_processor import safe_mean, MIN_IMAGE_SIDE_FOR_KERNEL, SMALL_IMAGE_FALLBACK


def test_safe_mean_empty_returns_default_nan():
    """Test safe_mean handles empty arrays correctly"""
    result = safe_mean(np.array([]))
    assert np.isnan(result), f"Expected NaN for empty array, got {result}"


def test_safe_mean_empty_returns_custom_default():
    """Test safe_mean returns custom default for empty arrays"""
    result = safe_mean(np.array([]), default=0.0)
    assert result == 0.0, f"Expected 0.0 for empty array with default, got {result}"


def test_safe_mean_normal_array():
    """Test safe_mean works correctly with normal arrays"""
    result = safe_mean(np.array([1, 2, 3]), default=0.0)
    assert result == 2.0, f"Expected 2.0 for [1,2,3], got {result}"


def test_safe_mean_with_nans():
    """Test safe_mean handles arrays with NaN values"""
    result = safe_mean(np.array([1, np.nan, 3]), default=0.0)
    assert result == 2.0, f"Expected 2.0 for [1,nan,3] with nanmean, got {result}"


def test_safe_mean_all_nans():
    """Test safe_mean handles arrays with all NaN values"""
    result = safe_mean(np.array([np.nan, np.nan]), default=-1.0)
    assert result == -1.0, f"Expected -1.0 for all-nan array, got {result}"


def test_safe_mean_none_input():
    """Test safe_mean handles None input"""
    result = safe_mean(None, default=42.0)
    assert result == 42.0, f"Expected 42.0 for None input, got {result}"


def test_configuration_loaded():
    """Test that environment configuration is loaded"""
    assert isinstance(MIN_IMAGE_SIDE_FOR_KERNEL, int)
    assert MIN_IMAGE_SIDE_FOR_KERNEL >= 1
    assert SMALL_IMAGE_FALLBACK in ['identity', 'upsample']
    print(f"✅ Config: MIN_IMAGE_SIDE_FOR_KERNEL={MIN_IMAGE_SIDE_FOR_KERNEL}, SMALL_IMAGE_FALLBACK={SMALL_IMAGE_FALLBACK}")


def test_quantum_image_processing_import():
    """Test that quantum image processor imports without errors"""
    try:
        from quantum_image_processor import (
            analyze_image_quantum, 
            _ui_pattern_signals, 
            _fft_features,
            safe_mean
        )
        print("✅ All quantum image processor functions imported successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import quantum_image_processor functions: {e}")


if __name__ == "__main__":
    # Run tests directly for manual verification
    print("🧪 Running quantum image processor tests...")
    
    test_safe_mean_empty_returns_default_nan()
    print("✅ test_safe_mean_empty_returns_default_nan")
    
    test_safe_mean_empty_returns_custom_default() 
    print("✅ test_safe_mean_empty_returns_custom_default")
    
    test_safe_mean_normal_array()
    print("✅ test_safe_mean_normal_array")
    
    test_safe_mean_with_nans()
    print("✅ test_safe_mean_with_nans")
    
    test_safe_mean_all_nans()
    print("✅ test_safe_mean_all_nans")
    
    test_safe_mean_none_input()
    print("✅ test_safe_mean_none_input")
    
    test_configuration_loaded()
    print("✅ test_configuration_loaded")
    
    test_quantum_image_processing_import()
    print("✅ test_quantum_image_processing_import")
    
    print("🎉 All tests passed!")
