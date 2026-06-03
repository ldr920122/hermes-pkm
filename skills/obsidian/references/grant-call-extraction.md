# Chinese Grant Call / Competition Notice Extraction

Recurring pattern for this user (hospital pharmacist with ML thesis).
When the user shares a URL from a Chinese pharmaceutical association or
government website, extract and cross-reference.

## Extraction pipeline

```bash
# Step 1: Fetch with proper headers (some .cn sites block curl without UA)
curl -sL 'URL' -H 'User-Agent: Mozilla/5.0' | python3 -c "
import sys, re
html = sys.stdin.read()
# Strip scripts and styles first
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
# Strip remaining HTML tags
text = re.sub(r'<[^>]+>', ' ', text)
# Collapse whitespace
text = re.sub(r'\s+', ' ', text).strip()
print(text[:10000])
"
```

## Quick extraction checklist

For each grant/competition notice, extract in order:
1. **Deadline** — always the most critical field
2. **Funding amounts** — per category (重点/面上/青年/基层)
3. **Research directions** — the numbered list of funding priorities
4. **Eligibility** —职称, 学历, 年龄 limits, membership requirements
5. **Submission process** — online vs paper, attachments needed
6. **Contact info** — for follow-up

## Cross-reference with user profile

When evaluating fit, check against the user's known profile:
- 三甲医院临床药师, 中级职称, 硕士学历
- Thesis: ML-based immune-related cardiotoxicity prediction (carrelizumab/PD-1)
- Software copyright (计算机软著) already obtained
- Interests: AI + pharmacy, prescription review, clinical prediction models
- Key match signals: "人工智能" + "药学服务" / "不良反应预测" / "精准用药" / "抗肿瘤药物"

## Common pitfalls

- **Chinese government PDFs often have image-only title pages** — body text
  may start at page 5+. Use fitz to detect: `page.get_text().strip() == ""`.
  The attachments (申报书 templates) are usually text-based.
- **Some sites serve PDF as the main content** — try the URL directly with
  fitz first; if it's HTML, use the curl pipeline above.
- **Membership gates** — 中国药学会 and similar organizations require
  personal membership. Flag this immediately if the user hasn't confirmed.
- **Overlapping deadlines** — this user typically has multiple concurrent
  applications. Always present a timeline showing all deadlines in order.
