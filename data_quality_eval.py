import json
import matplotlib.pyplot as plt

PHON_FEATURES = ['1A','2A','3A','4A','5A','6A','7A','8A','9A',
                 '10A','10B','11A','12A','13A','14A','15A','16A',
                 '17A','18A','19A']

MORPH_FEATURES = ['20A','21A','21B','22A','23A','24A','25A','25B',
                  '26A','27A','28A','29A']

filepath = 'organized_info.json'

with open(filepath) as f:
    data = json.load(f)

languages = list(data.keys())
n = len(languages)

# count how many features each language has data for
phon_pct  = []
morph_pct = []

for lang in languages:
    lang_data = data[lang]
    phon_have  = sum(1 for f in PHON_FEATURES  if f in lang_data)
    morph_have = sum(1 for f in MORPH_FEATURES if f in lang_data)
    phon_pct.append(phon_have  / len(PHON_FEATURES))
    morph_pct.append(morph_have / len(MORPH_FEATURES))

# saves 'usable' languages which are those that have data for at least 50% of features 
# (doesn't necessarily need to be 50% but this could be a good starting point. If we are harsher
# and raise the threshold, this would be more 'accurate' in a sense and could strengthen our analysis)
usable     = [phon_pct[i] >= 0.5 and morph_pct[i] >= 0.5 for i in range(n)]
n_usable   = sum(usable)
print(f"Usable langs(>=50% in both domains): {n_usable} / {n} ")
print(f"{100*n_usable/n:.1f}", "%")

remove_langs = [languages[i] for i in range(n) if not usable[i]]
for lang in remove_langs:
    pass
    #uncomment to print all langs with under 50% of features for each domain
    # print("X  ", lang) 

# how much missing per feature in percents
all_feats = PHON_FEATURES + MORPH_FEATURES
miss_pct  = [100 * sum(1 for lang in languages if f not in data[lang]) / n for f in all_feats]
colors    = ['blue'] * len(PHON_FEATURES) + ['red'] * len(MORPH_FEATURES)

# how much missing per language 
TOTAL_FEATURES = len(PHON_FEATURES) + len(MORPH_FEATURES)

missing_per_language = []

for lang in languages:
    lang_data = data[lang]
    have = sum(1 for f in all_feats if f in lang_data)
    missing_pct = 100 * (1 - have / TOTAL_FEATURES)
    missing_per_language.append(missing_pct)


print("\n --PERCENT OF LANGUAGES MISSING PER FEATURE--")

feature_missing_pct = {}

for f in all_feats:
    missing = sum(1 for lang in languages if f not in data[lang])
    pct_missing = 100 * missing / n
    feature_missing_pct[f] = pct_missing

for f in feature_missing_pct:
    pct = feature_missing_pct[f]
    print(f, ":", round(pct, 2), "% missing")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# plot 1: % missing per feature
ax1.bar(range(len(all_feats)), miss_pct, color=colors)
# label for feature names
ax1.set_xticks(range(len(all_feats)))
ax1.set_xticklabels(all_feats, rotation=90, fontsize=8)
ax1.set_ylabel("% of languages missing this feature")
ax1.set_ylim(0, 105)
ax1.set_title("How much data is missing per feature?\n(blue = phonological, red = morphological)")

ax1.legend(fontsize=9)

# plot 2: boxplot for distribution
ax2.boxplot(missing_per_language, vert=True)
ax2.set_ylabel("% of features missing")
ax2.set_title("distribution of percent of features missing across languages")
ax2.set_xticks([])

plt.tight_layout()
plt.show()

