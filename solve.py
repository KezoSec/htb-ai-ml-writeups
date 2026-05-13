import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

df = pd.read_csv("uplink_spatial_auth.csv")

# scatter plots
colors = {0: 'red', 1: 'blue', 2: 'green', 3: 'orange'}
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for label, group in df.groupby('label'):
    axes[0].scatter(group['x'], group['y'], c=colors[label], label=f'label {label}', alpha=0.5, s=10)
    axes[1].scatter(group['x'], group['z'], c=colors[label], label=f'label {label}', alpha=0.5, s=10)
    axes[2].scatter(group['y'], group['z'], c=colors[label], label=f'label {label}', alpha=0.5, s=10)

axes[0].set_title('X vs Y')
axes[1].set_title('X vs Z')
axes[2].set_title('Y vs Z')
for ax in axes:
    ax.legend()

plt.tight_layout()
plt.savefig('scatter.png', dpi=150)
print("saved scatter.png")

# reconstruct QR
qr_df = df[df['label'] == 1].copy()
qr_df['x'] = qr_df['x'].round().astype(int)
qr_df['y'] = qr_df['y'].round().astype(int)
qr_df['x'] -= qr_df['x'].min()
qr_df['y'] -= qr_df['y'].min()

width = qr_df['x'].max() + 1
height = qr_df['y'].max() + 1
qr = np.zeros((height, width), dtype=int)

for _, row in qr_df.iterrows():
    qr[int(row['y']), int(row['x'])] = 1

plt.figure(figsize=(6, 6))
plt.imshow(qr, cmap='gray_r', interpolation='nearest')
plt.axis('off')
plt.savefig('qr.png', dpi=150, bbox_inches='tight')
print("saved qr.png")

# decode
result = decode(Image.open('qr.png'))
print("flag:", result[0].data.decode('utf-8'))