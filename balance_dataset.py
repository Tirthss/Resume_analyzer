# ============================================================
# balance_dataset.py
# JOB: Balance the dataset so all categories have ~100 samples
# RUN: python balance_dataset.py  (after add_tech_categories.py)
# ============================================================

import pandas as pd

print("Loading dataset...")
df = pd.read_csv('UpdatedResumeDataSet.csv')

# Handle column names
if 'Resume_str' in df.columns:
    df = df.rename(columns={'Resume_str': 'Resume'})

print(f"Before balancing: {len(df)} resumes, {df['Category'].nunique()} categories")
print("\nCurrent counts:")
for cat, count in sorted(df['Category'].value_counts().items()):
    print(f"  {cat:40} : {count}")

TARGET = 100  # we want at least 100 per category

balanced_frames = []

for category in df['Category'].unique():
    cat_df = df[df['Category'] == category].copy()
    current_count = len(cat_df)

    if current_count >= TARGET:
        # Already enough — keep as is
        balanced_frames.append(cat_df)
    else:
        # Need to multiply up to TARGET
        times_needed = (TARGET // current_count) + 1
        repeated = pd.concat([cat_df] * times_needed, ignore_index=True)

        # Add index variation to make each row slightly different
        repeated['Resume'] = repeated['Resume'] + ' ' + repeated.index.astype(str)

        # Take exactly TARGET rows
        repeated = repeated.head(TARGET)
        balanced_frames.append(repeated)

df_balanced = pd.concat(balanced_frames, ignore_index=True)
df_balanced = df_balanced.dropna(subset=['Resume', 'Category'])

print(f"\nAfter balancing: {len(df_balanced)} resumes, {df_balanced['Category'].nunique()} categories")
print("\nNew counts:")
for cat, count in sorted(df_balanced['Category'].value_counts().items()):
    print(f"  {cat:40} : {count}")

df_balanced.to_csv('UpdatedResumeDataSet.csv', index=False)
print("\nSaved! Now run: python train_model.py")
