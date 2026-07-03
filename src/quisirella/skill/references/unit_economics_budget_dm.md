# Unit Economics & Budget — DM-first (Quisirella)

Chuoi gia tri tu Meta den chot don that. Nguon: claude-ads `ads-math` + `ads-budget`, loc purchase ROAS.

---

## Chuoi metric (bat buoc)

```
chi phi/tin nhan → engaged_rate → quality_mess (manual) → chi phi/khach chot → LTV proxy
```

| Metric | Cong thuc | Nguon |
|---|---|---|
| Chi phi/tin nhan | spend / messaging_started_7d | API |
| engaged_rate | depth_3 / messaging_started | API |
| Reply rate | first_reply / messaging_started | API |
| Ty le tin nhan/link | messaging_started / link_click | API |
| Chi phi/mess chat | spend / quality_mess_count | `08-dm-quality-log.md` |
| Chi phi/khach chot | spend / orders_closed | `08-dm-quality-log.md` |
| LTV proxy | AOV don chot (manual) | `08-dm-quality-log.md` |

**LTV:CAC (DM):** `LTV_proxy / chi_phi_khach_chot` — healthy ≥3:1 cho luxury repeat referral; <1:1 = mat tien.

Purchase/ROAS Meta: chi ghi chu diagnostic — khong dung cho quyet dinh scale/pause.

---

## Break-even (tham khao)

```
Break-even chi phi/tin nhan ≈ (AOV × close_rate_tu_mess × gross_margin) / 1 mess
```

Neu khong co close_rate — dung chi phi/mess chat tu sổ 08 khi co du lieu.

---

## 70 / 20 / 10 (budget theo vai tro)

Ap dung cho 3 campaign sunset (xem `campaign_strategy.yaml`):

| Bucket | % ngan sach | Campaign / muc dich |
|---|---|---|
| 70% | Proven DM funnel | Phieu Tin nhan khi dat KPI |
| 20% | Scale / test | Tang Phieu, test creative moi |
| 10% | Experiment | Concept moi, placement test |

**Sunset Profile:** khi Phieu Tin nhan <25k/mess + ≥5 mess chat/ngay × 3 ngay → chuyen ~70k/ngay sang Phieu.

---

## 3x Kill Rule

| Dieu kien | Data toi thieu | Hanh dong |
|---|---|---|
| Chi phi/tin nhan >3× muc tieu campaign | ≥7 ngay, ≥20 tin nhan hoac ≥500k spend | Flag pause / reduce |
| Khong co tin nhan | ≥500k spend hoac ≥50 link_click | Pause + chan doan CTA/placement |
| CTR <50% benchmark account | ≥1.000 impressions | Kill creative, test moi |
| engaged_rate <10% lien tuc | ≥14 ngay | Review chat script / targeting |

**Accept:** da toi uu 3 lan (creative, CTA, placement) ma van fail → pause, khong tweak vo han.

---

## 20% Scaling Rule

Khong tang budget >20% mot lan:
- Ngay 1: 100k → 120k
- Cho 3-5 ngay on dinh chi phi/tin nhan + engaged_rate
- Ngay tiep: 120k → 144k

**San sang scale khi:**
- Chi phi/tin nhan duoi muc tieu ≥2 tuan
- Learning phase da qua
- Khong co fatigue (CTR khong giam >20%/14 ngay)
- engaged_rate on dinh hoac tang

---

## Budget sufficiency (Meta IG)

- Budget/ad set ≥ **5×** chi phi/tin nhan muc tieu (learning)
- Retarget: theo doi frequency <3.5/tuan
- Khong scale campaign sai `funnel_role` (Profile vi mess re)

---

## MER (blended — khi co doanh thu that)

```
MER = Tong doanh thu (08 + Sheets) / Tong chi tieu marketing
```

Chi dung khi co so don chot that — khong dung purchase Meta.

---

## Output goi y trong phan tich

- Bang unit economics theo campaign
- Scale list / Kill list
- Measurement plan cho moi hanh dong budget (ngay doc lai, metric)
