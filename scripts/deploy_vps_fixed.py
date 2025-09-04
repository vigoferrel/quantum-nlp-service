#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS Enhanced VPS Deployment Script
Fixes dependency installation issues and ensures background process compliance
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import argparse
from datetime import datetime

# VPS Configuration
VPS_CONFIG = {
    "host": "srv984842.hstgr.cloud",
    "ip": "72.60.61.49",
    "user": "root",
    "location": "São Paulo, Brazil",
    "deployment_path": "/opt/vigoleonrocks"
}

# Essential files to transfer (optimized structure)
ESSENTIAL_FILES = {
    "directories": [
        "vigoleonrocks/",
        "tests/",
        "scripts/",
        "benchmarks/",
        ".github/"
    ],
    "files": [
        "Makefile",
        "requirements.txt",
        "requirements-dev.txt", 
        "pyproject.toml",
        "pytest.ini",
        ".env.template",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.monitoring.yml",
        "README.md",
        "DEVELOPMENT.md",
        "ARCHITECTURE.md",
        "CONTRIBUTING.md",
        "LICENSE"
    ]
}

class VPSDeployer:
    def __init__(self, force=False):
        self.force = force
        self.deployment_path = VPS_CONFIG["deployment_path"]
        
    def run_ssh_command(self, command, ignore_errors=False):
        """Execute command on VPS via SSH"""
        ssh_cmd = f"ssh {VPS_CONFIG['user']}@{VPS_CONFIG['host']} '{command}'"
        print(f"🔧 Executing: {command}")
        
        try:
            result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
            if result.stdout.strip():
                print(f"📤 Output: {result.stdout.strip()}")
            
            if result.returncode != 0 and not ignore_errors:
                print(f"⚠️  Error: {result.stderr.strip()}")
                if not self.force:
                    raise subprocess.CalledProcessError(result.returncode, ssh_cmd, result.stderr)
                print(f"⚠️  Command failed (continuing): Command failed with exit code {result.returncode}: {result.stderr.strip()}")
            
            return result
        except Exception as e:
            if not ignore_errors:
                print(f"💥 SSH command failed: {e}")
                raise
            return None

    def setup_vps_environment(self):
        """Setup basic VPS environment with fixed dependencies"""
        print("\n🏗️  Preparing VPS environment...")
        
        # Update package lists
        self.run_ssh_command("apt-get update -y")
        
        # Install essential build dependencies first
        essential_packages = [
            "python3",
            "python3-pip", 
            "python3-venv",
            "python3-dev",
            "python3-setuptools",
            "python3-wheel",
            "build-essential",
            "git",
            "make",
            "curl",
            "wget",
            "pkg-config",
            "libpq-dev"
        ]
        
        for package in essential_packages:
            self.run_ssh_command(f"apt-get install -y {package}", ignore_errors=True)
        
        # Fix Docker installation separately to avoid conflicts
        print("\n🐳 Setting up Docker...")
        self.run_ssh_command("apt-get remove -y docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc", ignore_errors=True)
        self.run_ssh_command("curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh", ignore_errors=True)
        self.run_ssh_command("systemctl enable docker", ignore_errors=True)
        self.run_ssh_command("systemctl start docker", ignore_errors=True)
        
        # Create deployment directories
        self.run_ssh_command(f"mkdir -p {self.deployment_path}")
        self.run_ssh_command(f"mkdir -p {self.deployment_path}/logs")
        
        # Create Python virtual environment with proper setuptools
        self.run_ssh_command(f"cd {self.deployment_path} && python3 -m venv venv")
        self.run_ssh_command(f"cd {self.deployment_path} && source venv/bin/activate && pip install --upgrade pip setuptools wheel")
        
        # Set proper ownership
        self.run_ssh_command(f"chown -R root:root {self.deployment_path}")
        
        print("✅ VPS environment prepared")

    def transfer_files(self):
        """Transfer essential project files to VPS"""
        print("\n📤 Transferring optimized files to VPS...")
        
        transferred_count = 0
        
        # Transfer directories
        for directory in ESSENTIAL_FILES["directories"]:
            if os.path.exists(directory):
                scp_cmd = f"scp -r {directory} {VPS_CONFIG['user']}@{VPS_CONFIG['host']}:{self.deployment_path}/"
                try:
                    subprocess.run(scp_cmd, shell=True, check=True, capture_output=True)
                    print(f"📂 Transferring directory: {directory}")
                    transferred_count += 1
                except subprocess.CalledProcessError as e:
                    print(f"⚠️  Failed to transfer directory {directory}: {e}")
        
        # Transfer individual files
        for file_path in ESSENTIAL_FILES["files"]:
            if os.path.exists(file_path):
                scp_cmd = f"scp {file_path} {VPS_CONFIG['user']}@{VPS_CONFIG['host']}:{self.deployment_path}/"
                try:
                    subprocess.run(scp_cmd, shell=True, check=True, capture_output=True)
                    print(f"📁 Transferring file: {file_path}")
                    transferred_count += 1
                except subprocess.CalledProcessError as e:
                    print(f"⚠️  Failed to transfer file {file_path}: {e}")
        
        print(f"✅ Transferred {transferred_count} items to VPS")

    def create_production_config(self):
        """Create optimized production environment configuration"""
        print("\n⚙️  Setting up environment configuration...")
        
        env_config = """# VIGOLEONROCKS Production Environment
# Generated for VPS deployment with policy compliance

# Critical Policy Compliance (MANDATORY)
QUANTUM_PROCESSOR_ENABLED=true
METRICS_RNG_ENABLED=true
BACKGROUND_EXECUTION=true
PROMETHEUS_ENABLED=true

# Application Configuration  
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=prod-vigoleon-quantum-$(date +%s)-secure
HOST=0.0.0.0
PORT=5000

# Database URLs (configure as needed)
DATABASE_URL=postgresql://vigoleonrocks:secure_password@localhost:5432/vigoleonrocks_prod
REDIS_URL=redis://localhost:6379/0

# Quantum Configuration
QUANTUM_STATES_COUNT=1000
QUANTUM_ENTANGLEMENT_THRESHOLD=0.85
QUANTUM_COHERENCE_TIME=300

# Metrics-Based RNG (CRITICAL - No Math.random)
METRICS_RNG_SEED_SOURCE=kernel
METRICS_RNG_ENTROPY_POOL_SIZE=4096
METRICS_RNG_RESEED_INTERVAL=3600
KERNEL_ENTROPY_ENABLED=true

# Multilingual Support
DEFAULT_LANGUAGE=es
SUPPORTED_LANGUAGES=es,en,pt,fr,de

# Background Process Monitoring (MANDATORY)
PROMETHEUS_PORT=8000
METRICS_ENDPOINT=/api/status
QUANTUM_METRICS_ENDPOINT=/api/quantum-metrics
PROCESS_METRICS_ENDPOINT=/api/process-metrics

# Background Daemon Configuration
PID_FILE=/var/run/vigoleonrocks.pid
DAEMON_MODE=true
BACKGROUND_PROCESS=true

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=structured
LOG_FILE=/opt/vigoleonrocks/logs/vigoleonrocks.log
METRICS_LOG_FILE=/opt/vigoleonrocks/logs/metrics.log

# VPS Specific
VPS_HOST=srv984842.hstgr.cloud  
VPS_IP=72.60.61.49
VPS_LOCATION=sao_paulo_brazil

# Performance Optimization
WORKERS=4
THREADS=2
MAX_CONNECTIONS=100
KEEP_ALIVE=2

# Security
CORS_ORIGINS=*
SSL_CONTEXT=adhoc
"""
        
        # Create environment file on VPS
        self.run_ssh_command(f"""cat > {self.deployment_path}/.env << 'EOF'
{env_config}
EOF""")
        
        self.run_ssh_command(f"chmod 600 {self.deployment_path}/.env")
        print("✅ Production environment configuration created")

    def install_dependencies(self):
        """Install Python dependencies with proper error handling"""
        print("\n📦 Installing Python dependencies...")
        
        # Upgrade core packages first
        self.run_ssh_command(f"cd {self.deployment_path} && source venv/bin/activate && pip install --upgrade pip setuptools wheel")
        
        # Create a simplified requirements file for production
        simplified_requirements = """flask==2.3.3
flask-cors==4.0.0
redis==4.6.0
requests==2.31.0
gunicorn==21.2.0
prometheus-client==0.17.1
psutil==5.9.5
"""
        
        # Install simplified requirements first
        self.run_ssh_command(f"""cat > {self.deployment_path}/requirements-simple.txt << 'EOF'
{simplified_requirements}
EOF""")
        
        self.run_ssh_command(f"cd {self.deployment_path} && source venv/bin/activate && pip install -r requirements-simple.txt")
        
        # Try to install full requirements, but don't fail if some packages don't work
        self.run_ssh_command(f"cd {self.deployment_path} && source venv/bin/activate && pip install -r requirements.txt", ignore_errors=True)
        
        print("✅ Dependencies installed")

    def create_systemd_service(self):
        """Create systemd service for background process compliance"""
        print("\n🔧 Creating systemd service for background execution...")
        
        service_content = f"""[Unit]
Description=VIGOLEONROCKS Quantum NLP Service
After=network.target
Requires=network.target

[Service]
Type=forking
User=root
Group=root
WorkingDirectory={self.deployment_path}
Environment=PATH={self.deployment_path}/venv/bin
ExecStart={self.deployment_path}/venv/bin/python -m vigoleonrocks.app --daemon
ExecReload=/bin/kill -HUP $MAINPID
PIDFile=/var/run/vigoleonrocks.pid
Restart=always
RestartSec=10

# Background process compliance
RemainAfterExit=no
KillMode=mixed
TimeoutStopSec=30

# Metrics exposure
ExecStartPost=/bin/sleep 5
ExecStartPost=/bin/bash -c 'echo "Metrics available at http://$(hostname -I | cut -d" " -f1):8000/metrics"'

[Install]
WantedBy=multi-user.target
"""
        
        self.run_ssh_command(f"""cat > /etc/systemd/system/vigoleonrocks.service << 'EOF'
{service_content}
EOF""")
        
        self.run_ssh_command("systemctl daemon-reload")
        self.run_ssh_command("systemctl enable vigoleonrocks.service")
        
        print("✅ Systemd service created and enabled")

    def create_startup_script(self):
        """Create startup script for the application"""
        print("\n📝 Creating application startup script...")
        
        startup_script = f"""#!/bin/bash
# VIGOLEONROCKS Production Startup Script
# Ensures background execution and metrics compliance

cd {self.deployment_path}
source venv/bin/activate

# Load environment variables
source .env

# Start the application in background with metrics
exec python -m vigoleonrocks.app \\
    --host=$HOST \\
    --port=$PORT \\
    --workers=$WORKERS \\
    --daemon \\
    --pid-file=$PID_FILE \\
    --access-logfile={self.deployment_path}/logs/access.log \\
    --error-logfile={self.deployment_path}/logs/error.log \\
    --log-level=$LOG_LEVEL \\
    --bind=0.0.0.0:$PORT \\
    --preload \\
    --enable-stdio-inheritance \\
    --prometheus-enabled \\
    --prometheus-port=$PROMETHEUS_PORT
"""
        
        self.run_ssh_command(f"""cat > {self.deployment_path}/start.sh << 'EOF'
{startup_script}
EOF""")
        
        self.run_ssh_command(f"chmod +x {self.deployment_path}/start.sh")
        print("✅ Startup script created")

    def deploy(self):
        """Execute complete deployment process"""
        print("🚀 VIGOLEONROCKS Enhanced VPS Deployment")
        print(f"🌐 Target: {VPS_CONFIG['host']} ({VPS_CONFIG['ip']}) - {VPS_CONFIG['location']}")
        print("🔒 Policy Compliant: Background processes + Metrics exposure")
        print("=" * 80)
        
        try:
            # Test SSH connection
            print(f"🔗 Connecting to VPS: {VPS_CONFIG['host']}")
            result = self.run_ssh_command("echo 'SSH connection test'")
            if result and result.returncode == 0:
                print(f"✅ SSH connection established to {VPS_CONFIG['host']}")
            
            # Execute deployment steps
            self.setup_vps_environment()
            self.transfer_files()  
            self.create_production_config()
            self.install_dependencies()
            self.create_systemd_service()
            self.create_startup_script()
            
            print("\n🎉 Deployment completed successfully!")
            print("\n📊 Next steps:")
            print(f"1. Start the service: ssh {VPS_CONFIG['user']}@{VPS_CONFIG['host']} 'systemctl start vigoleonrocks'")
            print(f"2. Check status: ssh {VPS_CONFIG['user']}@{VPS_CONFIG['host']} 'systemctl status vigoleonrocks'")
            print(f"3. View logs: ssh {VPS_CONFIG['user']}@{VPS_CONFIG['host']} 'tail -f {self.deployment_path}/logs/vigoleonrocks.log'")
            print(f"4. Access metrics: http://{VPS_CONFIG['ip']}:8000/metrics")
            print(f"5. Access application: http://{VPS_CONFIG['ip']}:5000")
            
        except Exception as e:
            print(f"\n💥 Deployment failed: {e}")
            return False
        
        return True

def main():
    parser = argparse.ArgumentParser(description="Deploy VIGOLEONROCKS to VPS")
    parser.add_argument("--force", action="store_true", help="Continue on errors")
    
    args = parser.parse_args()
    
    deployer = VPSDeployer(force=args.force)
    success = deployer.deploy()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
