#!/usr/bin/env python3
"""
Deployment Validation Checklist
Verifies all files needed for deployment to Render/cloud platforms
"""

import os
import sys
from pathlib import Path

def check_deployment():
    """Verify all deployment requirements"""
    
    base_path = Path(__file__).parent
    checks = []
    
    # Essential files
    essential_files = [
        'Procfile',
        'runtime.txt',
        'gunicorn_config.py',
        '.gitignore',
        'requirements.txt',
        'fertilizer_deployment/app.py',
    ]
    
    # Model files
    model_files = [
        'fertilizer_deployment/model/random_forest_model.pkl',
        'fertilizer_deployment/model/le_soil.pkl',
        'fertilizer_deployment/model/le_crop.pkl',
        'fertilizer_deployment/model/le_fertilizer.pkl',
    ]
    
    print("🔍 Deployment Validation Checklist\n")
    print("=" * 50)
    
    # Check essential files
    print("\n📋 Essential Deployment Files:")
    for file in essential_files:
        file_path = base_path / file
        exists = file_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
        checks.append(exists)
    
    # Check model files
    print("\n🤖 ML Model Files:")
    for file in model_files:
        file_path = base_path / file
        exists = file_path.exists()
        size = f"({file_path.stat().st_size / 1024 / 1024:.2f} MB)" if exists else ""
        status = "✅" if exists else "❌"
        print(f"  {status} {file} {size}")
        checks.append(exists)
    
    # Dependencies check
    print("\n📦 Dependencies (from requirements.txt):")
    req_file = base_path / "fertilizer_deployment/requirements.txt"
    if req_file.exists():
        with open(req_file) as f:
            content = f.read()
            has_flask = "flask" in content.lower()
            has_gunicorn = "gunicorn" in content.lower()
            has_scikit = "scikit-learn" in content.lower()
            print(f"  {'✅' if has_flask else '❌'} Flask (web framework)")
            print(f"  {'✅' if has_gunicorn else '❌'} Gunicorn (production server)")
            print(f"  {'✅' if has_scikit else '❌'} Scikit-learn (ML library)")
            checks.extend([has_flask, has_gunicorn, has_scikit])
    
    # Summary
    print("\n" + "=" * 50)
    total_checks = len(checks)
    passed_checks = sum(checks)
    
    if all(checks):
        print(f"\n✅ All {total_checks} checks passed!")
        print("\n🚀 Ready to deploy! Next steps:")
        print("  1. git init && git add . && git commit -m 'Initial commit'")
        print("  2. Push to GitHub")
        print("  3. Connect GitHub to Render.com")
        print("  4. Your app will be live in 2-5 minutes!")
        return 0
    else:
        print(f"\n⚠️  {passed_checks}/{total_checks} checks passed")
        print("\n❌ Missing files detected. Fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(check_deployment())
