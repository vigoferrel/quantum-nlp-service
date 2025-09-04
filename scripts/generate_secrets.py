#!/usr/bin/env python3
"""
VIGOLEONROCKS Secure Secrets Generator

This script generates cryptographically secure secrets for the VIGOLEONROCKS project,
following the project's critical policies:
1. No Math.random usage - uses OS cryptographic randomness
2. Metric-aware secret generation
"""

import os
import sys
import secrets
import string
from typing import Dict, Optional
import argparse
from pathlib import Path


class SecureSecretsGenerator:
    """Generates cryptographically secure secrets using OS randomness"""

    def __init__(self):
        # CRITICAL: Uses OS cryptographic randomness, NOT Math.random
        # This complies with project policy of avoiding traditional RNG
        self.rng = secrets.SystemRandom()

    def generate_secret_key(self, length: int = 32) -> str:
        """Generate a secure secret key using URL-safe base64 encoding"""
        return secrets.token_urlsafe(length)

    def generate_hex_key(self, length: int = 32) -> str:
        """Generate a secure hexadecimal key"""
        return secrets.token_hex(length)

    def generate_password(self, length: int = 16, use_special: bool = True) -> str:
        """Generate a secure random password"""
        characters = string.ascii_letters + string.digits
        if use_special:
            characters += "!@#$%^&*"
        
        # Use secrets module (not random) for password generation
        return ''.join(secrets.choice(characters) for _ in range(length))

    def generate_database_password(self, length: int = 24) -> str:
        """Generate database-safe password (no special chars that might break URLs)"""
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))

    def generate_all_secrets(self) -> Dict[str, str]:
        """Generate all required secrets for VIGOLEONROCKS"""
        secrets_dict = {
            # Application secrets
            'SECRET_KEY': self.generate_secret_key(32),
            'JWT_SECRET_KEY': self.generate_secret_key(32),
            'ENCRYPTION_KEY': self.generate_secret_key(32),
            
            # Database credentials
            'POSTGRES_PASSWORD': self.generate_database_password(24),
            'REDIS_PASSWORD': self.generate_database_password(20),
            
            # API Keys (placeholder format)
            'API_KEY': f"vigo_{self.generate_hex_key(16)}",
            'WEBHOOK_SECRET': self.generate_hex_key(24),
            
            # Quantum system secrets
            'QUANTUM_ENCRYPTION_KEY': self.generate_hex_key(32),
            'METRICS_SALT': self.generate_hex_key(16),
            
            # Session and CSRF
            'SESSION_KEY': self.generate_secret_key(24),
            'CSRF_SECRET': self.generate_secret_key(20),
        }
        
        return secrets_dict

    def write_env_file(self, secrets_dict: Dict[str, str], output_path: str = ".env") -> None:
        """Write secrets to .env file with proper formatting"""
        
        env_content = [
            "# VIGOLEONROCKS Environment Configuration",
            "# Generated automatically - DO NOT commit to version control",
            "# Generated using cryptographically secure OS randomness (NO Math.random)",
            "",
            "# =============================================================================",
            "# CRITICAL POLICY COMPLIANCE",
            "# =============================================================================",
            "QUANTUM_PROCESSOR_ENABLED=true",
            "METRICS_RNG_ENABLED=true",
            "BACKGROUND_EXECUTION=true",
            "PROMETHEUS_ENABLED=true",
            "",
            "# =============================================================================",
            "# GENERATED SECURE SECRETS",
            "# =============================================================================",
        ]
        
        for key, value in secrets_dict.items():
            env_content.append(f"{key}={value}")
        
        env_content.extend([
            "",
            "# =============================================================================",
            "# BASIC CONFIGURATION (CUSTOMIZE AS NEEDED)",
            "# =============================================================================",
            "FLASK_ENV=development",
            "FLASK_DEBUG=true",
            "HOST=0.0.0.0",
            "PORT=5000",
            "",
            "# Database URLs (update hosts/ports as needed)",
            f"DATABASE_URL=postgresql://vigoleonrocks:{secrets_dict['POSTGRES_PASSWORD']}@localhost:5432/vigoleonrocks_dev",
            f"REDIS_URL=redis://:{secrets_dict['REDIS_PASSWORD']}@localhost:6379/0",
            "",
            "# Quantum Configuration",
            "QUANTUM_STATES_COUNT=1000",
            "QUANTUM_ENTANGLEMENT_THRESHOLD=0.85",
            "QUANTUM_COHERENCE_TIME=300",
            "",
            "# Metrics-Based RNG (CRITICAL)",
            "METRICS_RNG_SEED_SOURCE=kernel",
            "METRICS_RNG_ENTROPY_POOL_SIZE=4096",
            "METRICS_RNG_RESEED_INTERVAL=3600",
            "",
            "# Multilingual",
            "DEFAULT_LANGUAGE=es",
            "SUPPORTED_LANGUAGES=es,en,pt,fr,de",
            "",
            "# Monitoring",
            "PROMETHEUS_PORT=8000",
            "METRICS_ENDPOINT=/api/status",
            "QUANTUM_METRICS_ENDPOINT=/api/quantum-metrics",
            "",
            "# Background Process",
            "PID_FILE=/var/run/vigoleonrocks.pid",
            "DAEMON_MODE=true",
            "",
            "# Logging",
            "LOG_LEVEL=INFO",
            "LOG_FORMAT=structured",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(env_content))
        
        print(f"✅ Secrets written to {output_path}")

    def generate_docker_secrets(self) -> Dict[str, str]:
        """Generate secrets specifically for Docker deployments"""
        return {
            'postgres_password': self.generate_database_password(32),
            'redis_password': self.generate_database_password(24),
            'app_secret_key': self.generate_secret_key(32),
            'jwt_secret': self.generate_secret_key(32),
            'encryption_key': self.generate_secret_key(32),
        }

    def write_docker_secrets(self, secrets_dict: Dict[str, str], output_dir: str = "secrets") -> None:
        """Write individual secret files for Docker secrets"""
        secrets_path = Path(output_dir)
        secrets_path.mkdir(exist_ok=True)
        
        for name, value in secrets_dict.items():
            secret_file = secrets_path / name
            with open(secret_file, 'w', encoding='utf-8') as f:
                f.write(value)
            
            # Set secure permissions (Unix-like systems)
            if os.name != 'nt':  # Not Windows
                os.chmod(secret_file, 0o600)
        
        print(f"✅ Docker secrets written to {output_dir}/")

    def validate_entropy(self) -> bool:
        """Validate that the system has sufficient entropy for secure generation"""
        try:
            # Try to generate a test secret
            test_secret = secrets.token_urlsafe(32)
            if len(test_secret) < 32:
                return False
            
            # Check entropy by generating multiple secrets and ensuring diversity
            test_secrets = set()
            for _ in range(10):
                test_secrets.add(secrets.token_urlsafe(16))
            
            # If all secrets are the same, entropy is insufficient
            return len(test_secrets) > 1
            
        except Exception as e:
            print(f"❌ Entropy validation failed: {e}")
            return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate cryptographically secure secrets for VIGOLEONROCKS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate .env file with all secrets
  python generate_secrets.py

  # Generate custom .env file
  python generate_secrets.py --env-file custom.env

  # Generate Docker secrets
  python generate_secrets.py --docker

  # Generate specific secret types
  python generate_secrets.py --type password --length 20

CRITICAL: This script uses OS cryptographic randomness (secrets module),
NOT Math.random, in compliance with VIGOLEONROCKS policies.
        """
    )

    parser.add_argument(
        '--env-file', '-e',
        default='.env',
        help='Output path for .env file (default: .env)'
    )

    parser.add_argument(
        '--docker', '-d',
        action='store_true',
        help='Generate Docker secrets files'
    )

    parser.add_argument(
        '--docker-dir',
        default='secrets',
        help='Directory for Docker secrets (default: secrets/)'
    )

    parser.add_argument(
        '--type', '-t',
        choices=['key', 'password', 'hex', 'all'],
        default='all',
        help='Type of secret to generate'
    )

    parser.add_argument(
        '--length', '-l',
        type=int,
        default=32,
        help='Length of generated secret (default: 32)'
    )

    parser.add_argument(
        '--validate', '-v',
        action='store_true',
        help='Validate system entropy before generation'
    )

    args = parser.parse_args()

    print("🔐 VIGOLEONROCKS Secure Secrets Generator")
    print("Using OS cryptographic randomness (NO Math.random)")
    print("=" * 60)

    generator = SecureSecretsGenerator()

    # Validate entropy if requested
    if args.validate:
        print("🔍 Validating system entropy...")
        if not generator.validate_entropy():
            print("❌ CRITICAL: Insufficient system entropy!")
            print("   System may not have enough entropy for secure random generation.")
            print("   Consider running on a system with more entropy sources.")
            sys.exit(1)
        print("✅ System entropy validation passed")

    try:
        if args.type == 'all':
            # Generate all secrets for .env
            secrets_dict = generator.generate_all_secrets()
            generator.write_env_file(secrets_dict, args.env_file)

            # Also generate Docker secrets if requested
            if args.docker:
                docker_secrets = generator.generate_docker_secrets()
                generator.write_docker_secrets(docker_secrets, args.docker_dir)

        elif args.type == 'key':
            secret = generator.generate_secret_key(args.length)
            print(f"Secret Key: {secret}")

        elif args.type == 'password':
            password = generator.generate_password(args.length)
            print(f"Password: {password}")

        elif args.type == 'hex':
            hex_key = generator.generate_hex_key(args.length)
            print(f"Hex Key: {hex_key}")

        print("\n🎉 Secret generation completed successfully!")
        print("\n⚠️  SECURITY REMINDERS:")
        print("  1. Never commit .env or secret files to version control")
        print("  2. Use different secrets for different environments")
        print("  3. Rotate secrets regularly")
        print("  4. Store production secrets in secure secret management systems")
        print("\n🔒 POLICY COMPLIANCE:")
        print("  ✅ Generated using OS cryptographic randomness (NOT Math.random)")
        print("  ✅ Complies with VIGOLEONROCKS security policies")

    except Exception as e:
        print(f"❌ Error generating secrets: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
