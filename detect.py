import importlib

required_packages = [
    "transformers",
    "torch",
    "json",
    "re"
]

print("🔍 Checking Python dependencies...\n")
for pkg in required_packages:
    try:
        importlib.import_module(pkg)
        print(f" {pkg} installed")
    except ImportError:
        print(f"Missing package: {pkg}")