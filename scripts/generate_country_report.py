"""Generate country-wise analysis and ranking report from the processed policy dataset."""
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / 'data' / 'merged_policy_data.csv'
OUT_DIR = Path(__file__).parent.parent / 'reports'
OUT_DIR.mkdir(exist_ok=True)


def generate_country_ranking():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f'Processed dataset not found: {DATA_PATH}')
    df = pd.read_csv(DATA_PATH)
    # Attempt to find country/authority fields
    if 'Authority' in df.columns:
        counts = df['Authority'].value_counts().rename_axis('Authority').reset_index(name='PolicyCount')
        counts['Rank'] = counts['PolicyCount'].rank(method='dense', ascending=False).astype(int)
        out_csv = OUT_DIR / 'country_policy_ranking.csv'
        counts.to_csv(out_csv, index=False)
        print('Saved ranking to', out_csv)
        # Simple markdown report
        md = ['# Country-wise Policy Ranking', '', f'Generated: {pd.Timestamp.now()}', '']
        md.append(counts.head(50).to_markdown(index=False))
        out_md = OUT_DIR / 'country_policy_ranking.md'
        out_md.write_text('\n'.join(md))
        print('Saved markdown report to', out_md)
        return counts
    else:
        raise ValueError('Authority column not found in processed dataset')


if __name__ == '__main__':
    res = generate_country_ranking()
    print(res.head())
