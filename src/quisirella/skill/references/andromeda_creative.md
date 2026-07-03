# Andromeda + Creative Diversity — Instagram (Quisirella)

Ap dung cho placement **`instagram_feed`**, **`instagram_reels`**, **`instagram_stories`** only. KPI chinh van la **chi phi/tin nhan** — creative la don bay retrieval, khong thay the funnel DM.

Nguon: claude-ads `ads-meta` + `meta-audit.md`, loc bo pixel/CAPI focus.

---

## Stack Meta 2026 (tom tat)

| Thanh phan | Vai tro |
|---|---|
| **Andromeda** (10/2025) | Retrieval ranking — loc hang trieu ad xuong ~1.000 candidate truoc auction |
| **GEM** | Creative content embed vao khong gian targeting — "creative is the new targeting" |
| **Lattice** | Sequence-aware optimizer tren GEM |

**Hau qua:** Creative diversity la don bay #1. Similarity >60% → retrieval suppression. 100 bien the nho ≈ 10 concept that su khac biet.

---

## Rubric Creative-as-Targeting (0-10)

Moi truc 0-2 diem; tong 0-10:

| Truc | 0 (Risk) | 1 (OK) | 2 (Strong) |
|---|---|---|---|
| Concept diversity | 1 message/xu huong cho tat ca asset | 2 goc (trust vs style) | 3+ goc (macro, timeless, qua tang inclusive) |
| Format diversity | Chi static | 2 format (static + video) | 3+ (static, video, carousel) |
| Visual diversity | 1 bo anh/composition | 2 treatment | 3+ (macro, on-model, flat lay) |
| Hook diversity (video) | Hook giong nhau ≤3s | 2 hook pattern | 3+ (cau hoi, claim, POV, demo) |
| Headline diversity | Paraphrase cung 1 dong | 2 cau truc | 3+ (so, cau hoi, claim, comparison) |

| Tong | Risk |
|---|---|
| 8-10 | LOW Entity-ID clustering |
| 4-7 | MEDIUM — co the bi suppression |
| 0-3 | HIGH — mat retrieval ticket |

---

## Entity-ID Clustering Predictor (pre-launch)

Truoc khi chay creative moi, doi tung cap asset:

1. **Visual fingerprint** — cung macro/backdrop/model → likely cluster
2. **Headline fingerprint** — 4 token dau giong nhau → likely cluster
3. **Body/CTA fingerprint** — cung mo dau + cung CTA verb → likely cluster
4. **Video hook** — 0-3s giong nhau → likely cluster du phan sau khac
5. **Format mismatch wins** — static + video + visual khac → khong cluster

**Output goi y:** nhom cluster du doan, giu 1/cum, cat hoac rebuild phan con lai. Muc tieu ≥8/10 truoc scale spend.

---

## Creative fatigue (IG)

| Tin hieu | Nguong | Hanh dong |
|---|---|---|
| CTR (all) giam | >20% trong 14 ngay | Refresh concept (khong chi doi mau) |
| Frequency prospecting (7d) | >3.0 warn, >5.0 fail | Creative moi hoac audience |
| Frequency retargeting (7d) | >8.0 warn, >12.0 fail | Creative moi |
| Khong co creative moi | >21 ngay (Andromeda era) | Test concept moi |

Tuoi tho creative Andromeda: **2-4 tuan** (khong con 6-8 tuan nhu truoc).

**Quisirella:** frequency >2.5/30 ngay → red flag trong KPI rule.

---

## Volume & format (IG-only)

- ≥3 format active (image, video, carousel) — uu tien Reels/Stories vertical 9:16
- ≥5 creative/ad set (standard); test them neu spend cao
- Headline ads: <40 ky tu; primary text: <125 ky tu (khi viet copy ads)
- UGC/testimonial: huu ich cho luxury pre-owned neu authentic — khong gia VO

---

## Lien ket Quisirella

- Copy ads: `output/00-ig-ad-creative-guide.md` + `00-meta-ad-policy-ig.md`
- Copy organic: `copy_frameworks_ig.md` + `quisirella-ig-organic-copy.mdc`
- Competitive visual: `competitor_meta_ig.md` + `00-competitive-ig-used-luxury.md`
- **Khong** dung EMQ/CAPI/purchase lam tieu chi creative success
