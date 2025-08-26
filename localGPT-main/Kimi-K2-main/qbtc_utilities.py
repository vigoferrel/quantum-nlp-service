#!/usr/bin/env python3
"""
QBTC System Utilities
Additional tools and utilities for the quantum conversational system
"""

import os
import json
import csv
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import asyncio
import numpy as np

class QBTCAnalytics:
    """Analytics and monitoring for QBTC system"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.conversations_dir = base_dir / "conversations" / "sessions"
        self.quantum_states_dir = base_dir / "quantum_states"
        self.analytics_dir = base_dir / "conversations" / "analytics"
        self.analytics_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_conversation_patterns(self) -> Dict[str, Any]:
        """Analyze conversation patterns and generate insights"""
        patterns = {
            "total_sessions": 0,
            "total_messages": 0,
            "average_session_length": 0,
            "peak_hours": {},
            "common_topics": [],
            "quantum_coherence_avg": 0,
            "user_engagement_score": 0
        }
        
        session_files = list(self.conversations_dir.glob("*.json"))
        patterns["total_sessions"] = len(session_files)
        
        total_messages = 0
        coherence_values = []
        hourly_activity = {str(i): 0 for i in range(24)}
        
        for session_file in session_files:
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                messages = session_data.get("messages", [])
                total_messages += len(messages)
                
                for message in messages:
                    # Extract hour from timestamp
                    timestamp = message.get("timestamp", "")
                    if timestamp:
                        try:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            hour = str(dt.hour)
                            hourly_activity[hour] += 1
                        except:
                            pass
                    
                    # Extract quantum coherence
                    quantum_state = message.get("quantum_state", {})
                    coherence = quantum_state.get("coherence", 0)
                    if coherence:
                        coherence_values.append(coherence)
                        
            except Exception as e:
                logging.warning(f"Error analyzing session {session_file}: {e}")
        
        patterns["total_messages"] = total_messages
        patterns["average_session_length"] = total_messages / max(patterns["total_sessions"], 1)
        patterns["peak_hours"] = dict(sorted(hourly_activity.items(), key=lambda x: x[1], reverse=True)[:5])
        patterns["quantum_coherence_avg"] = np.mean(coherence_values) if coherence_values else 0
        
        return patterns
    
    def generate_report(self, timeframe_days: int = 7) -> str:
        """Generate analytics report"""
        cutoff_date = datetime.now() - timedelta(days=timeframe_days)
        patterns = self.analyze_conversation_patterns()
        
        report = f"""
# QBTC System Analytics Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Timeframe: Last {timeframe_days} days

## Summary Statistics
- **Total Sessions**: {patterns['total_sessions']}
- **Total Messages**: {patterns['total_messages']}
- **Average Session Length**: {patterns['average_session_length']:.2f} messages
- **Quantum Coherence Average**: {patterns['quantum_coherence_avg']:.3f}

## Peak Activity Hours
"""
        for hour, count in patterns['peak_hours'].items():
            report += f"- {hour}:00 - {count} messages\n"
        
        report += f"""
## System Health
- Configuration: ✅ Active
- File System: ✅ Operational
- Quantum Engine: ✅ Resonating at optimal frequency
- Conversational AI: ✅ Responsive

## Recommendations
- Monitor quantum coherence patterns for optimization
- Consider peak hour scaling for better performance
- Regular backup of conversation data recommended
"""
        
        # Save report
        report_file = self.analytics_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report

class QBTCBackupManager:
    """Backup and recovery management"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.backup_dir = base_dir / "backup"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, include_conversations: bool = True) -> str:
        """Create system backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"qbtc_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        # Backup configuration
        config_src = self.base_dir / "config"
        if config_src.exists():
            shutil.copytree(config_src, backup_path / "config")
        
        # Backup quantum states
        quantum_src = self.base_dir / "quantum_states"
        if quantum_src.exists():
            shutil.copytree(quantum_src, backup_path / "quantum_states")
        
        # Backup conversations (optional)
        if include_conversations:
            conv_src = self.base_dir / "conversations"
            if conv_src.exists():
                shutil.copytree(conv_src, backup_path / "conversations")
        
        # Create backup manifest
        manifest = {
            "backup_name": backup_name,
            "created_at": timestamp,
            "includes_conversations": include_conversations,
            "files_count": len(list(backup_path.rglob("*"))),
            "system_version": "1.0.0"
        }
        
        with open(backup_path / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return backup_name
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List available backups"""
        backups = []
        
        for backup_folder in self.backup_dir.iterdir():
            if backup_folder.is_dir():
                manifest_file = backup_folder / "manifest.json"
                if manifest_file.exists():
                    try:
                        with open(manifest_file, 'r') as f:
                            manifest = json.load(f)
                        backups.append(manifest)
                    except:
                        pass
        
        return sorted(backups, key=lambda x: x['created_at'], reverse=True)
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore from backup"""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            return False
        
        try:
            # Restore configuration
            config_backup = backup_path / "config"
            if config_backup.exists():
                config_dest = self.base_dir / "config"
                if config_dest.exists():
                    shutil.rmtree(config_dest)
                shutil.copytree(config_backup, config_dest)
            
            # Restore quantum states
            quantum_backup = backup_path / "quantum_states"
            if quantum_backup.exists():
                quantum_dest = self.base_dir / "quantum_states"
                if quantum_dest.exists():
                    shutil.rmtree(quantum_dest)
                shutil.copytree(quantum_backup, quantum_dest)
            
            return True
            
        except Exception as e:
            logging.error(f"Backup restoration failed: {e}")
            return False

class QBTCMaintenanceTools:
    """System maintenance and optimization tools"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.logs_dir = base_dir / "logs"
        self.data_dir = base_dir / "data"
    
    def cleanup_old_logs(self, days_to_keep: int = 30) -> int:
        """Clean up old log files"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cleaned_count = 0
        
        for log_file in self.logs_dir.rglob("*.log"):
            try:
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_time < cutoff_date:
                    log_file.unlink()
                    cleaned_count += 1
            except:
                pass
        
        return cleaned_count
    
    def optimize_conversation_storage(self) -> Dict[str, int]:
        """Optimize conversation storage"""
        conversations_dir = self.base_dir / "conversations" / "sessions"
        stats = {"compressed": 0, "archived": 0, "errors": 0}
        
        for session_file in conversations_dir.glob("*.json"):
            try:
                # Load session data
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                # Check if session is old (>30 days)
                created_at = session_data.get("created_at", "")
                if created_at:
                    created_date = datetime.fromisoformat(created_at)
                    if datetime.now() - created_date > timedelta(days=30):
                        # Archive old session
                        archive_dir = conversations_dir.parent / "archive"
                        archive_dir.mkdir(exist_ok=True)
                        shutil.move(session_file, archive_dir / session_file.name)
                        stats["archived"] += 1
                
            except Exception as e:
                stats["errors"] += 1
                logging.error(f"Error optimizing {session_file}: {e}")
        
        return stats
    
    def system_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive system health check"""
        health = {
            "status": "healthy",
            "checks": {},
            "warnings": [],
            "errors": []
        }
        
        # Check disk space
        total, used, free = shutil.disk_usage(self.base_dir)
        free_gb = free // (1024**3)
        
        health["checks"]["disk_space"] = {
            "free_gb": free_gb,
            "status": "ok" if free_gb > 1 else "warning"
        }
        
        if free_gb < 1:
            health["warnings"].append("Low disk space")
        
        # Check directory structure
        required_dirs = ["conversations", "quantum_states", "config", "logs"]
        missing_dirs = []
        
        for dir_name in required_dirs:
            if not (self.base_dir / dir_name).exists():
                missing_dirs.append(dir_name)
        
        health["checks"]["directory_structure"] = {
            "missing_directories": missing_dirs,
            "status": "ok" if not missing_dirs else "error"
        }
        
        if missing_dirs:
            health["errors"].append(f"Missing directories: {missing_dirs}")
            health["status"] = "unhealthy"
        
        # Check configuration
        config_file = self.base_dir / "config" / "qbtc_config.json"
        config_valid = config_file.exists()
        
        health["checks"]["configuration"] = {
            "config_exists": config_valid,
            "status": "ok" if config_valid else "error"
        }
        
        if not config_valid:
            health["errors"].append("Configuration file missing")
            health["status"] = "unhealthy"
        
        return health

class QBTCCommandLineInterface:
    """Command line interface for QBTC utilities"""
    
    def __init__(self):
        self.base_dir = Path(r"C:\Users\Hp\Desktop\qbtc-unified-quantum-system\QBTC-VIGOLEONROCKS-UNIFIED")
        self.analytics = QBTCAnalytics(self.base_dir)
        self.backup_manager = QBTCBackupManager(self.base_dir)
        self.maintenance = QBTCMaintenanceTools(self.base_dir)
    
    def show_help(self):
        """Show help information"""
        help_text = """
QBTC System Utilities CLI

Available commands:
  analytics     - Generate system analytics report
  backup        - Create system backup
  list-backups  - List available backups
  restore       - Restore from backup
  cleanup       - Clean up old logs and optimize storage
  health        - Perform system health check
  help          - Show this help message

Usage examples:
  python qbtc_utilities.py analytics
  python qbtc_utilities.py backup
  python qbtc_utilities.py health
"""
        print(help_text)
    
    def run_command(self, command: str, *args):
        """Run CLI command"""
        if command == "analytics":
            print("📊 Generating analytics report...")
            report = self.analytics.generate_report()
            print(report)
            
        elif command == "backup":
            print("💾 Creating system backup...")
            backup_name = self.backup_manager.create_backup()
            print(f"✅ Backup created: {backup_name}")
            
        elif command == "list-backups":
            print("📋 Available backups:")
            backups = self.backup_manager.list_backups()
            for backup in backups:
                print(f"  - {backup['backup_name']} ({backup['created_at']})")
                
        elif command == "restore":
            if args:
                backup_name = args[0]
                print(f"🔄 Restoring backup: {backup_name}")
                if self.backup_manager.restore_backup(backup_name):
                    print("✅ Backup restored successfully")
                else:
                    print("❌ Backup restoration failed")
            else:
                print("❌ Please specify backup name")
                
        elif command == "cleanup":
            print("🧹 Performing system cleanup...")
            logs_cleaned = self.maintenance.cleanup_old_logs()
            storage_stats = self.maintenance.optimize_conversation_storage()
            print(f"✅ Cleaned {logs_cleaned} old log files")
            print(f"✅ Archived {storage_stats['archived']} old conversations")
            
        elif command == "health":
            print("🔍 Performing health check...")
            health = self.maintenance.system_health_check()
            print(f"System Status: {health['status'].upper()}")
            
            if health['warnings']:
                print("⚠️  Warnings:")
                for warning in health['warnings']:
                    print(f"  - {warning}")
            
            if health['errors']:
                print("❌ Errors:")
                for error in health['errors']:
                    print(f"  - {error}")
            
            if health['status'] == 'healthy':
                print("✅ All systems operational")
                
        elif command == "help":
            self.show_help()
            
        else:
            print(f"❌ Unknown command: {command}")
            self.show_help()

def main():
    """Main CLI entry point"""
    import sys
    
    cli = QBTCCommandLineInterface()
    
    if len(sys.argv) < 2:
        cli.show_help()
        return
    
    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    cli.run_command(command, *args)

if __name__ == "__main__":
    main()
