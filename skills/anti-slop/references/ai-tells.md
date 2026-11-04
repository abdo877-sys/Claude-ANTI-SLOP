# AI tells — what makes a UI look machine-made

Run `scripts/slop_scan.py --list-rules` for the live rule catalogue. This
file explains *why* each tell happens and what to do instead.

Language models pick the most probable option for every unconstrained visual
choice. The most probable option is the average of every tutorial, template
and starter kit they were trained on. Stack enough averages and you get *the
default look*. None of these choices is wrong on its own — the problem is that
they all arrive together, and none of them was chosen *for this product*.

## The default look (use this for the divergence check)

| Axis | The default | Why it's the default |
|---|---|---|
| Accent | Indigo/violet `#6366F1`–`#8B5CF6`, or Tailwind `blue-600` | Tailwind UI, shadcn demos, Material 2 purple |
| Background | White or near-black `#0A0A0A` with zinc greys | shadcn defaults |
| Gradient | Purple → blue / pink, on hero or headline text | Stripe-era landing pages, Dribbble |
| Type | Inter (web), Roboto (Android), SF (iOS), Poppins (Flutter tutorials) — one face for everything | Framework defaults |
| Shape | `rounded-xl`/`2xl` or 16–20px on every surface | Card-based templates |
| Depth | Soft blurred shadow on every card, glassmorphism on nav | 2021–2023 trend |
| Layout | Centered hero → 3 feature cards → testimonial → CTA | Landing templates |
| Icons | Lucide/Heroicons in a tinted circle, or emoji | Copy-paste component kits |
| Motion | `ease-in-out` 300ms everywhere, bounce/pulse for attention | Defaults |
| Copy | "Elevate", "Seamless", "Supercharge", "All-in-one" | Marketing average |

**Divergence check:** after deriving an identity, count how many axes still
match this table. More than two → the identity is not yet an identity.

## Scanner rule families

The scanner groups rules into four categories, each scored separately.

### Identity (aesthetic tells)
| Rule | Severity | Why it reads as AI | Do instead |
|---|---|---|---|
| AI-HEX, GRADIENT-PURPLE | critical | The single most common output of unconstrained generation | Palette sampled from the brief's metaphor |
| GRADIENT-TEXT, GLOW | major/minor | Decoration substituting for hierarchy | Solid ink, contrast, scale |
| DEFAULT-ACCENT, SHADCN-UNTOUCHED | major | Framework defaults never re-decided | Semantic tokens from the brief |
| GLASS | major | 2021 trend, now a default | Solid surfaces; blur only over scrolling content |
| BLOB, FLOATING | major/minor | Filler for empty backgrounds | Real content, typography or a meaningful texture |
| FONT-DEFAULT | major | Inter/Poppins are the statistical font | A pairing derived from the direction |
| RADIUS-SPAM, SHADOW-SPAM | minor (bulk) | Same treatment on every surface | One shape philosophy, one depth model, by role |
| HERO-3-CARDS | major | The template section | Layout moves in `layout.md` |
| EMOJI-ICON, SPARKLE | major/minor | "I didn't design this" | One icon family, or none |
| COPY-HYPE, LOREM, UNVERIFIED-PROOF | minor/major | Interchangeable or invented content | Concrete, true, product-specific copy |
| STOCK-IMAGERY | major | Same photos as everyone else | Real assets; ask the user |
| BOUNCE | minor | Attention-seeking motion | Motion tokens |
| FL-*, SW-*, KT-* | critical/major | Mobile template defaults | Theme from the brief |

### Function (fake UI)
DEAD-LINK, NOOP-HANDLER, FORM-NO-HANDLER, CONSOLE-ONLY. A screenshot can look
finished while nothing works. These are failures, not style issues.

### Accessibility
DIV-BUTTON, IMG-NO-ALT, FOCUS-REMOVED, HTML-NO-LANG, TINY-TEXT, ZOOM-BLOCKED,
ICON-BUTTON-NO-LABEL. See `checklists/accessibility.md`.

### Performance
FONT-IMPORT-BLOCKING, IMG-NO-DIMENSIONS, TRANSITION-ALL, FIXED-WIDTH.
See `checklists/performance.md`.

## Visual tells the scanner cannot see

1. **No focal point.** Everything the same size and weight.
2. **Symmetry by default.** Every section centered.
3. **Uniform rhythm.** Same padding, same pattern, section after section.
4. **Cards inside cards.** Nested rounded containers.
5. **Icon-in-a-circle feature rows.**
6. **Fake product UI.** Dashboards and mockups with invented numbers, lorem
   charts, or perspective-tilted screenshots of nothing. Show the real product
   or nothing.
7. **Decorative clutter.** Blobs, grid floors, dot patterns, floating shapes
   that encode nothing.
8. **Nothing domain-specific on screen.** A bakery, a bank and a dev tool look
   identical. This is the most important tell.
9. **Dead states.** Grey spinner, "No data", red error box with a stack trace.
10. **Mobile as an afterthought.** Desktop layout squeezed; hamburger hiding
    the one primary action; tap targets under 44px.

## The blur test

Blur the screenshot until text is unreadable. If you can't tell what kind of
product this is — or that it's *this* product — the direction hasn't reached
the visual layer.
