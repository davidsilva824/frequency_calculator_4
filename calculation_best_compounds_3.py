### best combinations that p0riveliege diminishing the difference between regulars and irregulars
### it uses ony four groups of man/men 
import itertools

num_answers= 10
num_stimuli = 12

# ---- helpers ----
GROUP_KEYS = ("irr_sg","irr_pl","reg_sg","reg_pl")  # requested order

def pack(irr_sg, irr_pl, reg_sg, reg_pl):
    # each: (word, SUBTLEX, B10, B100)
    return {"irr_sg": irr_sg, "irr_pl": irr_pl, "reg_sg": reg_sg, "reg_pl": reg_pl}

def gap(vals):
    return max(vals) - min(vals)

def score_combo(packs_subset):
    K = len(packs_subset)
    sums = [[0.0, 0.0, 0.0] for _ in range(4)]  # groups x columns
    for P in packs_subset:
        for gi, key in enumerate(GROUP_KEYS):
            _, s, b10, b100 = P[key]
            sums[gi][0] += s; sums[gi][1] += b10; sums[gi][2] += b100
    means = [[sums[g][c]/K for c in range(3)] for g in range(4)]
    gaps = [gap([means[g][c] for g in range(4)]) for c in range(3)]
    return max(gaps), sum(gaps), gaps, means

def show(ids, packs, gaps, means):
    print("Combo IDs:", ids)
    for idx in ids:
        P = packs[idx]
        a,b,c,d = P["irr_sg"], P["irr_pl"], P["reg_sg"], P["reg_pl"]
        print(f"  {a[0]}/{b[0]} — {c[0]}/{d[0]}")
    labels = ["SUBTLEX","BabyLM-10M","BabyLM-100M"]
    print("Group means (Irr-SG / Irr-PL / Reg-SG / Reg-PL):")
    for ci, lab in enumerate(labels):
        col = [means[g][ci] for g in range(4)]
        print(f"  {lab:11s}: " + "  ".join(f"{x:.3f}" for x in col) +
              f"   | gap={max(col)-min(col):.3f}")
    print("Gaps per column:", " / ".join(f"{g:.3f}" for g in gaps))
    print("-"*60)

# ---- 24 four-packs (irr_sg, irr_pl, reg_sg, reg_pl) ----
packs = [
    pack(("goose",4.02777,4.04625,4.22590), ("geese",3.65190,3.54185,3.81799),
         ("swan",3.98376,3.86061,3.83010), ("swans",3.70688,3.50407,3.42038)),
    pack(("goose",4.02777,4.04625,4.22590), ("geese",3.65190,3.54185,3.81799),
         ("duck",4.52952,5.13569,4.95029), ("ducks",3.92771,4.35662,4.38682)),
    pack(("louse",2.66886,2.46267,2.68082), ("lice",3.28680,3.13168,3.04753),
         ("mite",3.08313,3.32797,3.32908), ("mites",3.27780,2.46267,2.89911)),
    pack(("louse",2.66886,2.46267,2.68082), ("lice",3.28680,3.13168,3.04753),
         ("flea",3.49988,3.16164,3.38156), ("fleas",3.45389,2.46267,3.21851)),
    pack(("child", 5.14472, 5.68400, 5.50831), ("children", 5.52835, 5.52085, 5.50545),
         ("adult", 4.40331, 4.29942, 4.71605), ("adults", 4.27277, 4.08936, 4.16001)),
    pack(("mouse",4.41482,4.63586,4.80005), ("mice",3.91164,4.08936,4.19474),
         ("rat",4.22555,4.12857,4.20520), ("rats",4.02838,3.94934,4.00640)),
    pack(("woman",5.22085,5.36322,5.36451), ("women",5.28064,5.17616,5.24917),
         ("girl",5.29345,5.71423,5.70143), ("girls",5.22702,5.31617,5.34394)),
    pack(("man",5.85755,5.98106,5.99202), ("men",5.36528,5.57315,5.59830),
         ("boy",5.27610,5.77351,5.75638), ("boys",5.19912,5.40203,5.43891)),
    pack(("salesman",3.69005,3.56534,3.45749), ("salesmen",2.95341,2.93979,2.71490),
         ("vendor",3.12062,2.98555,2.94001), ("vendors",2.97220,2.58761,2.89911)),
    pack(("salesman",3.69005,3.56534,3.45749), ("salesmen",2.95341,2.93979,2.71490),
         ("retailer",3.63074,2.68452,2.90444), ("retailers",3.91663,2.76370,2.81670)),
    pack(("salesman",3.69005,3.56534,3.45749), ("salesmen",2.95341,2.93979,2.71490),
         ("merchant",3.78245,4.02298,4.15379), ("merchants",3.44081,3.54185,3.82695)),
    pack(("tooth",4.08773,3.96328,4.11284), ("teeth",4.70053,4.82878,4.90913),
         ("bone",4.51390,4.41043,4.45257), ("bones",4.42982,4.50930,4.46426)),
    pack(("foot",4.91934,5.09072,5.10584), ("feet",5.07716,5.31637,5.35163),
         ("leg",4.87632,4.76298,4.81129), ("legs",4.85298,4.93494,4.96283)),
    pack(("foot", 4.91934, 5.09072, 5.10584), ("feet", 5.07716, 5.31637, 5.35163),
         ("hand", 5.43662, 5.6605, 5.66254), ("hands", 5.24962, 5.45962, 5.48105)),
    pack(("nobleman",2.82284,3.26431,3.33305), ("noblemen",2.53458,2.46267,3.02001),
         ("aristocrat",3.08843,2.28658,2.89371), ("aristocrats",3.08313,2.88864,2.90970)),
    pack(("nobleman",2.82284,3.26431,3.33305), ("noblemen",2.53458,2.46267,3.02001),
         ("courtier",2.65952,2.88864,2.77595), ("courtiers",2.92618,2.76370,3.13984)),
    pack(("boatman",2.62515,2.83065,3.31284), ("boatmen",2.64022,2.83065,2.84796),
         ("shipmate",2.34895,2.76370,2.77595), ("shipmates",2.60955,3.06473,3.18375)),
    pack(("craftsman",3.25684,3.02694,2.79680), ("craftsmen",3.44081,2.83065,2.94001),
         ("labourer",3.10398,3.13168,2.90970), ("labourers",3.11071,3.21600,3.13675)),
    pack(("fisherman",3.75073,3.49070,3.73959), ("fishermen",3.99284,3.63876,3.64480),
         ("gardener",3.87872,3.61902,3.94050), ("gardeners",3.74262,3.02694,3.18375)),
    pack(("ox",3.39209,3.52962,3.88383), ("oxen",2.90525,3.82440,3.73648),
         ("ram",3.65334,3.89404,3.98757), ("rams",3.29013,3.32797,3.17247)),
    pack(("ox",3.39209,3.52962,3.88383), ("oxen",2.90525,3.82440,3.73648),
         ("cow",4.44011,4.84529,4.99550), ("cows",4.25276,4.30152,4.41124)),
    pack(("policeman",4.06178,4.44795,4.40577), ("policemen",3.62053,3.84288,3.69219),
         ("detective",4.25540,4.46122,4.43279), ("detectives",3.85830,3.65765,3.59701)),
    pack(("fireman",3.48107,4.10282,4.43763), ("firemen",3.29996,3.66679,3.77738),
         ("lifeguard",2.96525,2.28658,2.69819), ("lifeguards",2.74106,2.46267,2.37084)),
     pack(("fireman", 3.48107, 4.10282, 4.43763), ("firemen", 3.29996, 3.66679, 3.77738),
         ("gardener", 3.87872, 3.61902, 3.94050), ("gardeners", 3.74262, 3.02694, 3.18375)),
]

# precompute word sets (for no repeats)
pack_words = [{P[k][0] for k in GROUP_KEYS} for P in packs]

# count words ending in 'man' or 'men' (exclude 'woman'/'women')
def is_man_men_word(w: str) -> bool:
    if w.endswith("woman") or w.endswith("women"):
        return False
    return w.endswith("man") or w.endswith("men")

# per-pack count of such words
pack_manmen_counts = [
    sum(1 for k in GROUP_KEYS if is_man_men_word(P[k][0]))
    for P in packs
]

# ---- exhaustive search (no repeats) ----

best = []  # (obj_main, obj_sum, gaps, means, ids)

for ids in itertools.combinations(range(len(packs)), num_stimuli):
    # limit total words with man/men (excluding woman/women) to <= 4
    if sum(pack_manmen_counts[i] for i in ids) > 4:
        continue

    used = set()
    ok = True
    for i in ids:
        if used & pack_words[i]:
            ok = False
            break
        used |= pack_words[i]
    if not ok:
        continue

    obj_main, obj_sum, gaps, means = score_combo([packs[i] for i in ids])
    rec = (obj_main, obj_sum, gaps, means, ids)
    best.append(rec)
    best.sort(key=lambda x: (x[0], x[1]))
    if len(best) > num_answers:
        best.pop()

# ---- report ----
for rank, (obj_main, obj_sum, gaps, means, ids) in enumerate(best, 1):
    print(f"Rank {rank}: objective={obj_main:.6f}  sum_gaps={obj_sum:.6f}")
    show(ids, packs, gaps, means)
import itertools

num_answers= 10
num_stimuli = 12

# ---- helpers ----
GROUP_KEYS = ("irr_sg","irr_pl","reg_sg","reg_pl")  # requested order

def pack(irr_sg, irr_pl, reg_sg, reg_pl):
    # each: (word, SUBTLEX, B10, B100)
    return {"irr_sg": irr_sg, "irr_pl": irr_pl, "reg_sg": reg_sg, "reg_pl": reg_pl}

def gap(vals):
    return max(vals) - min(vals)

def score_combo(packs_subset):
    K = len(packs_subset)
    sums = [[0.0, 0.0, 0.0] for _ in range(4)]  # groups x columns
    for P in packs_subset:
        for gi, key in enumerate(GROUP_KEYS):
            _, s, b10, b100 = P[key]
            sums[gi][0] += s; sums[gi][1] += b10; sums[gi][2] += b100
    means = [[sums[g][c]/K for c in range(3)] for g in range(4)]
    gaps = [gap([means[g][c] for g in range(4)]) for c in range(3)]
    return max(gaps), sum(gaps), gaps, means

def show(ids, packs, gaps, means):
    print("Combo IDs:", ids)
    for idx in ids:
        P = packs[idx]
        a,b,c,d = P["irr_sg"], P["irr_pl"], P["reg_sg"], P["reg_pl"]
        print(f"  {a[0]}/{b[0]} — {c[0]}/{d[0]}")
    labels = ["SUBTLEX","BabyLM-10M","BabyLM-100M"]
    print("Group means (Irr-SG / Irr-PL / Reg-SG / Reg-PL):")
    for ci, lab in enumerate(labels):
        col = [means[g][ci] for g in range(4)]
        print(f"  {lab:11s}: " + "  ".join(f"{x:.3f}" for x in col) +
              f"   | gap={max(col)-min(col):.3f}")
    print("Gaps per column:", " / ".join(f"{g:.3f}" for g in gaps))
    print("-"*60)

# ---- 24 four-packs (irr_sg, irr_pl, reg_sg, reg_pl) ----
packs = [
    pack(("goose",4.02777,4.04625,4.22590), ("geese",3.65190,3.54185,3.81799),
         ("swan",3.98376,3.86061,3.83010), ("swans",3.70688,3.50407,3.42038)),
    pack(("goose",4.02777,4.04625,4.22590), ("geese",3.65190,3.54185,3.81799),
         ("duck",4.52952,5.13569,4.95029), ("ducks",3.92771,4.35662,4.38682)),
    pack(("louse",2.66886,2.46267,2.68082), ("lice",3.28680,3.13168,3.04753),
         ("mite",3.08313,3.32797,3.32908), ("mites",3.27780,2.46267,2.89911)),
    pack(("louse",2.66886,2.46267,2.68082), ("lice",3.28680,3.13168,3.04753),
         ("flea",3.49988,3.16164,3.38156), ("fleas",3.45389,2.46267,3.21851)),
    pack(("child", 5.14472, 5.68400, 5.50831), ("children", 5.52835, 5.52085, 5.50545),
         ("adult", 4.40331, 4.29942, 4.71605), ("adults", 4.27277, 4.08936, 4.16001)),
    pack(("mouse",4.41482,4.63586,4.80005), ("mice",3.91164,4.08936,4.19474),
         ("rat",4.22555,4.12857,4.20520), ("rats",4.02838,3.94934,4.00640)),
    pack(("woman",5.22085,5.36322,5.36451), ("women",5.28064,5.17616,5.24917),
         ("girl",5.29345,5.71423,5.70143), ("girls",5.22702,5.31617,5.34394)),
    pack(("man",5.85755,5.98106,5.99202), ("men",5.36528,5.57315,5.59830),
         ("boy",5.27610,5.77351,5.75638), ("boys",5.19912,5.40203,5.43891)),
    pack(("salesman",3.69005,3.56534,3.45749), ("salesmen",2.95341,2.93979,2.71490),
         ("vendor",3.12062,2.98555,2.94001), ("vendors",2.97220,2.58761,2.89911)),
    pack(("salesman",3.69005,3.56534,3.45749), ("salesmen",2.95341,2.93979,2.71490),
         ("retailer",3.63074,2.68452,2.90444), ("retailers",3.91663,2.76370,2.81670)),
    pack(("salesman",3.69005,3.56534,3.45749), ("salesmen",2.95341,2.93979,2.71490),
         ("merchant",3.78245,4.02298,4.15379), ("merchants",3.44081,3.54185,3.82695)),
    pack(("tooth",4.08773,3.96328,4.11284), ("teeth",4.70053,4.82878,4.90913),
         ("bone",4.51390,4.41043,4.45257), ("bones",4.42982,4.50930,4.46426)),
    pack(("foot",4.91934,5.09072,5.10584), ("feet",5.07716,5.31637,5.35163),
         ("leg",4.87632,4.76298,4.81129), ("legs",4.85298,4.93494,4.96283)),
    pack(("foot", 4.91934, 5.09072, 5.10584), ("feet", 5.07716, 5.31637, 5.35163),
         ("hand", 5.43662, 5.6605, 5.66254), ("hands", 5.24962, 5.45962, 5.48105)),
    pack(("nobleman",2.82284,3.26431,3.33305), ("noblemen",2.53458,2.46267,3.02001),
         ("aristocrat",3.08843,2.28658,2.89371), ("aristocrats",3.08313,2.88864,2.90970)),
    pack(("nobleman",2.82284,3.26431,3.33305), ("noblemen",2.53458,2.46267,3.02001),
         ("courtier",2.65952,2.88864,2.77595), ("courtiers",2.92618,2.76370,3.13984)),
    pack(("boatman",2.62515,2.83065,3.31284), ("boatmen",2.64022,2.83065,2.84796),
         ("shipmate",2.34895,2.76370,2.77595), ("shipmates",2.60955,3.06473,3.18375)),
    pack(("craftsman",3.25684,3.02694,2.79680), ("craftsmen",3.44081,2.83065,2.94001),
         ("labourer",3.10398,3.13168,2.90970), ("labourers",3.11071,3.21600,3.13675)),
    pack(("fisherman",3.75073,3.49070,3.73959), ("fishermen",3.99284,3.63876,3.64480),
         ("gardener",3.87872,3.61902,3.94050), ("gardeners",3.74262,3.02694,3.18375)),
    pack(("ox",3.39209,3.52962,3.88383), ("oxen",2.90525,3.82440,3.73648),
         ("ram",3.65334,3.89404,3.98757), ("rams",3.29013,3.32797,3.17247)),
    pack(("ox",3.39209,3.52962,3.88383), ("oxen",2.90525,3.82440,3.73648),
         ("cow",4.44011,4.84529,4.99550), ("cows",4.25276,4.30152,4.41124)),
    pack(("policeman",4.06178,4.44795,4.40577), ("policemen",3.62053,3.84288,3.69219),
         ("detective",4.25540,4.46122,4.43279), ("detectives",3.85830,3.65765,3.59701)),
    pack(("fireman",3.48107,4.10282,4.43763), ("firemen",3.29996,3.66679,3.77738),
         ("lifeguard",2.96525,2.28658,2.69819), ("lifeguards",2.74106,2.46267,2.37084)),
     pack(("fireman", 3.48107, 4.10282, 4.43763), ("firemen", 3.29996, 3.66679, 3.77738),
         ("gardener", 3.87872, 3.61902, 3.94050), ("gardeners", 3.74262, 3.02694, 3.18375)),
]

# precompute word sets (for no repeats)
pack_words = [{P[k][0] for k in GROUP_KEYS} for P in packs]

# helper: include man/men, exclude woman/women
def is_man_men_word(w: str) -> bool:
    return (w.endswith("man") or w.endswith("men")) and not (w.endswith("woman") or w.endswith("women"))

# mark packs that contain ANY such word
pack_has_manmen = [any(is_man_men_word(P[k][0]) for k in GROUP_KEYS) for P in packs]

# ---- exhaustive search (no repeats) ----
best = []  # (obj_main, obj_sum, gaps, means, ids)

for ids in itertools.combinations(range(len(packs)), num_stimuli):
    # EXACTLY 4 packs in the selection may contain man/men (woman/women excluded)
    if sum(pack_has_manmen[i] for i in ids) != 4:
        continue

    used = set()
    ok = True
    for i in ids:
        if used & pack_words[i]:
            ok = False
            break
        used |= pack_words[i]
    if not ok:
        continue

    obj_main, obj_sum, gaps, means = score_combo([packs[i] for i in ids])
    rec = (obj_main, obj_sum, gaps, means, ids)
    best.append(rec)
    best.sort(key=lambda x: (x[0], x[1]))
    if len(best) > num_answers:
        best.pop()

# ---- report ----
for rank, (obj_main, obj_sum, gaps, means, ids) in enumerate(best, 1):
    print(f"Rank {rank}: objective={obj_main:.6f}  sum_gaps={obj_sum:.6f}")
    show(ids, packs, gaps, means)
