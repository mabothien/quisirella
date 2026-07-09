---
title: Quisirella — Session checkpoints (user-triggered)
generated_at: 2026-07-06
purpose: episodic_memory
language: vi
---

# 09 — Session checkpoints

**Chỉ ghi khi user nói "lưu phiên"** (intent `save_session`). Không auto-checkpoint ở `sessionEnd`.

Chat mới: hook `sessionStart` inject **checkpoint mới nhất** từ file này. Spec: `.cursor/rules/quisirella-session-memory.mdc`.

## Template (agent copy khi lưu)

```markdown
## Checkpoint YYYY-MM-DD HH:MM +07

- **User focus:** (1 dòng — từ user nếu có, vd. "lưu phiên — sunset 1806")
- **Decisions:** (verbatim, có số)
- **Key metrics:** (cite data/ hoặc output/ — không từ user paste)
- **Open items:** (việc còn dở)
- **Files touched:** (paths output/ hoặc data/)
- **Intent summary:** (intent đã chạy trong phiên)
```

<!-- Checkpoints appended below by agent on save_session -->

## Checkpoint 2026-07-06 17:34 +07

- **User focus:** Creative phễu (Andromeda), ad Tiffany T carousel, test-prompts, fetch creative Meta, vận hành 2 ad / 1 ad set phễu
- **Decisions:**
  - phễu tin nhắn: **2 ad song song** (「Nỗi sợ」+ 「Nỗi sợ 2」/ Tiffany T) — cùng objective mess, **khác concept + SKU**; đo **7 ngày**, KPI chính **chi phí/tin nhắn &lt; 25k**, không tối ưu theo CTR đơn thuần
  - 「Nỗi sợ」: **1 ảnh** hoặc concept giáo dục — **không** tối ưu 3 ảnh 3 SKU trong 1 ad; giữ nếu KPI tốt
  - 「Nỗi sợ 2」: **carousel 3 slide** 1 SKU — Tiffany T True narrow vàng hồng **size 51.5**; hook giáo dục 3 ❌ + vuốt ảnh (cận → form → khắc lòng trong); CTA macro + size + giữ mẫu; **pause ngay khi hết hàng** dù KPI đẹp
  - **Bán - Bản sao** (retarget): **không** duplicate creative phễu / Nỗi sợ 2 — giữ logic bottom; chỉ đổi card khi hết hàng hoặc frequency cao
  - Hết hàng 1-of-1 → **pause ad** (bắt buộc), duplicate ad mới cho SKU khác
  - Ảnh mạng / stock on-hand → **không** dùng trong ad
- **Key metrics:** (cite `output/06-active-campaigns-analysis.md`, kỳ 01–06/07) phễu window **22.652 VND**/mess · Retarget window **9.303 VND**/mess · account 62 mess / 1.399.459 spend; creative live 「Nỗi sợ」= static image + `INSTAGRAM_MESSAGE` (`data/meta_fetch/active/120253285175280110_creatives.json`)
- **Open items:**
  - Theo dõi 2 ad phễu **7 ngày** (chi phí/tin nhắn, mess chất manual, % spend từng ad)
  - Rà 「Nỗi sợ」còn **3 ảnh mixed SKU** trong Ads Manager → cân nhắc rút 1 ảnh
  - Pause 「Nỗi sợ 2」khi nhẫn T 51.5 bán hết
  - Sunset 1806 theo strategy (phễu &lt;25k + mess chất ≥5/ngày × 3 ngày)
  - `test-prompts` full suite ~22 phút CPU — dùng `--tier` / `--id` khi cần nhanh
- **Files touched:** `output/09-session-checkpoints.md`; `data/meta_fetch/active/120253285175280110_ads.json`, `120253285175280110_creatives.json`; `config/intent_router.yaml`, `config/rag_synonyms.yaml`, `config/rag_prompt_tests.yaml`; `src/quisirella/retrieval/prompt_tests.py`, `src/quisirella/main.py`; `README.md`
- **Intent summary:** `ads_analysis` · `meta_lookup`/creative fetch · `save_session` · RAG `test-prompts` (16→19 pass sau tune intent/synonyms)

## Checkpoint 2026-07-09 09:07 +07

- **User focus:** Copy + launch「Nỗi sợ 2」phễu (Tiffany bạc chục triệu, 1 ảnh); chẩn đoán starvation「Nỗi sợ」sau khi thêm ad mới; merge fetch script phễu
- **Decisions:**
  - **Copy「Nỗi sợ 2」chốt publish** (~9/10): hook *Tiffany bạc chục triệu* + 3 bullet (*hoá đơn / ảnh shop khớp / app check auth*) + bridge *đắt nhất là chọn người bán uy tín* + CTA *Nhắn tin Quisirella — xem macro trước khi chốt* + guarantee *Hàng không đúng ảnh, hoàn 100% trong 24h* (cam kết thật — chi tiết bổ sung trong DM)
  - Format **1 ảnh** + file phương tiện Advantage+ — **không** ghi “vuốt” trong copy; macro gửi qua DM
  - Tách entity khỏi「Nỗi sợ」: hook/bullet/ảnh khác; tránh copy generic *Mua Tiffany Bvlgari sợ nhất…*
  - Cùng ad set CBO: nếu「Nỗi sợ 2」&gt;60% spend × 3 ngày + CPA &gt;75k → cân nhắc **ad set spend limit** (vd. Nỗi sợ min ~100k, test max ~40–50k/ngày) hoặc tách ad set
  - **Không pause「Nỗi sợ」** vì starvation ngày đầu — period vẫn &lt;25k/tin; đợi review **13/07/2026** (test 7 ngày)
  - Hết hàng 1-of-1 → **pause ad** ngay
  - Fetch CLI: `scripts/_fetch_pheu_ads.py` (0 arg=MTD, 1 date, 2 dates=range); xóa `_fetch_pheu_day.py`
  - User **đã tạo xong** chiến dịch/quảng cáo「Nỗi sợ 2」09/07
- **Key metrics:** (cite `output/06-active-campaigns-analysis.md` §7.1.1, refresh **08/07**) phễu `120253285175280110` period 01–07/07 —「Nỗi sợ」785.708 VND / 40 mess = **19.643**/tin ·「Nỗi sợ 2」(ad cũ T carousel) 197.439 / 1 mess = **197.439**/tin; ngày **07/07**「Nỗi sợ」376 VND (**0,3%** spend) vs「Nỗi sợ 2」122.697 (**99,7%**); ngày **08/07**「Nỗi sợ」0 spend ·「Nỗi sợ 2」66.485 / **2 mess** = **33.242**/tin (`ad_insights_2026-07-08.json`); verdict **YELLOW** — interim review **10/07**
- **Open items:**
  - Fetch + đọc **09/07** (và tiếp) — % spend, CPA từng ad sau launch copy mới
  - Theo dõi RED trigger: starvation「Nỗi sợ」kéo dài +「Nỗi sợ 2」CPA &gt;75k
  - Review đủ **7 ngày** → **13/07/2026**
  - DM sẵn: macro + giá + hoàn 100% trong 24h
  - Cập nhật `06` §7.1.1 khi có fetch mới (ad ID / creative「Nỗi sợ 2」mới nếu khác T carousel)
- **Files touched:** `output/09-session-checkpoints.md`; `output/06-active-campaigns-analysis.md`; `scripts/_fetch_pheu_ads.py`; `scripts/_fetch_pheu_day.py` (deleted); `data/meta_fetch/active/120253285175280110_*`
- **Intent summary:** `ads_analysis` · copy review (ig-ad-creative) · `save_session` · phễu ad-level diagnosis
