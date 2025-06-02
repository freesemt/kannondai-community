import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
plt.rcParams['font.family'] = ["MS Gothic"]  # "MS Gothic", "MS Mincho", "Meiryo" 

# サンプルデータ：10人分の能力値（ランダム例）
np.random.seed(0)
abilities = np.random.randint(40, 100, size=10)

# 能力水準
medium_ability = np.mean(abilities)
min_ability = min(abilities)

# 棒グラフ
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(range(1, len(abilities)+1), abilities, color='skyblue', edgecolor='k')

# 水平線
ax.axhline(medium_ability, color='red', linestyle='--', linewidth=2, label=f'平均水準（{medium_ability}）')
# 能力値の最小値を示す線
ax.axhline(min_ability, color='green', linestyle='--', linewidth=2, label=f'最低水準（{min_ability}）')   

# ラベル等
ax.set_xlabel('人')
ax.set_ylabel('ある側面の許容力値')
ax.set_title('人ごとの許容力分布と許容力水準')
ax.set_xticks(range(1, len(abilities)+1))
ax.legend()

plt.tight_layout()
plt.show()

