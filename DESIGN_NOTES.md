# A personal node in the Wired

## Direction

The landing page introduces Richard before asking visitors to inspect his work. It contains a personal introduction, background, interests, and three short project previews. Full implementation details live in dedicated case studies reached through the project directory.

The visual direction draws on overhead power lines, muted analog imagery, isolation, and terminal typography associated with Serial Experiments Lain. The image is confined to an artwork panel so the text remains readable. Dark mode uses near-black and dusty rose; light mode uses warm paper and burgundy. No flashing effects, autoplay sound, or continuous animations are used.

References consulted:

- [WIRED: Wired at Heart](https://www.wired.com/2000/05/wired-at-heart/) — contemporary discussion of the show's visual contrasts, hardware imagery, and transformer hum.
- [Lain wiki: Typographics](https://lain.wiki/wiki/Typographics) — interface and text imagery from the series.
- [IBM Design Language: Typeface](https://www.ibm.com/design/language/typography/typeface/) — the Plex family and its open-source availability.
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) — reduced-motion behavior, checked via Context7.

Typography uses IBM Plex Sans for readable prose and IBM Plex Mono for navigation, labels, code, and small interface elements. Richard's name uses a local Georgia serif for a more personal, editorial contrast. No claim is made that these reproduce the anime's original title font.

## Original generated artwork

Saved asset: `site/assets/wired-sky.png` (1536 × 1024 PNG). Generated with the built-in imagegen tool and copied into the project. No anime frame or third-party wallpaper is embedded.

Final generation prompt:

> Use case: stylized-concept. Asset type: atmospheric editorial illustration for a personal computer science/game developer portfolio inspired by Serial Experiments Lain and the Wired. Create an original scene, no characters or logos. Wide landscape 3:2 composition: a solitary Japanese utility pole slightly right of center with transformers and many fine black overhead cables stretching diagonally across a vast pale gray overcast sky. Low-angle view. Distant rooftop silhouettes only at the bottom edge. Late-1990s psychological anime background mood, analog photocopy grain, charcoal linework, desaturated warm gray paper, subtle dusty burgundy shadows. Spare, eerie, quiet, beautifully composed, lots of negative sky space, crisp fine wires. Not neon cyberpunk, no city billboards, no text, no watermarks, no readable signage. Keep grain subtle and poles detailed. This is a standalone artwork panel, not a UI mockup.

The source PNG remains in Codex's generated-images directory as well. The site references only the copy in its own assets directory. The slight dark-mode brightness adjustment and responsive crop are CSS presentation; the stored image is unchanged.

## Expansion model

`content/profile.json` owns identity/contact text. `content/projects.json` registers projects. `content/pages/` owns authored HTML content. `templates/layout.html` owns all shared chrome. The standard-library Python generator renders portable static pages and fails on invalid project configuration. Additions require content changes, not a new framework or new runtime dependency.
