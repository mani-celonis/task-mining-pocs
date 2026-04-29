# Aha! REST API v1 — Usage Notes

Reference for correct API usage when scripting against `https://celonis.aha.io/api/v1`.  
See `celonis_aha_rules.md` for Celonis taxonomy (Features vs Epics, PrP/PuP/GA).

---

## Interpreting User Requests

**Always map user language to the correct Aha! endpoint before making API calls:**

| User says | They mean | Use endpoint |
|-----------|-----------|--------------|
| "my features" / "list features" / "GTM features" | Celonis Features (client-facing) | `GET /epics` |
| "my epics" / "list epics" / "internal epics" | Celonis Epics (internal work) | `GET /features` |

If the user says "features" without context, assume they mean **Celonis Features** (GTM) → `GET /epics`.  
If the user says "epics", assume **Celonis Epics** (internal) → `GET /features`.

---

## Authentication & Headers

- **Auth:** `Authorization: Bearer <AHA_API_KEY>`
- **Headers:** `Accept: application/json`, `Content-Type: application/json`
- **User-Agent:** e.g. `Celonis PM Automation (Agent)`

---

## Celonis Taxonomy (Critical)

Celonis uses the **opposite** of standard Aha! naming:

| Celonis Term | `reference_num` Pattern | Aha! Resource | Create Via |
|--------------|-------------------------|----------------|------------|
| **Feature** (GTM-facing) | Contains `-E-` (e.g. `AIMODULES-E-7`) | `GET /epics` | `POST /releases/{id}/epics` |
| **Epic** (internal) | No `-E-` (e.g. `AIMODULES-10`, `CELOAI-106`) | `GET /features` | `POST /releases/{id}/features` |

- **Update Celonis Features** → `PUT /epics/{reference_num}`
- **Update Celonis Epics** → `PUT /features/{reference_num}`

---

## Descriptions

When setting `description` in create/update payloads, follow Celonis standards:

| Celonis Term | Description rules |
|--------------|-------------------|
| **Feature** (GTM) | Max 2 sentences. Use a who-what-why formula (e.g. "Find what you need faster..."). Avoid internal engineering specs. |
| **Epic** (internal) | 2–3 sentences with the goal of the solution. Include links to designs or PRDs. |

Descriptions may include HTML (e.g. `<p>...</p>`, `<a href="...">...</a>`).

---

## Release Assignment

### Epics (Celonis Features — `-E-` in ref)

Use `release` as an object with `reference_num`:

```json
{
  "epic": {
    "release": {"reference_num": "AITOOLS-R-9"}
  }
}
```

### Features (Celonis Epics — no `-E-`)

Use `release` as a string (reference_num):

```json
{
  "feature": {
    "release": "AITOOLS-R-4"
  }
}
```

---

## Creating Phase-Specific Epics (PrP/PuP)

When creating a Celonis Epic (PrP/PuP phase) that belongs to a Celonis Feature (GA):

- **Endpoint:** `POST /releases/{release_id}/features`
- **Link to parent:** `epic` = parent Feature reference_num (string)
- **Assignee:** `assigned_to_user` = `{"email": "user@celonis.com"}`

Example:

```json
{
  "feature": {
    "name": "[PuP] Annotations in PIG",
    "description": "<p>Public Preview phase for Annotations in PIG. Parent: AIMODULES-E-7</p>",
    "release": "AITOOLS-R-7",
    "epic": "AIMODULES-E-7",
    "custom_fields": {"launch_type": "PuP"},
    "assigned_to_user": {"email": "f.chettouh@celonis.com"}
  }
}
```

---

## Pagination

- **Params:** `?page=1&per_page=100` (max 200 per page)
- **Response:** Check `pagination.total_pages` and loop until done.

---

## Rate Limiting

- 300 requests/minute, 20/second
- On `429 Too Many Requests`: read `Retry-After` header and sleep before retry.

---

## Custom Fields

Pass in `custom_fields` object:

```json
{
  "feature": {
    "custom_fields": {
      "launch_type": "PrP",
      "development_type": "New Feature",
      "for_external_roadmap": "Yes"
    }
  }
}
```

---

## Ideas (product Ideas portal)

List and read (for cross-reference, dedupe, and planning flows):

| Action | Endpoint |
|--------|----------|
| List | `GET /products/{product_key}/ideas` (paginate; names on list, not full categories) |
| Get one | `GET /ideas/{reference_num}` (detail includes `categories`, custom fields) |

**Create** (only in **approved** flows: e.g. after user confirmation in the [planning-to-ideas](../.cursor/skills/planning-to-ideas/SKILL.md) skill or an explicit request—never silently):

| Action | Endpoint |
|--------|----------|
| Create | `POST /products/{product_key}/ideas` |

Example body (HTML description is common in Aha!):

```json
{
  "idea": {
    "name": "Short customer-facing title",
    "description": "<p>1–3 sentences: problem, outcome, who benefits.</p>"
  }
}
```

- If the response does not attach the desired **Idea category**, use `GET /ideas/{ref}` to inspect, then `PUT /ideas/{ref}` with the fields your workspace allows (category assignment varies by account; confirm in the UI or via a test record).
- After create, the response includes `reference_num` and links for the new Idea.

---

## Writes vs read-only defaults

- **Read** operations are always safe for cross-referencing (Ideas, Features, Epics, Releases) and local docs.
- **Write** operations (POST/PUT/DELETE) are **not** allowed ad hoc. Use them only when:
  - the user has **explicitly approved** the change (e.g. intake/bulk update, planning-to-ideas create), and
  - you follow [docs/celonis_aha_rules.md](celonis_aha_rules.md) and the relevant skill (aha-bulk-update, planning-to-ideas, etc.).

---

## Ideas and Feature Suggestions

Ideas (including Feature Suggestions) are managed through Aha! Ideas portals. The `SUGGESTION` product key holds cross-product Feature Suggestions.

### List ideas for a product

`GET /products/{product_key}/ideas`

| Param | Description |
|-------|-------------|
| `workflow_status` | Filter by status name or ID (e.g. `In Review`) |
| `q` | Search term matched against idea name |
| `per_page` / `page` | Pagination (max 200 per page) |
| `tag` | Filter by tag value |
| `sort` | `recent`, `trending`, or `popular` |
| `created_since` / `created_before` / `updated_since` | UTC ISO8601 timestamps |

**Note:** There is no server-side `assigned_to` filter. To find ideas assigned to a specific user, fetch with `workflow_status` and filter client-side by `assigned_to_user.email` from the detail endpoint.

### Get idea detail

`GET /ideas/{ref}`

Returns full idea body including `assigned_to_user`, `description` (may contain HTML), `votes`, `categories`, `created_by_user`, and `workflow_status`. Categories and custom fields are **only** returned on the detail endpoint, not in list responses.

### Record links (related items)

`GET /ideas/{numeric_id}/record_links`

Returns features, epics, and other ideas linked to this idea. Requires the **numeric ID** (from the detail response's `id` field), not the reference_num.

### Internal comments

`POST /ideas/{numeric_id}/comments`

Creates an internal comment (visible to team members, not portal users).

```json
{"comment": {"body": "<p>Comment text with <strong>HTML</strong> formatting.</p>"}}
```

Requires numeric ID. Use for requesting more information from suggestion submitters.

**Idea comments** (visible on portals) use a separate endpoint: `POST /ideas/{id}/idea_comments`.

### Throttling for detail fetches

The list endpoint returns minimal fields. When fetching detail or record links per idea, throttle at ~15 requests per batch with `time.sleep(1.1)` between batches to stay within rate limits.

---

## Endpoint Summary

| Action | Epics (Celonis Features) | Features (Celonis Epics) |
|--------|--------------------------|--------------------------|
| List | `GET /epics` | `GET /features` |
| Get one | `GET /epics/{ref}` | `GET /features/{ref}` |
| Create | `POST /releases/{id}/epics` | `POST /releases/{id}/features` |
| Update | `PUT /epics/{ref}` | `PUT /features/{ref}` |
| Delete | `DELETE /epics/{ref}` | `DELETE /features/{ref}` |

| Action | Ideas / Suggestions (product Ideas portal) |
|--------|--------------------------------------------|
| List | `GET /products/{product_key}/ideas` |
| Get one | `GET /ideas/{ref}` |
| Create | `POST /products/{product_key}/ideas` |
| Update | `PUT /ideas/{ref}` |
| Delete | `DELETE /ideas/{ref}` |
| Record links | `GET /ideas/{numeric_id}/record_links` |
| Internal comment | `POST /ideas/{numeric_id}/comments` |
| Portal comment | `POST /ideas/{numeric_id}/idea_comments` |
