# Grant & Competition Opportunity Matching

When a user mentions vague academic/professional goals ("课题申报 but no ideas", "need to publish"), and URLs or PDFs of funding calls or competitions arrive:

## Pattern: Cross-reference existing work against opportunities

1. **Read the call carefully** — extract: deadline, funding tracks, eligibility, funding directions (资助方向)
2. **Cross-reference with user's existing work** — thesis topic, published papers, software copyrights, clinical data access, institutional affiliation
3. **Find the intersection** — which track/direction does their existing work naturally fit?
4. **Quantify the match** — list exactly what they already have (e.g., "ML model built, 软著 obtained, 三甲医院 data") and what they still need
5. **Chain opportunities** — when multiple calls exist, show how the same core work feeds multiple submissions: "先报比赛(6/15)，再报基金(7/30)，比赛材料改一改就能投基金"

## Key indicators that this pattern applies

- User shares a `.gov.cn` or `.org.cn` URL (Chinese academic/professional notices)
- User says "课题申报" / "项目申报" / "基金" / "比赛" but has no concrete plan
- User has a thesis or ongoing research project that isn't yet leveraged for grants
- PDF attachments with names like "申报通知", "基金", "大赛通知"

## Concrete example from real session

User had thesis: ML-based prediction of immune-related cardiotoxicity from carrelizumab (anti-tumor drug). Their field: clinical pharmacy at a 三甲 hospital. Three opportunities arrived in one session:

| Opportunity | Level | Deadline | Track | Match |
|---|---|---|---|---|
| 江苏省AI+医药大赛 | 省级 | 6/15 | AI+药学服务 | thesis = individualization + TDM |
| 江苏省天晴基金 | 省级 | 7/30 | 青年/面上 | thesis = AI + drug safety |
| 中国药学会基金 | 国家级 | 7/31 | 青年/面上 | priority direction #2: \"AI+药物不良反应预测\" |

All three shared the same core material. Writing the first application produced drafts for the other two. Key tactic: **chain them** — \"先报比赛(6/15)，再报基金(7/30)，比赛材料改一改就能投基金\".

When a user's thesis topic directly matches a funding call's priority direction, flag it explicitly with \"你的论文题目，一个字都不差\" to break through the user's tendency to underestimate their own qualifications.

## Eligibility checks to run immediately

- Is CPA (中国药学会) membership required? If user isn't sure, prompt them to check.
- Age limits: 青年项目 often has ≤35 or ≤40 age caps — check against user's birth year.
- Title requirements: 面上项目 often requires 中级及以上职称.
- User's institution type: 三甲医院 qualifies for most hospital pharmacy grants.

## Pitfall

Don't just file the opportunity. The value is in **actively connecting** the user's existing work to the opportunity. A P-person (spontaneous/flexible) user may not see the connection themselves because their knowledge is in different mental compartments.
