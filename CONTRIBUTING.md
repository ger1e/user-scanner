<!-- GER1E-DOC-SCHEMA: v1 -->
<a id="contributing-to-user-scanner"></a>
<div align="center">

<strong>Contributing to user-scanner</strong><br/>
<sub>GER1E // USER SCANNER // DOCUMENTATION</sub>

</div>

---

This project separates two kinds of checks:

- Username availability checks (under `user_scanner/user_scan/*`) — synchronous validators that the main username scanner uses.
- Email OSINT checks (under `user_scanner/email_scan/`) — asynchronous, multi-step flows that probe signup pages or email-focused APIs. Put email-focused modules in `user_scanner/email_scan/` (subfolders like `social/`, `dev/`, `community`, `creator` etc. are fine — follow the existing tree).

---

<a id="module-naming-for-both-emailscan-and-userscan-modules"></a>
<sub><strong>01 // Module naming for both `email_scan` and `user_scan` modules</strong></sub>

- File name must be the platform name in lowercase (no spaces or special characters).
  - Examples: `github.py`, `reddit.py`, `x.py`, `pinterest.py`

---

<a id="email-scan-emailscan-guide-for-contributors"></a>
<sub><strong>02 // Email-scan (email_scan) — guide for contributors</strong></sub>

Minimal best-practices checklist for email modules

- [ ] Put file in `user_scanner/email_scan/<category>/service.py`.
- [ ] Export `async def validate_<service>(email: str) -> Result`.
- [ ] Use `httpx.AsyncClient` for requests, with sensible timeouts and follow_redirects when needed.
- [ ] Add a short docstring describing environment variables (api keys), rate limits, and responsible-use note (if required)

<a id="example-mastodon-async-example"></a>
<sub><strong>03 // Example: Mastodon async example:</strong></sub>

```python name=user_scanner/email_scan/social/mastodon.py
import httpx
import re
from user_scanner.core.result import Result


async def _check(email: str) -> Result:
    """
    Internal helper that performs the multi-step signup probe.

    This function demonstrates how to handle CSRF tokens, custom error
    messages (like IP bans), and passing the target URL back to Results.
    """
    # The display URL used for output and error reporting
    show_url = "https://mastodon.social"

    signup_url = f"{show_url}/auth/sign_up"
    post_url = f"{show_url}/auth"

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "referer": f"{show_url}/explore",
        "origin": show_url,
    }

    async with httpx.AsyncClient(http2=True, headers=headers, follow_redirects=True) as client:
        try:
            # 1. Access the signup page to retrieve required CSRF tokens
            initial_resp = await client.get(signup_url, timeout=15.0)
            if initial_resp.status_code not in [200, 302]:
                return Result.error(f"Failed to access signup page: {initial_resp.status_code}", url=show_url)

            # Extract the CSRF/authenticity token from the HTML
            token_match = re.search(r'name="csrf-token" content="([^"]+)"', initial_resp.text)
            if not token_match:
                return Result.error("Could not find authenticity token", url=show_url)

            csrf_token = token_match.group(1)

            # 2. Prepare the probe payload with the email we want to check
            payload = {
                "authenticity_token": csrf_token,
                "user[account_attributes][username]": "no3motions_robot_020102",
                "user[email]": email,
                "user[password]": "Theleftalone@me",
                "user[password_confirmation]": "Theleftalone@me",
                "user[agreement]": "1",
                "button": ""
            }

            response = await client.post(post_url, data=payload, timeout=15.0)
            res_text = response.text
            res_status = response.status_code

            # 3. Analyze the response to determine account status
            if "has already been taken" in res_text:
                return Result.taken(url=show_url)

            elif "registration attempt has been blocked" in res_text:
                return Result.error("Your IP has been flagged by Mastodon", url=show_url)

            elif res_status == 429:
                return Result.error("Rate limited; try using the '-d' flag", url=show_url)

            elif res_status in [200, 302]:
                # If no 'taken' message is found and status is OK/Redirect, it's available
                return Result.available(url=show_url)

            else:
                return Result.error("Unexpected response body", url=show_url)

        except Exception as exc:
            # Always pass the url=show_url even in exceptions for clear reporting
            return Result.error(str(exc), url=show_url)


async def validate_mastodon(email: str) -> Result:
    """
    Public validator used by the email mode.

    All email modules must export a 'validate_<name>' function that
    returns a Result object.
    """
    return await _check(email)


```

---

<a id="username-availability-check-guide"></a>
<sub><strong>04 // Username availability check guide:</strong></sub>

<a id="validator-function-userscan"></a>
<sub><strong>05 // Validator function (user_scan/)</strong></sub>

Each module must expose exactly one validator function named:

```python
def validate_<sitename>(user: str) -> Result:
    ...
```

**CRITICAL Rules for `user_scan` Modules:**

1. **Explicit Verification (No False Positives):** Never rely solely on a generic HTTP 200 to assume availability. Many WAFs and CDNs intercept requests and return 200 OK. You MUST explicitly verify a unique string or JSON key for BOTH the `taken` and `available` states. **Never use a bare `else: return Result.available()` block.**
2. **Deep Data Extraction:** If the user is found, attempt to extract rich metadata (fullname, location, bio, stats) and return it via `Result.taken(extra={"fullname": "John Doe", ...})`. **If extracting profile pictures, banners, or other images, you MUST pass their URLs in the `media` dictionary** (e.g., `Result.taken(media={"avatar": "https://..."})`), not in `extra`.
3. **Strict Error Handling:** NEVER use `raise Exception()`. All unhandled states or unexpected status codes must return `Result.error(f"Unexpected status code {resp.status_code}")`.
4. **Use Orchestrator Helpers:** Use `generic_validate` to standardize `httpx` logic, but write robust `process` callbacks.
5. **Use Next.js Helpers:** When a site is based on Next.js, use the matching helper from `user_scanner.core.nextjs`: `parse_next_pages_data` for Pages Router `__NEXT_DATA__`, `iter_next_app_flight_chunks` for App Router Flight data, or `parse_next_pages_redirect` for Pages Router JSON redirects. Do not duplicate this parsing in a module.

---

<a id="orchestrator-helpers-userscan"></a>
<sub><strong>06 // Orchestrator helpers (user_scan)</strong></sub>

To keep validators DRY, the repository provides helper functions in `core/orchestrator.py`.

<a id="1-genericvalidate-preferred"></a>
<sub><strong>07 // 1. generic_validate (Preferred)</strong></sub>

- **Purpose:** Run a request for a given URL and let a callback (`process`) inspect the `httpx.Response` and return a `Result`.
- **Use case:** Highly recommended for all modern modules to inspect response content, prevent false positives, and parse out deep data.

<a id="example-robust-module-with-deep-data-extraction"></a>
<sub><strong>08 // Example robust module with deep data extraction:</strong></sub>

```python
from user_scanner.core.orchestrator import generic_validate
from user_scanner.core.result import Result
import re
import json

def validate_example(user: str) -> Result:
    url = f"https://www.example.com/{user}/profile"
    show_url = "https://www.example.com"
    headers = {"User-Agent": "Mozilla/5.0"}

    def process(response):
        # 1. Explicitly check for the "not found" state
        if response.status_code == 404 or "User does not exist" in response.text:
            return Result.available()
            
        # 2. Explicitly verify the "taken" state and extract deep data
        if response.status_code == 200 and "profile-data" in response.text:
            extra = {}
            match = re.search(r'<script id="profile-data">({.+?})</script>', response.text)
            if match:
                data = json.loads(match.group(1))
                if "name" in data:
                    extra["fullname"] = data["name"]
                if "location" in data:
                    extra["location"] = data["location"]
            return Result.taken(extra=extra)

        # 3. Graceful error handling for unexpected states (No bare else!)
        return Result.error(f"Unexpected response status: {response.status_code}")

    return generic_validate(url, process, headers=headers, show_url=show_url, follow_redirects=True)
```

<a id="2-impersonatevalidate"></a>
<sub><strong>09 // 2. impersonate_validate</strong></sub>

- **Purpose:** Run a request through a cookie-persistent `curl_cffi` session that impersonates a browser TLS fingerprint. Use it for services protected by strict anti-bot walls such as DataDome or Cloudflare, which may reject standard Python HTTP clients even when their headers look like a browser's.
- **When to use:** Prefer `generic_validate` for ordinary endpoints. Choose `impersonate_validate` when the site is known to inspect the TLS fingerprint or requires browser-like session cookies.
- **Key parameters:**
  - `warmup_url` optionally fetches a page once per session before the main request so the session can obtain clearance cookies.
  - `impersonate` selects the browser profile and defaults to `"chrome"`.
  - `show_url` controls the URL attached to the returned `Result`; it defaults to the request URL.
  - `allow_redirects` defaults to `False`, unlike httpx's `follow_redirects=True` in the `generic_validate` example. Pass `allow_redirects=True` when the profile URL redirects. Additional keyword arguments are forwarded to `impersonate_request`.

```python
from user_scanner.core.impersonate import impersonate_validate
from user_scanner.core.result import Result


def validate_example(user: str) -> Result:
    url = f"https://www.example.com/profile/{user}"

    def process(response):
        if response.status_code == 404 and "User does not exist" in response.text:
            return Result.available()
        if response.status_code == 200 and f'profile/{user}' in response.text:
            return Result.taken()
        return Result.error(f"Unexpected response status: {response.status_code}")

    return impersonate_validate(
        url,
        process,
        warmup_url="https://www.example.com/",
        impersonate="chrome",
        show_url=url,
    )
```

For multi-step flows, use `impersonate_request` directly. It returns the raw `curl_cffi` response and reuses the same browser-like session, cookies, proxy, and optional warm-up as `impersonate_validate`.

<a id="3-statusvalidate-discouraged"></a>
<sub><strong>10 // 3. status_validate (Discouraged)</strong></sub>

- **Purpose:** Simple helper for sites where availability can be determined purely from HTTP status codes (e.g., 404 = available, 200 = taken).
- **Warning:** Use this *only* as a last resort if the site has absolutely no WAF and reliably returns strict HTTP codes without custom redirect/error pages. Modern sites heavily punish this approach.

<a id="4-url-construction-and-user-input"></a>
<sub><strong>11 // 4. URL construction and user input</strong></sub>

Never interpolate user-controlled input (`user`, `email`, `target`, etc.) directly
into a URL string:

```python
# ❌ Don't do this — special characters (&, #, %, +, whitespace, non-ASCII)
# can corrupt the request or inject unintended query parameters
url = f"https://example.com/api/users?username={user}"
```

Instead, build the URL without the value and pass it via `params`. This is
supported by `generic_validate`, `make_request`, `status_validate`, and
`impersonate_request`, and encodes correctly regardless of what the input
contains:

```python
# ✅ Do this
url = "https://example.com/api/users"
return generic_validate(url, process, show_url=show_url, params={"username": user})
```

If a module needs a separate human-facing URL (e.g. to show the profile link
in results), keep that as its own `show_url` built with an f-string — it's
just for display and isn't sent as a request, so interpolation there is fine:

```python
url = "https://example.com/api/users"
show_url = f"https://example.com/{user}"  # display only, not a request
return generic_validate(url, process, show_url=show_url, params={"username": user})
```

---

<a id="return-values-and-error-handling"></a>
<sub><strong>12 // Return values and error handling</strong></sub>

- Always return a Result object:
  - `Result.available()`
  - `Result.taken(extra={"fullname": "..."}, media={"avatar": "..."})`
  - `Result.error("short diagnostic message")`
- The orchestrator captures network errors (`httpx.ConnectError`, `httpx.TimeoutException`, etc.) and returns `Result.error(...)` automatically.
- **NEVER** use `raise Exception("...")`. If you encounter an anomaly in your `process` function, always return `Result.error("...")` so the scanner can gracefully continue to the next module.

---

<a id="style-linting"></a>
<sub><strong>13 // Style & linting</strong></sub>

- Follow PEP8.
- Use type hints for validator signatures.
- Keep code readable and small.
- Add docstrings to explain non-obvious heuristics.
- Run linters and formatters before opening a PR (pre-commit is recommended).
- If you contribute with an AI coding agent, the
  [ponytail](https://github.com/DietrichGebert/ponytail) skill pairs well
  with this project's philosophy of small, self-contained modules.

---

Thank you for contributing!

<p align="center"><sub>GER1E // USER SCANNER // MOBILE-SAFE DOCUMENTATION</sub></p>
