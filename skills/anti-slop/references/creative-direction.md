# Creative direction engine

The chain is fixed: **evidence → DNA → tensions → direction family → metaphor →
system → signature move → refusals.** Every link must be written down in the
brief. If you can't trace a pixel back up the chain, it doesn't belong.

## 1. Evidence

Collect before deciding anything:

| Source | What to extract |
|---|---|
| Repo (README, routes, models, copy, i18n) | What the product *is about* (its core object), locales/scripts, features that matter |
| User answers (≤3 questions) | Audience, the one action that matters, constraints |
| Existing brand assets | Logo geometry, colors, fonts that must survive |
| Content | Real photos, real data, real case studies — content is the strongest identity source |
| Business objective | Convert, retain, impress, inform, sell, recruit |

## 2. DNA — one paragraph

*"<Product> helps <audience> <do X> so they <outcome>. They arrive feeling
<state>, on <device/context>. They trust <source of trust>. The core object
on screen is <object>."*

## 3. Tension pairs

Place the product on the three axes that matter most, with a reason:

precise ↔ warm · still ↔ kinetic · crafted ↔ technical · spacious ↔ dense ·
quiet ↔ loud · institutional ↔ intimate · accessible ↔ rare ·
serious ↔ playful · timeless ↔ of-the-moment

Example: *"80% dense — analysts compare 40 rows at once; 70% quiet — the data
is the hero; 60% technical — users write SQL."*

## 4. Direction family — chosen by evidence, never by taste

Use this table to find candidates. A family is justified only if **at least two
pieces of evidence** from steps 1–3 point to it. Note the failure mode: it's
what that family looks like when applied generically — avoid it.

| Family | Evidence that justifies it | Evidence against | Core moves | Generic failure mode |
|---|---|---|---|---|
| **Editorial** | Content-led, long reads, authorship, journalism, publishing, thought leadership | Task-heavy apps | Strong serif/grotesk contrast, measure 60–75ch, columns, pull quotes, captions, rules | Random serif + huge whitespace with nothing to read |
| **Swiss International** | Information clarity, institutions, transport, civic, documentation | Emotional consumer brands | Strict grid, flush-left grotesk, scale contrast, objective imagery, minimal color | Helvetica + red square, no grid discipline |
| **Brutalist** | Artists, raw/honest positioning, counter-culture, dev tools that celebrate rawness | Trust-critical (finance, health) | Exposed structure, system fonts, default-ish controls, hard edges, honest HTML | Ugly for its own sake, unreadable |
| **Neo-brutalist** | Young, playful-but-direct products, creator tools, indie SaaS | Luxury, institutional | Thick ink borders, hard offset shadows, flat saturated fills, chunky type | Every element with a 4px border and yellow fill |
| **Minimalist** | Few features, one action, premium utility, the product itself is the visual | Rich content, many features | Very few elements, precise spacing, one accent, typography carries everything | Empty and bland; minimal content, not minimal design |
| **Luxury** | High price, scarcity, craftsmanship, fashion, hospitality, jewelry | Mass market, utilities | High-contrast serif, generous space, restrained palette, slow motion, real photography | Gold gradient + script font |
| **Experimental** | Art, music, events, studios that sell creativity itself | Anything users must operate quickly | Unconventional navigation, type as image, generative/interactive pieces — with a usable fallback | Disorienting with no payoff; broken mobile |
| **Futuristic** | Hardware, space, AI research, mobility, deep tech | Heritage, warmth-led | Precise mono/grotesk, technical diagrams, measured motion, dark surfaces with one signal color | Neon on black + glow + grid floor |
| **Industrial** | Manufacturing, logistics, infra, tools, B2B ops | Soft consumer | Labels, stencils, data plates, safety colors used semantically, rugged grids | Caution stripes as decoration |
| **Organic** | Food, wellness, farming, craft, sustainability, local | Fintech, dev tools | Natural palette sampled from materials, softer shapes, real textures, humanist type | Beige + leaves + blob shapes |
| **Playful** | Kids, games, casual consumer, community | Serious B2B, health, legal | Rounded/quirky type, bright but limited palette, characterful micro-interactions | Emoji, confetti, bounce everywhere |
| **Cinematic** | Film, launches, storytelling brands, immersive campaigns | Frequent-use tools | Full-bleed media, sequencing, dramatic type scale, scroll as narrative, sound off by default | Autoplay video background with a centered tagline |
| **Architectural** | Architecture, interiors, real estate, design studios | Dense apps | Plans, sections, axonometrics, precise thin rules, large imagery, measured grids | Grey photos with thin type and no hierarchy |
| **Technical** | Developer tools, APIs, data products, scientific | Lifestyle | Mono for code/data, docs-quality hierarchy, real code samples, diagrams, keyboard-first | Fake terminal with fake output |
| **Retro-futuristic** | Products with nostalgia in their DNA, music/hardware, games | Neutral professional | Era-specific type, period color, CRT/print artifacts used sparingly | Synthwave sunset |
| **Art-direction-driven** | Brands with strong existing photography/illustration | No assets available | The art leads; UI recedes; layout built around specific images | Stock photos with a filter |
| **High-end SaaS** | B2B product where clarity and trust convert | Indie/creative audiences | Real product UI, precise type, one accent, honest proof, focused copy | Indigo gradient + 3 cards (the default itself) |
| **Immersive storytelling** | Reports, campaigns, journalism, nonprofits, product narratives | Utilities | Scrollytelling with meaning, data revealed in steps, chapters, progress | Parallax for its own sake |

Blending: a direction may borrow **one** move from a second family if the
evidence supports it ("Swiss grid + one editorial serif for headlines").

## 5. Material metaphor

*"If this product were a physical object in its users' world, what would it be
made of?"* — ledger paper, enamel signage, rack labels, illuminated
manuscript, ticket stub, transit map, field notebook, apothecary label, market
stall sign, specimen card… The metaphor turns the family into concrete
choices: it supplies the palette (sample real materials), the texture, the
shape language and the motion personality (paper settles, stamps land,
terminals cut, fabric drapes).

## 6. Signature move

One recurring, product-specific detail used in 3–5 deliberate places. It must
be meaningful (reflects what the product does), cheap (CSS or one component),
and restrained. Examples: a double rule under totals (ledger); a station-dot
progress line (transit); a blinking LED on live counters (infra); a perforated
divider (tickets); a single geometric star as divider/loader/empty-state art.

## 7. Refusals

Write 3–6 things this design will deliberately **not** do, specific to the
product. Example: *"No product screenshots in perspective. No testimonial
carousel. No dark mode for the marketing site (the brand is paper). No icons in
feature lists."* Refusals prevent drift more than rules do.

## 8. Checks before you build

1. **Default-look check:** compare with the table in `ai-tells.md`. ≤2 axes
   may match the default.
2. **Sibling test:** would another product in a different domain get the same
   brief from this process? If yes, you used trend, not evidence — redo step 4/5.
3. **Blur test (after build):** blur a screenshot until text is unreadable.
   Can you still tell what kind of product this is?
4. **Reason test:** pick any 5 random decisions; each must have a one-line
   reason that names the product or its users.

## Worked examples (short)

**Accounting app for small Djiboutian shops (FR/AR).** DNA: shop owners track
credit given to regulars; trust is personal. Tensions: 70% warm, 60% dense,
65% accessible. Family: Swiss International (clarity) + one Organic move
(warmth). Metaphor: the carbon-copy receipt book. Palette from receipt paper,
carbon blue ink, rubber-stamp red for overdue. Type: IBM Plex Sans + IBM Plex
Sans Arabic, tabular figures. Signature move: duplicate-copy offset (a faint
second line) under each total. Refusals: no gradients, no illustrations of
people, no dark marketing hero.

**Portfolio of a motion designer.** Evidence: the work *is* motion; audience
is art directors scanning fast. Family: Cinematic + Minimalist restraint.
Metaphor: an editing timeline. Signature move: a scrub bar that doubles as
navigation between projects. Refusals: no about-me hero portrait, no skill
bars, no case-study template sections.

**Open-source database CLI docs.** Evidence: users live in terminals, copy
commands, scan reference. Family: Technical. Metaphor: a well-kept man page.
Signature move: every command has a real, copyable, tested example with output.
Refusals: no fake terminal animation, no illustration, no marketing hero on docs pages.
