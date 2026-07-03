# 10-Principle Thinking Framework — Quisirella (DM-first)

Mindset gate truoc moi phan tich, bao cao, hoac viet copy. Khong phai checklist — hoi: *minh dang bo qua nguyen tac nao?*

Nguon: claude-ads `thinking-framework.md`, adapt cho Meta IG + chot DM Quisirella.

---

## 1. OBSERVE — Ngoai canh (du lieu that)

**Trong cong viec Meta DM:**
- Lay insights/breakdown tu MCP hoac `data/meta_fetch/` truoc khi ket luan.
- Chi phan tich placement `instagram_*` — khong dung Facebook row lam creative benchmark.
- Doc `output/08-dm-quality-log.md` neu can mess chat / don chot.

**Anti-pattern:** Chan doan tu benchmark e-commerce hoac nho so cu ma khong mo account.

---

## 2. OBSERVE — Noi tam (tu soi bias)

**Trong cong viec Meta DM:**
- Co dang ap heuristic ROAS/purchase len shop chot DM?
- Co dang penalize Phieu Profile vi chi phi/tin nhan cao? (sai `funnel_role`)
- Co dang khuyen pause segment chi vi CPA/tin-nhan trung binh cao trong breakdown? (vi pham Breakdown Effect)

**Anti-pattern:** Tu tin khuyen "pause Reels" ma khong xem time-series marginal.

---

## 3. LISTEN — Lang nghe muc tieu that

**Trong cong viec Meta DM:**
- Doc `campaign_strategy.yaml` — muc tieu tung campaign (top_only vs top_middle vs bottom).
- Lang nghe user: "mess chat" vs "visit profile" la hai KPI khac nhau.
- Khong dich "hieu qua" thanh purchase pixel neu business chot DM.

---

## 4. THINK — Xu ly logic (first principles)

**Trong cong viec Meta DM:**
- Tinh tay: chi phi/tin nhan, engaged_rate, ty le tin nhan/link.
- Xay funnel: impression → click → tin nhan → first_reply → depth_3 → chot (manual).
- Kiem tra learning phase (~50 events/7 ngay) truoc verdict scale/pause.

Chi tiet: `unit_economics_budget_dm.md`, `health_score_dm.md`.

---

## 5. CONNECT — Lien tuong (insight cheo)

**Trong cong viec Meta DM:**
- Andromeda + creative diversity + fatigue = cung he thong retrieval — xem `andromeda_creative.md`.
- Chi phi/tin nhan re + depth_3 thap = volume nhung chat kem — khong scale ngay.
- Placement IG tot + copy khong hop policy = creative issue, khong phai audience.

---

## 6. CONNECT — He thong (orchestration)

**Trong cong viec Meta DM:**
- Pipeline: fetcher → analyst (bang so verbatim) → writer (quality gate).
- Khuyen nghi khong mau thuan: "tang budget 30%" va "pause campaign" cung luc ma khong giai thich trade-off.
- Sunset Profile ↔ scale Phieu Tin nhan la mot he thong budget — xem `campaign_strategy.yaml`.

---

## 7. FEEL — Cam xuc & giong brand

**Trong cong viec Meta DM:**
- Copy ads/organic: than thien, chuyen nghiep, khong phien dien — xem `copy_frameworks_ig.md`.
- Creative luxury: trust/macro truoc gia — khong FOMO toxic.
- Scoring 100% spec ma khong co cam xuc = fail cho used luxury.

---

## 8. ACCEPT — Khiem ton (bo sunk cost)

**Trong cong viec Meta DM:**
- **3x Kill Rule:** chi phi/tin nhan >3x muc tieu + da toi uu 3 lan → chap nhan pause.
- Sunset Profile khi dieu kien du — khong giu vi "da ton budget".
- Khuyen nghi truoc do khong hieu qua sau measurement window → bo, khong double down.

Chi tiet: `unit_economics_budget_dm.md`.

---

## 9. CREATE — Ship deliverable

**Trong cong viec Meta DM:**
- Bao cao phai co verdict + hanh dong cu the + owner (test/placement/creative).
- Khuyen nghi = gia thuyet test duoc — xem `ab_test_dm.md`.
- Writer khong ship report fail quality gate.

---

## 10. GROW — Vong lap do luong

**Trong cong viec Meta DM:**
- Moi khuyen nghi kem **measurement plan** (metric, thoi gian, nguong thanh cong).
- Tai audit 30/90 ngay — so sanh voi baseline trong `06`.
- Cap nhat `08-dm-quality-log.md` khi co so mess chat / don chot moi.

---

## Workflow map (Quisirella)

| Buoc | Nguyen tac chinh |
|---|---|
| Bat dau phien / fetch | OBSERVE (ngoai), LISTEN |
| Phan tich campaign | THINK, OBSERVE (noi) |
| Breakdown placement | THINK + Breakdown Effect |
| Creative / copy | FEEL, CONNECT (lateral) |
| Verdict scale/pause | ACCEPT, THINK |
| Ghi bao cao | CREATE |
| Sau deliverable | GROW (measurement plan) |
