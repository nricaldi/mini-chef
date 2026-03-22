# Mini Chef MVP PRD

## 1. Product Overview
- Mini Chef helps home cooks save recipe videos from social media and convert them into usable, searchable recipes.
- MVP starts with Instagram ingestion and an iOS-first experience backed by a FastAPI API.
- Core values:
  1. Easily save a recipe from social media.
  2. Make the user want to use their saved recipes.

## 2. Problem Statement
- Users discover recipes on Instagram but lose them in DMs or saved collections.
- Saved videos are hard to use while cooking because recipe details are split across title/description, spoken audio, and on-screen text.
- Users need a fast path from "found recipe" to "ready-to-cook format".

## 3. Target User (MVP)
- Home cooks who want to save and cook recipes from social media (Instagram first).
- Primary pain points:
  - Recipes get lost in DMs and saved collections.
  - Saved recipes are not searchable by dish/ingredient.

## 4. Goals and Non-Goals
### Goals
- Convert social recipe sources into structured, editable recipes.
- Preserve source transparency and show explicit missing-information messaging.
- Provide a focused Cook Mode that makes saved recipes usable in the kitchen.

### Non-Goals (MVP)
- Meal planning.
- Grocery shopping integrations.
- Social sharing/community features.
- Full multi-platform ingestion parity (Instagram only for MVP).
- Full pantry ontology and hard canonical ingredient merge system.

## 5. MVP Scope

### 5.1 Ingestion
- Accept:
  - Instagram link.
  - iOS share extension payload (URL/text, typically not raw media).
  - Manual video upload.
- Save source metadata:
  - `source_url`, `platform`, `creator_handle` (if available), `thumbnail_url`, `raw_title`, `raw_description`, `captured_at`.
- Processing is asynchronous.

### 5.2 Extraction
- Extract and structure:
  - Dish name (lightly normalized).
  - Ingredients.
  - Ordered instructions.
- Fuse evidence from metadata, transcript, and OCR.
- Always attempt extraction when at least one evidence source exists.
- Enforce strict server-side schema validation before persistence.
- Retry extraction up to 2 times with fallback strategy.
- Persist:
  - `missing_information` entries.
  - confidence (global and optional per-field).
  - source evidence tags (`title`, `description`, `transcript`, `onscreen_text`).

### 5.3 View Recipe
- Show clear recipe details:
  - title, source, summary/description.
  - ingredient list.
  - step-by-step instructions.
- Show a non-blocking missing-information banner when applicable.

### 5.4 Cook Mode
- Preparation phase/checklist.
- Focus on one step at a time.
- Timer suggestions from parsed step text with one-tap start.

### 5.5 Editable Recipe
- Edit title, ingredients, and steps.
- Save edits as append-only recipe revisions (not destructive overwrite).

### 5.6 Recipe Library
- List saved recipes.
- Search by recipe name and ingredients.

### 5.7 Auth
- Sign in with Apple only for MVP.

### 5.8 Onboarding
- Lightweight onboarding with immediate action to ingest first recipe.

## 6. Recipe State and Review Logic
- Generated/extracted recipes are evaluated for readiness.
- `needs_review` applies when any core field is missing:
  - title, ingredients, or instructions.
- Manually added recipes do not require extraction-based review by default.
- User can override state (for example, mark as ready) from UI.
- State changes are captured in revision/audit metadata.

## 7. API Requirements (FastAPI, v1)
- Versioning: all routes under `/v1`.
- Endpoints:
  - `POST /v1/ingestions/url`
  - `POST /v1/ingestions/upload`
  - `GET /v1/jobs/{job_id}`
  - `GET /v1/recipes/{recipe_id}`
  - `POST /v1/recipes/{recipe_id}/revisions`
- `POST /v1/ingestions/url` accepts generic `source_url`; backend identifies platform.

### Async Job Status
- Status values: `queued`, `running`, `succeeded`, `failed`, `needs_review`.
- Include current stage and machine-readable error code.

### Idempotency and Dedup
- Idempotency key: per-user, per-submission request key to prevent duplicate submits.
- Dedup: canonicalized source fingerprint (for example, cleaned URL/reel id) for reuse optimization.

## 8. Data Model (MVP)
- Core entities/tables:
  - `users`
  - `sources`
  - `ingestions`
  - `jobs`
  - `job_events`
  - `recipes`
  - `recipe_revisions`
  - `ingredients`
  - `steps`

### Ingredient Strategy (MVP)
- Keep raw ingredient text.
- Derive lightweight normalized key for search and soft dedupe.
- Optional ingredient API enrichment is non-blocking and confidence-gated.

## 9. Privacy, Security, and Compliance
- Do not store raw video/audio long term.
- Keep recipe thumbnail and structured outputs as needed.
- Raw media retention uses temporary short TTL (exact duration defined during infra implementation).
- Treat source URLs and user identifiers as sensitive; strip query params when storing/logging where feasible.
- Secrets managed via environment variables (`.env` for local only).
- Enforce ownership checks by `user_id`.
- Apply per-user ingestion rate limits.

## 10. Observability and Reliability
- Structured logs include `request_id`, `user_id`, and `job_id` where relevant.
- Track:
  - stage latency.
  - queue depth.
  - failures by stage and error code.
- Error taxonomy includes examples such as:
  - `INVALID_SOURCE_URL`
  - `MEDIA_DOWNLOAD_FAILED`
  - `TRANSCRIPTION_FAILED`
  - `OCR_FAILED`
  - `SCHEMA_VALIDATION_FAILED`

## 11. Product Metrics (Friends and Family Phase)
- Keep metrics lightweight and learning-focused (no hard startup-style targets yet).
- Core metrics:
  - Successful saves per user per week.
  - Percentage of saved recipes that enter Cook Mode.
  - Extraction outcomes:
    - percentage marked `needs_review`.
    - failures by pipeline component (media download, transcription, OCR, generation/validation).

### Cooking Completion Tracking
- Track both:
  - `cook_mode_started` (entered cook mode).
  - `cook_mode_completed` (reached final step/complete action).
- This avoids relying on a single potentially gameable "cooked" flag while still capturing intent and completion behavior.

## 12. Launch Readiness (Pre-External Users)
- End-to-end flow works: ingest -> process -> recipe available.
- Retry and failure paths are surfaced clearly in the app.
- Edit and revision flow is stable.
- Auth/session ownership behavior is correct.
- Baseline metrics and logs are available for debugging.

## 13. Implementation Notes
- Existing prototype modules will be migrated behind service interfaces in the backend pipeline:
  - media download.
  - audio transcription.
  - OCR.
  - recipe generation.
- Backend orchestration moves first, then internals are improved incrementally.
