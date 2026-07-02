import os
import py_compile

errors = []
for root, dirs, files in os.walk(os.getcwd()):
    normalized_root = root.replace('\\', '/').lower()
    if '/venv/' in normalized_root or normalized_root.endswith('/venv') or '/.git/' in normalized_root or normalized_root.endswith('/.git'):
        continue
    for fn in files:
        if fn.endswith('.py'):
            path = os.path.join(root, fn)
            try:
                py_compile.compile(path, doraise=True)
            except Exception as e:
                errors.append((path, str(e)))

if errors:
    for path, err in errors:
        print(f'ERROR: {path}\n{err}\n')
    raise SystemExit(f'{len(errors)} files failed compilation')
print('OK')
