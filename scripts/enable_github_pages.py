import json
import subprocess
import urllib.request

OWNER = 'HoDcseDMICE'
REPO = 'ai-policy-dashboard'
TEMPLATE = {
    'source': {
        'branch': 'main',
        'path': 'docs'
    }
}

try:
    token = subprocess.check_output(['gh', 'auth', 'token'], text=True).strip()
except subprocess.CalledProcessError as e:
    raise SystemExit('Failed to get GitHub auth token: ' + str(e))

url = f'https://api.github.com/repos/{OWNER}/{REPO}/pages'
req = urllib.request.Request(url, method='PUT')
req.add_header('Authorization', f'Bearer {token}')
req.add_header('Accept', 'application/vnd.github+json')
req.add_header('Content-Type', 'application/json')
body = json.dumps(TEMPLATE).encode('utf-8')

try:
    with urllib.request.urlopen(req, body) as resp:
        print(resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('ERROR', e.code)
    print(e.read().decode('utf-8'))
    raise
