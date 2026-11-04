# Workflow — premium portfolio

The work is the hero. The site's job is to frame it and get the visitor to contact.

## 1. Evidence
- What is the discipline (motion, photo, product design, architecture, dev)?
- Who reviews it (art directors, recruiters, clients) and how fast do they scan?
- 4–8 real projects with real assets. Ask for them. Never use stock imagery.

## 2. Direction from the discipline
The medium suggests the metaphor: motion → timeline/scrubber; photography →
contact sheet/light table; architecture → plans and sections; product design →
process boards; development → working demos and source. Choose a family that
lets the work be large (Minimalist, Art-direction-driven, Editorial, Cinematic).

## 3. Structure
- Home: name + discipline + one line of positioning, then the work immediately.
  No hero portrait, no skill bars, no "Hi, I'm…" wall of text, no progress circles.
- Project pages: what the problem was, what they did, the result (real numbers
  only if real), credits. Variable layout per project is good; a single template
  for every case study is the generic tell.
- About: short, specific, with a real way to contact. Availability if relevant.
- Contact: a mailto or a working form. Nothing else required.

## 4. Craft details that matter here
- Image handling: correct aspect ratios, art-directed crops per breakpoint
  (`<picture>`), AVIF/WebP, blur-up placeholders, no layout shift.
- Video: muted, `playsinline`, poster frame, paused when offscreen, reduced-motion = poster only.
- One signature interaction (e.g. hover-preview of project, scrub navigation),
  fully keyboard accessible and with a non-hover equivalent on touch.

## Quality checks
- [ ] Work visible within the first viewport on mobile and desktop
- [ ] Every project page has real content; no lorem, no stock
- [ ] LCP image optimised; CLS < 0.1 on project pages (measure if possible)
- [ ] Signature interaction works with keyboard and touch
- [ ] Contact path works end to end
