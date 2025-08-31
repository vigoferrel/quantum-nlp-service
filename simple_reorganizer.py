#!/usr/bin/env python3
"""
Simple VIGOLEONROCKS Reorganizer with Windows compatibility
"""

import os
import shutil
import json
import time
from pathlib import Path
from datetime import datetime
import logging

def setup_logging(project_root):
    """Setup logging"""
    log_file = project_root / "reorganizer.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(str(log_file), encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def create_target_structure(project_root):
    """Create target directory structure"""
    structure = {
        'vigoleonrocks-core': ['models', 'consciousness', 'quantum', 'unified-brain'],
        'domain': ['services', 'handlers', 'processors', 'managers'],
        'application': ['use-cases', 'workflows', 'orchestration'],
        'infrastructure': ['database', 'storage', 'messaging', 'external-apis'],
        'interfaces': ['rest-api', 'graphql', 'websockets', 'ui', 'cli'],
        'integrations': ['openrouter', 'docker', 'quantum-systems', 'ai-providers'],
        'config': ['environments', 'settings', 'schemas'],
        'tests': ['unit', 'integration', 'e2e', 'performance'],
        'docs': ['technical', 'user-guides', 'api-docs', 'architecture'],
        'tools': ['dev-tools', 'scripts', 'generators', 'analyzers'],
        'deployment': ['docker', 'kubernetes', 'ci-cd', 'monitoring'],
        'security': ['authentication', 'authorization', 'encryption', 'certificates']
    }
    
    new_structure_dir = project_root / "_new_optimized_structure"
    
    if new_structure_dir.exists():
        shutil.rmtree(new_structure_dir)
    
    new_structure_dir.mkdir(parents=True, exist_ok=True)
    
    # Create structure
    for main_dir, subdirs in structure.items():
        main_path = new_structure_dir / main_dir
        main_path.mkdir(parents=True, exist_ok=True)
        
        for subdir in subdirs:
            (main_path / subdir).mkdir(parents=True, exist_ok=True)
        
        # Create README
        readme_content = f"""# {main_dir.title()}

Directory for {main_dir} components of VIGOLEONROCKS.

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        (main_path / "README.md").write_text(readme_content, encoding='utf-8')
    
    return new_structure_dir

def create_backup(project_root, logger):
    """Create backup with simpler approach"""
    backup_dir = project_root / "_backup_original_structure"
    
    # Remove existing backup
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    
    # Create backup directory
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"📦 Creating backup in {backup_dir}")
    
    # Copy files and directories
    items_copied = 0
    for item in project_root.iterdir():
        if item.name.startswith('_') or item.name.startswith('.'):
            continue
            
        try:
            if item.is_dir():
                dest = backup_dir / item.name
                logger.info(f"  Copying directory: {item.name}")
                shutil.copytree(item, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                items_copied += 1
            else:
                logger.info(f"  Copying file: {item.name}")
                shutil.copy2(item, backup_dir)
                items_copied += 1
        except Exception as e:
            logger.warning(f"  ⚠️ Could not copy {item.name}: {e}")
    
    logger.info(f"✅ Backup completed: {items_copied} items copied")
    return backup_dir

def categorize_directories(project_root, logger):
    """Categorize directories based on patterns"""
    categories = {
        'vigoleonrocks-core': ['vigoleonrocks', 'quantum', 'consciousness', 'brain', 'core'],
        'interfaces': ['api', 'ui', 'web', 'server', 'client'],
        'tests': ['test', 'spec', 'mock', 'benchmark'],
        'docs': ['doc', 'readme', 'guide', 'paper'],
        'config': ['config', 'env', 'setting'],
        'tools': ['tool', 'script', 'util', 'helper'],
        'deployment': ['docker', 'k8s', 'deploy', 'helm'],
        'domain': ['service', 'handler', 'processor', 'manager'],
        'infrastructure': ['database', 'storage', 'cache', 'repository']
    }
    
    mappings = {}
    
    for root, dirs, files in os.walk(project_root):
        if '_backup_' in root or '_new_optimized_' in root or '.git' in root:
            continue
            
        current_path = Path(root)
        if current_path == project_root:
            continue
            
        relative_path = current_path.relative_to(project_root)
        dir_name = current_path.name.lower()
        
        # Skip if no files
        if not files:
            continue
        
        # Categorize based on directory name
        target_category = 'application'  # default
        
        for category, patterns in categories.items():
            if any(pattern in dir_name for pattern in patterns):
                target_category = category
                break
        
        mappings[str(relative_path)] = target_category
    
    return mappings

def move_directories(project_root, mappings, new_structure_dir, logger):
    """Move directories to new structure"""
    moved_count = 0
    errors = []
    
    for src_path, target_category in mappings.items():
        src = project_root / src_path
        
        if not src.exists():
            continue
            
        dir_name = src.name
        dest = new_structure_dir / target_category / dir_name
        
        try:
            # Ensure destination parent exists
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Move directory
            shutil.move(str(src), str(dest))
            logger.info(f"  ✅ Moved: {src_path} -> {target_category}/{dir_name}")
            moved_count += 1
            
        except Exception as e:
            error_msg = f"Error moving {src_path}: {e}"
            logger.error(f"  ❌ {error_msg}")
            errors.append(error_msg)
    
    return moved_count, errors

def generate_report(project_root, mappings, moved_count, errors, duration):
    """Generate simple report"""
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'duration_seconds': duration,
        'directories_moved': moved_count,
        'total_mappings': len(mappings),
        'errors': errors,
        'mappings': mappings
    }
    
    # Save JSON report
    report_file = project_root / "reorganization_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Generate text report
    text_report = f"""
VIGOLEONROCKS REORGANIZATION REPORT
==================================

Timestamp: {report['timestamp']}
Duration: {duration:.2f} seconds

RESULTS:
--------
• Total directories mapped: {len(mappings)}
• Directories moved: {moved_count}
• Errors: {len(errors)}

DIRECTORY MAPPINGS:
------------------
"""
    
    for src, dest in mappings.items():
        text_report += f"  {src} -> {dest}\n"
    
    if errors:
        text_report += "\nERRORS:\n-------\n"
        for error in errors:
            text_report += f"  • {error}\n"
    
    text_report += f"""
NEW STRUCTURE:
--------------
📁 _new_optimized_structure/
  ├── vigoleonrocks-core/
  ├── domain/
  ├── application/
  ├── infrastructure/
  ├── interfaces/
  ├── integrations/
  ├── config/
  ├── tests/
  ├── docs/
  ├── tools/
  ├── deployment/
  └── security/

BACKUP LOCATION:
---------------
📦 _backup_original_structure/

===============================
"""
    
    text_file = project_root / "reorganization_report.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(text_report)

def main():
    """Main reorganization function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    VIGOLEONROCKS SIMPLE REORGANIZER                          ║
║                               Version 1.0                                   ║
║                                                                              ║
║              Simple architectural reorganization for Windows                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    project_root = Path(__file__).parent.resolve()
    logger = setup_logging(project_root)
    
    print(f"📁 Project: {project_root}")
    
    # Confirm execution
    confirm = input("⚠️ Are you sure you want to execute the reorganization? (yes/no): ")
    if confirm.lower() not in ['yes', 'y', 'si', 'sí']:
        print("❌ Operation cancelled")
        return
    
    start_time = time.time()
    
    try:
        logger.info("🚀 Starting VIGOLEONROCKS reorganization")
        
        # Step 1: Create backup
        backup_dir = create_backup(project_root, logger)
        
        # Step 2: Create target structure
        logger.info("🏗️ Creating target structure")
        new_structure_dir = create_target_structure(project_root)
        
        # Step 3: Categorize directories
        logger.info("🔍 Categorizing directories")
        mappings = categorize_directories(project_root, logger)
        
        # Step 4: Move directories
        logger.info("📦 Moving directories")
        moved_count, errors = move_directories(project_root, mappings, new_structure_dir, logger)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Step 5: Generate report
        logger.info("📊 Generating report")
        generate_report(project_root, mappings, moved_count, errors, duration)
        
        print(f"\n{'='*80}")
        print("🎉 REORGANIZATION COMPLETED")
        print("="*80)
        print(f"⏱️ Duration: {duration:.2f} seconds")
        print(f"📁 Directories moved: {moved_count}/{len(mappings)}")
        print(f"❌ Errors: {len(errors)}")
        
        if errors:
            print("\nErrors encountered:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  • {error}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more (see report for details)")
        
        print(f"\n📋 Reports generated:")
        print(f"  • reorganization_report.json")
        print(f"  • reorganization_report.txt")
        print(f"\n📁 New structure: _new_optimized_structure/")
        print(f"📦 Backup: _backup_original_structure/")
        
        logger.info("✅ Reorganization completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Critical error: {e}")
        print(f"\n❌ Error during reorganization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
