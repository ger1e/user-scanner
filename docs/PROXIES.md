<!-- GER1E-DOC-SCHEMA: v1 -->
<a id="proxy-network-guide"></a>
<div align="center">

<strong>Proxy & Network Guide</strong><br/>
<sub>GER1E // USER SCANNER // DOCUMENTATION</sub>

</div>

`user-scanner` can rotate requests through a proxy list with `-P` / `--proxy-file`. The proxy manager preserves an explicit URI scheme and defaults entries without a scheme to `http://`.

<sub><strong>01 // FILE FORMAT</strong></sub>

Use one proxy per line. Blank lines and lines beginning with `#` are ignored.

```text
# Explicit schemes are preserved
http://192.0.2.10:8080
socks5://192.0.2.20:1080
socks5h://192.0.2.30:1080

# No scheme defaults to http://
192.0.2.40:3128
```

Do not commit proxy credentials, private proxy inventories, or provider access tokens to the repository.

<sub><strong>02 // USE</strong></sub>

```bash
user-scanner -u johndoe -P proxies.txt
user-scanner -e johndoe@example.com -P proxies.txt
```

Loaded proxies rotate round-robin across requests.

<sub><strong>03 // PRE-SCAN VALIDATION</strong></sub>

Add `--validate-proxies` to validate the loaded proxy set before scanning:

```bash
user-scanner -u johndoe -P proxies.txt --validate-proxies
```

Validation performs an HTTP request through each candidate proxy to `http://gstatic.com/generate_204` and retains proxies that return HTTP 200 or 204. The validation path is a reachability check, not proof that every target platform will accept the same proxy.

<sub><strong>04 // FAILURE MODES</strong></sub>

- A proxy can validate successfully and still be blocked, rate-limited, geofenced, or challenged by a target service.
- SOCKS support depends on the installed HTTP client dependencies and the scheme supplied in the proxy file.
- High concurrency can exhaust small proxy pools or trigger target-side throttling. Reduce `--concurrency` and/or add `--delay` when reliability matters more than speed.
- DNS behavior differs between proxy schemes. Use the scheme required by the proxy provider rather than silently changing it.
- Validation failures remove a proxy from the working set; they do not establish that the proxy is permanently dead.

<sub><strong>05 // OPERATIONAL SAFETY</strong></sub>

Use proxies only where you are authorized to perform the scan. Treat proxy logs and provider dashboards as potentially sensitive because they can expose targets, timestamps, and source infrastructure.

<sub>[CLI flags](FLAGS.md) · [Usage](USAGE.md) · [Cross-scan](CROSS_SCAN.md)</sub>

<p align="center"><sub>GER1E // USER SCANNER // MOBILE-SAFE DOCUMENTATION</sub></p>
