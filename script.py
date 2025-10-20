import os, subprocess, shutil
BASE_DIR = input("Path to your folder: ")
def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=True, text=True, capture_output=True)
    if r.returncode != 0: print(f"[!] Error in {cwd}: {r.stderr.strip()}")
    return r.stdout.strip()
def create_bash_script(exe_path):
    f = os.path.dirname(exe_path)
    n = os.path.basename(exe_path)
    b = os.path.join(f, f"{os.path.splitext(n)[0]}.sh")
    c = f"""#!/bin/bash
cd "$(dirname "$0")"
echo "Running {n}..."
wine "{n}" || ./"{n}" "$@"
"""
    with open(b,"w") as x: x.write(c)
    os.chmod(b,0o755)
    print(f"[✓] Bash script created: {b}")

def build_exe(project_path, py_file):
    name,_=os.path.splitext(py_file)
    mode="--noconsole" if "gui" in name.lower() else ""
    print(f"→ Building {py_file} in {project_path}")
    extra_files=[]
    sep=":" if os.name!="nt" else ";"
    for item in os.listdir(project_path):
        if item.endswith(".py") or item.startswith("run_") or item.startswith("credentials") or item.endswith(".env") or item in ["build","dist","__pycache__",".git",".github",".vscode",".idea",".DS_Store"]: continue
        extra_files.append(f'--add-data "{item}{sep}."')
    extras=" ".join(extra_files)
    cmd=f'pyinstaller --onefile {mode} {extras} "{py_file}"'
    run(cmd, cwd=project_path)
    exe_name = f"run_{name}.exe" if os.name == "nt" else f"run_{name}"
    exe = os.path.join(project_path, "dist", exe_name)
    out = os.path.join(project_path, exe_name)
    if os.path.exists(exe):
        shutil.move(exe, out)
        print(f"[✓] Built: {out}")
        create_bash_script(out)
    else:
        alt_exe = os.path.join(project_path, "dist", name)
        if os.path.exists(alt_exe):
            shutil.move(alt_exe, out)
            print(f"[✓] Built (no .exe extension): {out}")
            create_bash_script(out)
        else:
            print(f"[x] Failed to build {py_file}")
            return
    for t in ["build","dist",f"{name}.spec"]:
        p=os.path.join(project_path,t)
        if os.path.exists(p):
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
def main():
    if not shutil.which("pyinstaller"):
        print("[!] Please install PyInstaller: pip install pyinstaller")
        return
    if not os.path.exists(BASE_DIR):
        print(f"[!] Directory not found: {BASE_DIR}")
        return
    for folder in os.listdir(BASE_DIR):
        path=os.path.join(BASE_DIR,folder)
        if os.path.isdir(path):
            py_files=[f for f in os.listdir(path) if f.endswith(".py")]
            for py in py_files: build_exe(path,py)
    print("\n[✓] All projects built successfully.")
main()
