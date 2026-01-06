#!/usr/bin/env python3
"""
Windows build script for Christ In Song Hymnal
Automates the build process using PyInstaller and Inno Setup
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\\n{'='*70}")
    print(f"{description}")
    print(f"{'='*70}")
    print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"\\n❌ ERROR: {description} failed!")
        print(result.stderr)
        sys.exit(1)
    
    print(f"✅ {description} completed successfully!")
    return result


def main():
    """Main build function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║          CHRIST IN SONG - WINDOWS BUILD SCRIPT                           ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Step 1: Clean previous builds
    print("\\n🧹 Cleaning previous builds...")
    for directory in ['build', 'dist']:
        if Path(directory).exists():
            shutil.rmtree(directory)
            print(f"  Removed: {directory}")
    
    # Step 2: Run PyInstaller
    spec_file = project_root / "installer" / "build_windows.spec"
    run_command(
        ["pyinstaller", "--clean", str(spec_file)],
        "Building executable with PyInstaller"
    )
    
    # Step 3: Verify executable exists
    exe_path = project_root / "dist" / "ChristInSong.exe"
    if not exe_path.exists():
        print(f"\\n❌ ERROR: Executable not found at {exe_path}")
        sys.exit(1)
    
    print(f"\\n✅ Executable created: {exe_path}")
    print(f"   Size: {exe_path.stat().st_size / (1024*1024):.2f} MB")
    
    # Step 4: Check for Inno Setup (optional)
    inno_setup_path = Path("C:/Program Files (x86)/Inno Setup 6/ISCC.exe")
    
    if inno_setup_path.exists():
        print("\\n📦 Creating Windows installer with Inno Setup...")
        iss_file = project_root / "installer" / "windows" / "christ_in_song.iss"
        
        run_command(
            [str(inno_setup_path), str(iss_file)],
            "Building installer with Inno Setup"
        )
        
        installer_path = project_root / "dist" / "ChristInSongSetup_v1.0.0.exe"
        if installer_path.exists():
            print(f"\\n✅ Installer created: {installer_path}")
            print(f"   Size: {installer_path.stat().st_size / (1024*1024):.2f} MB")
    else:
        print("\\n⚠️  Inno Setup not found. Skipping installer creation.")
        print("   Download from: https://jrsoftware.org/isdl.php")
        print("   Install and re-run this script to create installer.")
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                         BUILD COMPLETED!                                  ║
╚══════════════════════════════════════════════════════════════════════════╝

Your application is ready for distribution:

📁 Standalone executable: dist/ChristInSong.exe
   - Can be run directly without installation
   - ~50-100 MB (includes Python + PySide6)

📦 Windows installer: dist/ChristInSongSetup_v1.0.0.exe
   - Professional installer with uninstaller
   - Creates Start Menu shortcuts
   - Desktop icon option

Testing recommendations:
1. Test executable on a clean Windows VM
2. Test installer on a clean Windows VM
3. Verify all features work correctly
4. Check file associations and shortcuts

Distribution:
- Upload to GitHub Releases
- Share installer link with users
- Provide checksums for verification
    """)


if __name__ == "__main__":
    main()