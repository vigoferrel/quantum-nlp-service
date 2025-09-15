"""
VIGOLEONROCKS Environment Configuration Validator

This module provides strict validation and configuration management for the VIGOLEONROCKS project,
enforcing the critical project policies:
1. No insecure randomness - metrics-based randomness only
2. Background processes with metrics exposure
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from urllib.parse import urlparse
import secrets
import warnings

# Configure logger for this module
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of environment validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    critical_violations: List[str]


class EnvironmentValidator:
    """Validates and manages environment configuration for VIGOLEONROCKS"""

    # CRITICAL: These variables MUST be set and comply with project policies
    CRITICAL_VARS = {
        'QUANTUM_PROCESSOR_ENABLED': 'true',
        'METRICS_RNG_ENABLED': 'true',
        'BACKGROUND_EXECUTION': 'true',
        'PROMETHEUS_ENABLED': 'true',
    }

    # Required environment variables
    REQUIRED_VARS = [
        'SECRET_KEY',
        'DATABASE_URL', 
        'REDIS_URL',
        'FLASK_ENV',
        'QUANTUM_PROCESSOR_ENABLED',
        'METRICS_RNG_ENABLED',
        'BACKGROUND_EXECUTION',
        'PROMETHEUS_ENABLED',
    ]

    # Default values for optional variables
    DEFAULTS = {
        'FLASK_ENV': 'production',
        'HOST': '0.0.0.0',
        'PORT': '5000',
        'WORKERS': '4',
        'LOG_LEVEL': 'INFO',
        'API_VERSION': 'v1',
        'DEFAULT_LANGUAGE': 'es',
        'SUPPORTED_LANGUAGES': 'es,en,pt,fr,de',
        'METRICS_ENDPOINT': '/api/status',
        'QUANTUM_METRICS_ENDPOINT': '/api/quantum-metrics',
        'HEALTH_CHECK_ENABLED': 'true',
        'HEALTH_CHECK_INTERVAL': '30',
        'QUANTUM_STATES_COUNT': '1000',
        'QUANTUM_ENTANGLEMENT_THRESHOLD': '0.85',
        'METRICS_RNG_SEED_SOURCE': 'kernel',
        'METRICS_RNG_ENTROPY_POOL_SIZE': '4096',
        'PROMETHEUS_PORT': '8000',
    }

    # Forbidden values that indicate default/insecure configuration
    FORBIDDEN_VALUES = {
        'SECRET_KEY': [
            'your-super-secret-key-here-change-this',
            'secret',
            'password',
            'changeme',
        ],
        'JWT_SECRET_KEY': [
            'your-jwt-secret-key-change-this',
            'secret',
            'jwt-secret',
        ],
        'ENCRYPTION_KEY': [
            'your-encryption-key-change-this',
            'encryption-key',
        ],
    }

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.validation_result: Optional[ValidationResult] = None

    def validate_environment(self) -> ValidationResult:
        """
        Comprehensive validation of environment configuration
        
        Returns:
            ValidationResult: Detailed validation results including critical violations
        """
        errors = []
        warnings = []
        critical_violations = []

        # 1. Check critical policy compliance (HIGHEST PRIORITY)
        critical_violations.extend(self._validate_critical_policies())

        # 2. Check required variables
        errors.extend(self._validate_required_vars())

        # 3. Validate URL formats
        errors.extend(self._validate_urls())

        # 4. Check for insecure default values
        warnings.extend(self._validate_security())

        # 5. Validate randomness configuration
        critical_violations.extend(self._validate_randomness_config())

        # 6. Validate background process configuration
        critical_violations.extend(self._validate_background_config())

        # 7. Validate metrics configuration
        critical_violations.extend(self._validate_metrics_config())

        # 8. Validate multilingual configuration
        warnings.extend(self._validate_multilingual_config())

        # If there are critical violations, the application CANNOT start
        is_valid = len(critical_violations) == 0 and len(errors) == 0

        self.validation_result = ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            critical_violations=critical_violations
        )

        return self.validation_result

    def _validate_critical_policies(self) -> List[str]:
        """Validate adherence to critical project policies"""
        violations = []

        for var, required_value in self.CRITICAL_VARS.items():
            actual_value = os.getenv(var, '').lower()
            if actual_value != required_value:
                violations.append(
                    f"CRITICAL POLICY VIOLATION: {var} must be '{required_value}' "
                    f"but found '{actual_value}'. This violates core project policies."
                )

        return violations

    def _validate_required_vars(self) -> List[str]:
        """Check all required environment variables are present"""
        errors = []

        for var in self.REQUIRED_VARS:
            if not os.getenv(var):
                errors.append(f"Required environment variable missing: {var}")

        return errors

    def _validate_urls(self) -> List[str]:
        """Validate URL format for database and service connections"""
        errors = []
        
        url_vars = ['DATABASE_URL', 'REDIS_URL', 'CELERY_BROKER_URL', 'CELERY_RESULT_BACKEND']
        
        for var in url_vars:
            url = os.getenv(var)
            if url and not self._is_valid_url(url):
                errors.append(f"Invalid URL format for {var}: {url}")

        return errors

    def _validate_security(self) -> List[str]:
        """Check for insecure default values"""
        warnings = []

        for var, forbidden in self.FORBIDDEN_VALUES.items():
            value = os.getenv(var, '')
            if value in forbidden:
                warnings.append(
                    f"SECURITY WARNING: {var} uses default/insecure value. "
                    f"Change to a secure random value in production."
                )

        return warnings

    def _validate_randomness_config(self) -> List[str]:
        """Validate randomness generation configuration (CRITICAL)"""
        violations = []

        # Check metrics-based RNG is enabled
        if not self._is_true(os.getenv('METRICS_RNG_ENABLED', 'false')):
            violations.append(
                "CRITICAL: METRICS_RNG_ENABLED must be 'true'. "
                "Project policy prohibits insecure randomness - use metrics-based randomness."
            )

        # Validate RNG seed source
        seed_source = os.getenv('METRICS_RNG_SEED_SOURCE', '').lower()
        valid_sources = ['kernel', 'cpu', 'memory', 'network', 'disk']
        if seed_source and seed_source not in valid_sources:
            violations.append(
                f"CRITICAL: METRICS_RNG_SEED_SOURCE must be one of {valid_sources}, "
                f"found '{seed_source}'"
            )

        return violations

    def _validate_background_config(self) -> List[str]:
        """Validate background process configuration (CRITICAL)"""
        violations = []

        if not self._is_true(os.getenv('BACKGROUND_EXECUTION', 'false')):
            violations.append(
                "CRITICAL: BACKGROUND_EXECUTION must be 'true'. "
                "Project policy requires all processes run in background."
            )

        return violations

    def _validate_metrics_config(self) -> List[str]:
        """Validate metrics exposure configuration (CRITICAL)"""
        violations = []

        if not self._is_true(os.getenv('PROMETHEUS_ENABLED', 'false')):
            violations.append(
                "CRITICAL: PROMETHEUS_ENABLED must be 'true'. "
                "Project policy requires metrics exposure for debugging and maintenance."
            )

        # Validate required metrics endpoints
        metrics_endpoint = os.getenv('METRICS_ENDPOINT', '')
        quantum_metrics_endpoint = os.getenv('QUANTUM_METRICS_ENDPOINT', '')

        if not metrics_endpoint:
            violations.append(
                "CRITICAL: METRICS_ENDPOINT must be set (e.g., '/api/status')"
            )

        if not quantum_metrics_endpoint:
            violations.append(
                "CRITICAL: QUANTUM_METRICS_ENDPOINT must be set (e.g., '/api/quantum-metrics')"
            )

        return violations

    def _validate_multilingual_config(self) -> List[str]:
        """Validate multilingual configuration"""
        warnings = []

        default_lang = os.getenv('DEFAULT_LANGUAGE', 'es')
        supported_langs = os.getenv('SUPPORTED_LANGUAGES', '').split(',')

        if default_lang not in supported_langs:
            warnings.append(
                f"DEFAULT_LANGUAGE '{default_lang}' not in SUPPORTED_LANGUAGES: {supported_langs}"
            )

        expected_langs = {'es', 'en', 'pt', 'fr', 'de'}
        actual_langs = set(lang.strip() for lang in supported_langs if lang.strip())

        missing_langs = expected_langs - actual_langs
        if missing_langs:
            warnings.append(
                f"Missing supported languages: {missing_langs}. "
                f"Consider adding for full multilingual support."
            )

        return warnings

    def load_configuration(self) -> Dict[str, Any]:
        """
        Load and process environment configuration with defaults
        
        Returns:
            Dict[str, Any]: Processed configuration dictionary
        """
        # Apply defaults first
        config = self.DEFAULTS.copy()

        # Override with environment variables
        for key in list(config.keys()) + list(os.environ.keys()):
            env_value = os.getenv(key)
            if env_value is not None:
                config[key] = self._parse_env_value(env_value)

        # Process special configurations
        config = self._process_special_configs(config)

        self.config = config
        return config

    def _process_special_configs(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process special configuration transformations"""
        
        # Convert string booleans
        bool_vars = [
            'FLASK_DEBUG', 'TESTING', 'QUANTUM_PROCESSOR_ENABLED', 
            'METRICS_RNG_ENABLED', 'BACKGROUND_EXECUTION', 'PROMETHEUS_ENABLED',
            'HEALTH_CHECK_ENABLED', 'DEBUG_TB_ENABLED', 'PROFILING_ENABLED'
        ]
        
        for var in bool_vars:
            if var in config:
                config[var] = self._is_true(str(config[var]))

        # Convert string numbers
        int_vars = [
            'PORT', 'WORKERS', 'PROMETHEUS_PORT', 'QUANTUM_STATES_COUNT',
            'HEALTH_CHECK_INTERVAL', 'HEALTH_CHECK_TIMEOUT', 'METRICS_RNG_ENTROPY_POOL_SIZE',
            'METRICS_RNG_RESEED_INTERVAL'
        ]
        
        for var in int_vars:
            if var in config:
                try:
                    config[var] = int(config[var])
                except (ValueError, TypeError):
                    logger.warning(f"Invalid integer value for {var}: {config[var]}")

        # Convert string floats
        float_vars = ['QUANTUM_ENTANGLEMENT_THRESHOLD', 'SENTRY_TRACES_SAMPLE_RATE']
        
        for var in float_vars:
            if var in config:
                try:
                    config[var] = float(config[var])
                except (ValueError, TypeError):
                    logger.warning(f"Invalid float value for {var}: {config[var]}")

        # Process lists
        if 'SUPPORTED_LANGUAGES' in config:
            config['SUPPORTED_LANGUAGES'] = [
                lang.strip() for lang in str(config['SUPPORTED_LANGUAGES']).split(',')
                if lang.strip()
            ]

        return config

    def generate_secure_secrets(self) -> Dict[str, str]:
        """Generate secure random secrets for required variables"""
        return {
            'SECRET_KEY': secrets.token_urlsafe(32),
            'JWT_SECRET_KEY': secrets.token_urlsafe(32),
            'ENCRYPTION_KEY': secrets.token_urlsafe(32),
        }

    def report_validation_results(self) -> None:
        """Print detailed validation report"""
        if not self.validation_result:
            print("❌ No validation performed. Call validate_environment() first.")
            return

        result = self.validation_result

        print("\n" + "="*80)
        print("🔍 VIGOLEONROCKS ENVIRONMENT VALIDATION REPORT")
        print("="*80)

        # Critical violations (HIGHEST PRIORITY)
        if result.critical_violations:
            print("\n🚨 CRITICAL POLICY VIOLATIONS:")
            print("These MUST be fixed before the application can start!")
            for violation in result.critical_violations:
                print(f"  ❌ {violation}")

        # Errors
        if result.errors:
            print(f"\n❌ ERRORS ({len(result.errors)}):")
            for error in result.errors:
                print(f"  ❌ {error}")

        # Warnings
        if result.warnings:
            print(f"\n⚠️  WARNINGS ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"  ⚠️  {warning}")

        # Summary
        print(f"\n📊 VALIDATION SUMMARY:")
        print(f"  ✅ Valid: {'YES' if result.is_valid else 'NO'}")
        print(f"  🚨 Critical Violations: {len(result.critical_violations)}")
        print(f"  ❌ Errors: {len(result.errors)}")
        print(f"  ⚠️  Warnings: {len(result.warnings)}")

        if result.is_valid:
            print("\n🎉 Environment validation PASSED! Ready to start VIGOLEONROCKS.")
        else:
            print("\n🛑 Environment validation FAILED! Fix issues before starting.")
            print("\nREMEMBER CRITICAL POLICIES:")
            print("  1. 🚫 NO insecure randomness - use kernel/service metrics")
            print("  2. 🔄 ALL processes in background with metrics")

        print("="*80)

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Check if URL has valid format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def _is_true(value: str) -> bool:
        """Convert string to boolean"""
        return str(value).lower() in ('true', '1', 'yes', 'on')

    @staticmethod
    def _parse_env_value(value: str) -> Union[str, int, float, bool]:
        """Parse environment variable value to appropriate type"""
        value = value.strip()
        
        # Try boolean
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        # Try integer
        try:
            if '.' not in value:
                return int(value)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value


def validate_environment_or_exit() -> Dict[str, Any]:
    """
    Validate environment and exit if critical violations found
    
    Returns:
        Dict[str, Any]: Validated configuration
    """
    validator = EnvironmentValidator()
    
    # Load configuration
    config = validator.load_configuration()
    
    # Validate environment
    result = validator.validate_environment()
    
    # Print report
    validator.report_validation_results()
    
    # Exit if validation failed
    if not result.is_valid:
        print("\n💥 CRITICAL: Environment validation failed!")
        print("Application cannot start with policy violations.")
        sys.exit(1)
    
    if result.warnings:
        print(f"\n⚠️  Found {len(result.warnings)} warnings. Consider addressing them.")
    
    return config


if __name__ == "__main__":
    # CLI tool for environment validation
    print("🔍 VIGOLEONROCKS Environment Validator")
    print("Checking environment configuration and policy compliance...")
    
    try:
        config = validate_environment_or_exit()
        print(f"\n✅ Configuration loaded with {len(config)} variables.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Validation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Validation failed with error: {e}")
        sys.exit(1)
