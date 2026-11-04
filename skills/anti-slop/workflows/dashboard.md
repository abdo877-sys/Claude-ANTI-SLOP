# Workflow — dashboard / admin

A dashboard answers questions. Design for the questions, not for "a grid of KPI cards".

## 1. Questions first
Ask or infer the 3–5 questions users open this dashboard to answer
("Are we on track this month?", "Which orders are stuck?"). Each question
becomes a block; the most frequent gets the dominant position.

## 2. Direction
Usually Technical, Swiss, Industrial or High-end SaaS. Identity lives in
data typography, status language and the signature move (e.g. a live
indicator whose rhythm encodes update frequency). Chrome stays quiet.

## 3. Layout
- One hero metric or chart per screen answering question #1, with comparison
  (vs last period, vs target) — a number without context is decoration.
- Secondary metrics as compact rows with sparklines, not equal cards.
- Detail tables below, filterable, sortable, exportable if users need it.
- Global time range and filters at the top, reflected in the URL.

## 4. Data integrity
- Real data from the API, or clearly labelled sample data. Never invent numbers.
- Every chart: title as a question or finding, units, time range, source/last updated.
- Loading per block (skeletons), errors per block with retry, empty per block with explanation.
- Numbers: tabular figures, consistent precision, locale formatting, abbreviations explained.

## 5. Charts
Follow `components.md` § Data visualization. Prefer the project's chart
library; otherwise a small one (e.g. Chart.js, Recharts, uPlot, Observable Plot).
Accessible: data table alternative, sufficient contrast, not color-only encoding.

## Quality checks
- [ ] Each block maps to a written user question
- [ ] No invented data; sample data labelled
- [ ] Per-block loading/error/empty states exercised
- [ ] Filters/time range persist in URL and work
- [ ] Usable at 390px (priorities reflow, tables scroll in labelled region)
