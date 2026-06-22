"""Weekly alert prototype
This script scans the processed policy dataset and prepares a simple weekly alert
summary highlighting newly published policies and significant topic counts.
It prints an email-ready digest; you can wire SMTP settings to send real emails.
"""
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

DATA_PATH = Path(__file__).parent.parent / 'data' / 'merged_policy_data.csv'


def prepare_weekly_digest(days: int = 7):
    if not DATA_PATH.exists():
        print('Processed dataset not found at', DATA_PATH)
        return None
    df = pd.read_csv(DATA_PATH)
    if 'Proposed date' in df.columns:
        df['Proposed date'] = pd.to_datetime(df['Proposed date'], errors='coerce')
        since = datetime.now() - timedelta(days=days)
        recent = df[df['Proposed date'] >= since]
    else:
        recent = df.head(0)

    summary = {
        'new_policies_count': len(recent),
        'top_authorities': recent['Authority'].value_counts().head(6).to_dict() if 'Authority' in recent.columns else {},
        'sample_titles': recent['Official name'].dropna().head(8).tolist() if 'Official name' in recent.columns else []
    }
    return summary


def render_email_body(summary: dict):
    if summary is None:
        return 'No data available for weekly digest.'
    lines = []
    lines.append('AI Policy Weekly Digest')
    lines.append('')
    lines.append(f"New policies in the last period: {summary['new_policies_count']}")
    lines.append('')
    lines.append('Top authorities with new policies:')
    for auth, cnt in summary['top_authorities'].items():
        lines.append(f"- {auth}: {cnt}")
    lines.append('')
    lines.append('Sample new policies:')
    for t in summary['sample_titles']:
        lines.append(f"- {t}")
    return '\n'.join(lines)


if __name__ == '__main__':
    s = prepare_weekly_digest(days=7)
    body = render_email_body(s)
    print(body)
    # TODO: wire to SMTP or a messaging service to send the digest
