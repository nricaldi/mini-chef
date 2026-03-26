## Problem Statement

Mini Chef users see recipe content on Instagram reels, but saving and reusing that content is unreliable and frustrating. A reel may split key details across spoken narration, on-screen text, captions, and visual context, which makes existing save workflows too manual. Users can bookmark the reel in Instagram, but that does not turn it into something they can confidently cook from later. They still need to rewatch the reel, pause repeatedly, transcribe ingredients and steps by hand, and guess at missing details.

The user needs a fast way to turn an Instagram reel into a structured recipe they can actually use. The saved result must be editable, searchable, and usable in the kitchen, even when extraction is imperfect. The product should favor speed and trust: save what is usable, make gaps visible, and let the user fix what matters without losing the original import value.

## Solution

Mini Chef v1 is an iOS app focused on Instagram reels. A signed-in user shares a reel into the Mini Chef share extension, or pastes a reel URL in-app, and Mini Chef creates an asynchronous import job. The backend fetches the reel's metadata and media, extracts evidence from audio and on-screen text, generates a structured recipe candidate, validates whether the result is usable, and saves it into the user's personal library.

If the extraction yields at least one ingredient and one step, Mini Chef saves the recipe and opens it immediately. If information is missing or confidence is imperfect, the recipe is still saved with a non-blocking `needs_review` state so the user can cook from it or edit it right away. If the reel cannot be turned into a usable recipe, the import fails clearly and does not create an empty recipe shell. Saved recipes are searchable by title and ingredient, editable through immutable backend revisions, and usable in a focused cook mode designed for hands-on kitchen use.

## User Stories

1. As a home cook, I want to share an Instagram reel directly into Mini Chef, so that I can save a recipe without copying details by hand.
2. As a home cook, I want to paste an Instagram reel URL inside the app, so that I can save recipes even if I do not start from the iOS share sheet.
3. As a signed-out user, I want Mini Chef to prompt me to sign in before import completes, so that my saved recipe is attached to my account.
4. As a returning user, I want the app to resume my pending import after Sign in with Apple succeeds, so that I do not need to restart the workflow.
5. As a user, I want Mini Chef to reject unsupported URLs clearly, so that I know why an import cannot proceed.
6. As a user, I want Mini Chef to accept Instagram reels only in v1, so that the app behavior is focused and predictable.
7. As a user, I want import progress to show simple human-readable stages, so that I know the app is still working.
8. As a user, I want the app to keep processing my import asynchronously, so that I am not blocked in the foreground.
9. As a user who leaves the app mid-import, I want a push notification when the import succeeds, so that I know my recipe is ready.
10. As a user who leaves the app mid-import, I want a push notification when the import fails, so that I know I need to retry or try a different reel.
11. As a user, I want the imported recipe to appear in my library when processing finishes, so that I can find it later even if I missed the completion screen.
12. As a user, I want Mini Chef to use spoken audio, on-screen text, and reel metadata together, so that the saved recipe is more complete than any single source alone.
13. As a user, I want the saved recipe title to reflect the dish shown in the reel, so that I can recognize it later.
14. As a user, I want ingredients to be structured into usable fields, so that the recipe is readable and searchable.
15. As a user, I want steps to be ordered and readable, so that I can actually cook from the import.
16. As a user, I want timer and temperature details captured when the reel provides them, so that I do not lose practical cooking information.
17. As a user, I do not want Mini Chef to invent quantities, times, or temperatures, so that I can trust what was extracted.
18. As a user, I want missing details to be surfaced explicitly, so that I know what to verify before cooking.
19. As a user, I want conflicting evidence to be handled conservatively, so that the app does not silently pick bad values without warning.
20. As a user, I want a recipe to save only when it is actually usable, so that my library does not fill with empty or broken imports.
21. As a user, I want a usable but incomplete recipe to save anyway, so that I can edit it instead of losing the entire import.
22. As a user, I want clearly non-recipe or unusable reels to fail instead of becoming junk recipes, so that my library stays useful.
23. As a user, I want the app to open my recipe immediately after a successful import, so that I can quickly review what was saved.
24. As a user, I want a visible but non-blocking `needs_review` banner, so that I know the recipe may need cleanup without being forced into a review flow.
25. As a user, I want recipes marked `needs_review` to remain in my library, so that I can return to them later.
26. As a user, I want to view the imported recipe title, source attribution, summary, ingredients, and instructions in one clear screen, so that I can understand what was extracted.
27. As a user, I want to edit the recipe title, so that I can fix naming mistakes or make it easier to find later.
28. As a user, I want to edit ingredients, so that I can correct missing quantities, wrong units, or formatting issues.
29. As a user, I want to edit steps, so that I can fix sequencing or make the recipe easier to follow.
30. As a user, I want each save to preserve a backend revision, so that my edits are not destructive.
31. As a user, I do not need visible revision history in v1, so that the product stays simple while still preserving safety on the backend.
32. As a user, I want `needs_review` to clear automatically once the recipe has a title, at least one ingredient, and at least one step, so that obvious fixes remove the warning state.
33. As a user, I want optional missing details to remain visible even after the recipe is usable, so that I can still decide whether to refine the recipe further.
34. As a cook, I want a prep checklist before I begin, so that I can organize ingredients before starting.
35. As a cook, I want cook mode to show one step at a time, so that I can focus without scanning a long recipe.
36. As a cook, I want a large next-step control, so that I can move through the recipe easily with messy hands.
37. As a cook, I want one-tap timers when a step already has a time value, so that I can act on extracted timing information quickly.
38. As a cook, I do not want cook mode cluttered with advanced controls in v1, so that it stays fast and dependable.
39. As a user, I want my library sorted by recency, so that newly imported recipes are easy to find.
40. As a user, I want to search by recipe title, so that I can find dishes by name.
41. As a user, I want to search by ingredient, so that I can rediscover recipes based on what I want to cook.
42. As a user, I want search results to come from the server, so that my library stays consistent across sessions and devices.
43. As a user, I do not need favorites, folders, or collections in v1, so that the app focuses on the core save-and-cook loop.
44. As a user, I want duplicate imports of the same reel to avoid unnecessary reprocessing behind the scenes, so that the system feels fast and efficient.
45. As a user, I want my own recipe copy even if another user imported the same reel before me, so that my edits remain personal.
46. As a user, I do not want another person's edits to change my saved recipe, so that my library stays under my control.
47. As a privacy-conscious user, I want account deletion to remove my personal recipes, revisions, and ingestion history, so that my data is actually erased.
48. As a user, I want explicit error outcomes for private, removed, timed-out, or otherwise failed imports, so that I understand what happened.
49. As a user, I want retries and validation recovery to happen automatically when possible, so that transient extraction issues do not require manual intervention.
50. As a user, I want the app to fail clearly when an import still cannot produce a usable recipe after retries, so that I am not misled by a bad save.
51. As a product team member, I want stage latency, retry rates, and error codes tracked, so that we can improve extraction quality and reliability.
52. As a product team member, I want to track how often saved recipes require review, so that we can understand where extraction quality is weak.
53. As a product team member, I want to measure whether users enter and complete cook mode, so that we know whether saved recipes are actually being used.
54. As a support or operations stakeholder, I want structured identifiers attached to logs and jobs, so that failed imports can be debugged quickly.

## Implementation Decisions

- v1 is limited to Instagram reels. Other platforms are out of scope and should fail with an explicit unsupported-platform outcome.
- The user entry points are the iOS share extension and in-app URL paste. Both feed the same backend ingestion flow rather than separate product paths.
- Users must be authenticated before an import can complete. Sign in with Apple is the only authentication method in v1.
- If a user starts an import from the share extension while signed out, the system should route the user through authentication and resume the pending ingest after sign-in.
- Imports are asynchronous jobs. The client submits an ingest request, receives a job identity, polls for progress while foregrounded, and relies on push notifications when backgrounded.
- User-facing progress is stage-based and simple. It should communicate meaningful progress without exposing low-level implementation details.
- The backend ingestion pipeline should encapsulate source validation, source canonicalization, metadata retrieval, media acquisition, audio transcription, OCR, recipe generation, validation, and persistence.
- The system should canonicalize Instagram source identity so duplicate imports of the same reel can reuse shared extraction artifacts where possible.
- v1 should use shared extraction artifacts behind the scenes, but each successful user import should materialize as a personal recipe copy owned by that user.
- User edits must never mutate a cross-user shared artifact. A user's saved recipe and revisions are isolated from other users' recipe copies.
- A successful import requires a usable recipe. In v1, usable means the latest candidate contains at least one ingredient and at least one step.
- Title may be generated from available evidence when needed, but the system must not fabricate unsupported cooking facts such as quantities, durations, or temperatures.
- If extraction yields a usable recipe with incomplete data, the recipe should be saved and marked `needs_review`.
- `needs_review` is non-blocking. Recipes in this state should still appear in the library, open normally, and remain available in cook mode.
- If extraction cannot produce a usable recipe after retry logic completes, the ingestion should fail and no empty recipe shell should be created.
- The system should attempt validation-aware retries before concluding failure. Retry behavior may include sending validation errors back into the extraction step and then falling back to a simpler minimum-viable prompt strategy.
- Reels that are food-adjacent, promotional, comedic, incomplete, private, deleted, or otherwise non-extractable should follow the same top-level ingestion path and fail clearly if they cannot produce a usable recipe.
- The extraction engine should combine metadata, transcript, and on-screen text with conservative evidence handling. When sources conflict, the system should prefer the more specific value and surface the conflict as missing or uncertain information rather than hide it.
- The extraction engine should return structured ingredients, structured ordered steps, recipe-level missing information, and a confidence signal suitable for product use and observability.
- User editing in v1 is limited to title, ingredients, and steps.
- Source attribution and raw extraction evidence are not user-editable in v1.
- User edits should create immutable backend revisions. The UI does not need to expose revision history in v1.
- `needs_review` should clear automatically when the latest revision has a title, at least one ingredient, and at least one step. Optional missing data may still justify informational warnings after the recipe is usable.
- Library behavior in v1 is intentionally simple: recency-ordered listing plus server-backed search on recipe title and ingredient names.
- Rich organization features such as favorites, folders, collections, and tag-based browsing are out of scope for v1.
- Cook mode in v1 includes a preparation checklist, single-step presentation, a prominent next-step control, and one-tap timers only when timing data already exists on the step.
- v1 cook mode excludes serving scaling, voice controls, step editing during cooking, advanced timer authoring, and richer kitchen-assistant features.
- Account deletion must remove user-owned recipes, user revisions, and user ingestion history in order to satisfy privacy and platform requirements.
- The implementation should be organized around deep modules with stable interfaces: ingestion orchestration, source resolution and media acquisition, recipe extraction, recipe persistence and revisioning, library and search, and notification/status delivery.
- API contracts should support idempotent ingest submission, job status retrieval, recipe retrieval, and user edit submission.
- The ingest API should support a client-supplied idempotency key so client retries do not create duplicate work.
- Concurrency and daily ingest limits should be enforced per user and remain configurable.
- Observability should include structured identifiers for request, user, job, and source, along with stage latency, retry distribution, and failures by error code.
- Metrics should support launch decisions by tracking saves per user, cook mode start and completion, `needs_review` rate, pipeline failure distribution, and the rate at which users materially edit imported recipes.

## Testing Decisions

- Good tests should validate external behavior, contracts, and user-visible outcomes rather than internal implementation details.
- Good tests should avoid coupling to prompt wording, internal sequencing within the extraction pipeline, or incidental storage details that may change without affecting product behavior.
- The highest-priority automated tests should cover ingestion orchestration, because it owns auth gating, idempotency, rate limiting, job creation, retry behavior, and success-versus-failure outcomes.
- The highest-priority automated tests should cover recipe extraction validation rules, especially the boundary between usable recipes, `needs_review` recipes, and failed ingestions.
- The highest-priority automated tests should cover recipe persistence and revisioning, including personal ownership, immutable revision creation, and automatic `needs_review` clearing after valid edits.
- The highest-priority automated tests should cover library and search behavior, including recency ordering and title-plus-ingredient search contracts.
- Notification and status delivery should receive lighter integration coverage that verifies foreground polling behavior and background completion/failure notification triggers.
- Source resolution and media acquisition should receive lighter integration coverage around URL validation, canonicalization, and major failure classes, while platform-specific implementation details remain hidden behind stable interfaces.
- Because this repo currently has no meaningful test suite or test prior art, the v1 implementation should establish its own patterns around boundary-focused unit and integration tests.
- The preferred prior art for new tests should come from adjacent backend service patterns: validate request and response contracts, persistence side effects, ownership rules, and observable job state transitions.

## Out of Scope

- Platforms other than Instagram reels
- Manual video upload
- Anonymous recipe capture or anonymous saved drafts
- Android or web client support
- Admin moderation or internal review tooling
- User-visible revision history UI
- Favorites, folders, collections, and richer library organization features
- Serving scaling, voice controls, and advanced cook-assistant interactions
- Pre-ingest non-recipe classification that blocks processing before extraction begins
- Saving failed ingests as empty or near-empty editable recipe shells
- Social features, collaboration, sharing edited recipes with other users, or public publishing
- Marketplace, monetization, subscriptions, or billing flows

## Further Notes

- The current repository reflects an early prototype of the extraction path, not the full production system described here. This PRD is intentionally forward-looking and defines the production-ready v1 target.
- The existing prototype already validates the core multimodal concept by combining reel metadata, media download, audio transcription, OCR, and LLM-based recipe generation.
- The primary product risk for v1 is not whether extraction works at all, but whether the app can save trustworthy usable recipes quickly enough that users prefer Mini Chef over simply bookmarking the original reel.
- Launch readiness should be judged by reliability of the ingest-to-save path, clarity of failure behavior, correctness of ownership and deletion semantics, and whether saved recipes actually lead to repeat cooking behavior.
