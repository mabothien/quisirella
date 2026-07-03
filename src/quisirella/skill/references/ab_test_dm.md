# A/B Test Design — DM-first (Quisirella)

Moi khuyen nghi toi uu phai co the chuyen thanh gia thuyet test. Nguon: claude-ads `ads-test`, metric = **tin nhan** / **chi phi/tin nhan**.

---

## Khung gia thuyet (bat buoc)

```
IF chung ta [thay doi]
THEN [metric] se [tang/giam] khoang [X%]
BECAUSE [ly do tu data hoac insight Meta/Quisirella]
```

**Vi du:**
```
IF thay static macro bang video Reels 9:16 (hook macro 2s)
THEN chi phi/tin nhan giam 15-25%
BECAUSE Andromeda uu tien format diversity; account hien chi co static, CTR Reels thuong cao hon Feed cho luxury visual
```

### Chat luong gia thuyet

- [ ] 1 bien duy nhat (concept, hook, placement, audience — khong tron)
- [ ] Metric cu the: chi phi/tin nhan, engaged_rate, ty le tin nhan/link
- [ ] Effect size uoc luong (cho duration)
- [ ] Tieu chi thanh/bai truoc khi chay

---

## Thu tu uu tien test (DM funnel)

| Uu tien | Bien test | Ly do |
|---|---|---|
| 1 | Creative concept (khong chi doi mau) | Tac dong Andromeda + CTR |
| 2 | Hook video 0-3s / opening static | Anh huong dung lai |
| 3 | CTA (Send message vs link-first) | Anh huong ty le tin nhan/link |
| 4 | Placement (Reels vs Feed vs Stories) | Chi `instagram_*` |
| 5 | Audience (LAL vs interest vs broad) | Sau khi creative on |
| 6 | Copy nho (tu thay the) | Tac dong thap |

---

## Sample size & duration (volume nho)

Quisirella thuong <500 clicks/ngay — dung **pragmatic test**, khong can hang tram nghin conversions.

| Baseline | Cach uoc luong duration |
|---|---|
| chi phi/tin nhan on dinh 7-14 ngay | So sanh 2 variant sau 7 ngay toi thieu |
| <20 tin nhan/variant/tuan | Keo dai 14-21 ngay hoac tang budget test |
| Learning phase active | Khong ket luan — doi ~50 events |

**Minimum:** 7 ngay (bat tuan) · **Maximum khuyen nghi:** 21 ngay (tranh mua vu)

---

## Meta Experiments (IG)

- Dung **Ads Manager → Experiments** (khong duplicate ad set thu cong)
- Split audience tu dong — tranh overlap
- Budget: chia deu; ≥100 USD/ngay/variant neu co the (adapt VND tuong duong)
- Primary metric: **Cost per messaging conversation started** hoac chi phi/tin nhan tinh tay
- Secondary: engaged_rate, CTR (all) tren `instagram_*`

---

## Output mau

```markdown
## A/B Test Plan — [ten test]

### Gia thuyet
IF ...
THEN ...
BECAUSE ...

### Thiet ke
| Tham so | Gia tri |
|---|---|
| Campaign | [ten] |
| Bien | [creative / placement / ...] |
| Control | [hien tai] |
| Variant | [de xuat] |
| Metric chinh | chi phi/tin nhan |
| Split | 50/50 |

### Duration
- Toi thieu: 7 ngay
- Do luong: so sanh chi phi/tin nhan + engaged_rate cuoi ky

### Tieu chi thanh cong
- chi phi/tin nhan giam ≥X% voi engaged_rate khong giam >Y%
- Khong tang FB spend share

### Measurement plan (GROW)
- Ngay [X]: doc ket qua, ghi vao 07-session-log
- Neu variant thang: scale theo 20% rule (`unit_economics_budget_dm.md`)
```

---

## Loi thuong gap

- Test nhieu bien cung luc
- Ket thuc som (<7 ngay)
- Dung purchase/ROAS lam metric chinh
- Ket luan trong learning phase
- Pause segment breakdown chi vi CPA trung binh cao (Breakdown Effect)
