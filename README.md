<!-- GER1E-DOC-SCHEMA: v1 -->
<a id="user-scanner"></a>
<div align="center">

<strong>User Scanner</strong><br/>
<sub>GER1E // USER SCANNER // DOCUMENTATION</sub>

</div>

<p align="center">
  <img src="https://github.com/user-attachments/assets/49ec8d24-665b-4115-8525-01a8d0ca2ef4" alt="User Scanner Logo" width="100%" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.5.1-blueviolet?style=for-the-badge&logo=github" />
  <img src="https://img.shields.io/github/issues/kaifcodec/user-scanner?style=for-the-badge&logo=github" />
  <img src="https://img.shields.io/badge/Tested%20on-Termux-black?style=for-the-badge&logo=termux" />
  <img src="https://img.shields.io/badge/Tested%20on-Windows-cyan?style=for-the-badge&logo=Windows" />
  <img src="https://img.shields.io/badge/Tested%20on-Linux-black?style=for-the-badge&logo=Linux" />
  <img src="https://img.shields.io/pepy/dt/user-scanner?style=for-the-badge" />
  <a href="https://discord.gg/tVNrKVXb49" target="_blank">
     <img src="https://img.shields.io/badge/Discord-Join%20Chat-7289da?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" />
  </a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/16556" target="_blank">
    <img src="https://trendshift.io/api/badge/repositories/16556" alt="kaifcodec%2Fuser-scanner | Trendshift" width="250" height="55"/>
  </a>
</p>

---

> [!IMPORTANT]
> **Authorized defensive use only.** Use User Scanner only for identifiers you own, test fixtures, or investigations where you have explicit permission and a legitimate defensive purpose. A scanner hit is an **investigative indicator**, not proof of identity, account ownership, activity, intent, or compromise. Do not use this fork for harassment, stalking, credential testing, access-control bypass, or unauthorized account enumeration. Minimize collected personal data and follow the target platform's terms and applicable law. See [SECURITY.md](SECURITY.md) for the security and evidence boundary.

> [!NOTE]
> **GER1E hardening fork.** This repository is derived from [`kaifcodec/user-scanner`](https://github.com/kaifcodec/user-scanner) and carries GER1E-specific security, CI, network-boundary, MCP, and reporting hardening. It intentionally does not track upstream line-for-line, so upstream may have newer scan modules and release numbers. See [FORK.md](FORK.md) for the divergence policy and [SECURITY.md](SECURITY.md) for the security boundary.

A defensive **Email and Username OSINT** toolkit for scoped, evidence-aware investigations.

The upstream-derived module set exposes **455+ scan vectors** across email-integrated services and username platforms. Use them as bounded collection points, preserve provenance, corroborate consequential findings independently, and avoid treating registration indicators as identity proof.

---

<a id="sponsored-by"></a>
<sub><strong>01 // 💖 Sponsored by</strong></sub>

<p align="center">
  <a href="https://webvetted.com/user-scanner?ref=github&utm_source=github" target="_blank">
    <img width="100%" height="250" alt="WebVetted Sponsor Banner" src="https://github.com/user-attachments/assets/a18398f5-193e-4659-87d6-ccdbf6d4d4c2" />
  </a>
  <br>
  <em><strong>Defensive identity investigation.</strong> WebVetted provides OSINT enrichment, breach context, AI-assisted analysis, and an interactive identity graph for authorized investigations.</em>
  <br>
  <a href="https://webvetted.com/user-scanner?ref=github&utm_source=github" target="_blank"><strong>View WebVetted →</strong></a>
</p>

---

<p align="center">
  <a href="https://noimosiny.com/" target="_blank">
    <img width="100%" style="max-width: 100%; height: auto;" alt="banner-github" src="https://github.com/user-attachments/assets/05ca5b27-f9b4-4385-b0cf-768fbad05c39" />
  </a>
  <br>
  <em><strong>OSINT for professional investigators and analysts.</strong> Reverse email, phone number, and username research across a broad module set for authorized investigative workflows.</em>
  <br>
  <a href="https://noimosiny.com/" target="_blank"><strong>View Noimosiny →</strong></a>
</p>

---

<a id="key-features"></a>
<sub><strong>02 // ✨ Key Features</strong></sub>

- 🔎 **Scoped Email & Username OSINT:** Query supported public-facing signals across 455+ platform modules for authorized investigations.
- 👤 **Public Metadata Collection:** Collects exposed profile metadata such as avatars, bios, follower counts, public identifiers, and account attributes where modules support them.
- 🔀 **Cross-Scan & Pivot Engine:** Correlates exposed handles, profile links, and public email addresses within operator-defined scope; every pivot remains an investigative lead rather than identity proof.
- 🤖 **Model Context Protocol (MCP) Server:** Native AI integration for bounded, operator-authorized OSINT workflows with explicit inputs and reviewable results.
- 🛡️ **Optional Breach Context:** Hudson Rock integration can add infostealer exposure context where the operator is authorized and the data use is lawful.
- ⚡ **Bounded Parallel Engine:** `httpx` and `curl_cffi` support efficient module execution while the operator remains responsible for scope, rate limits, and platform terms.
- 🔀 **Permutation & Alias Generator:** Generates candidate username variations for defensive footprint review and typosquatting analysis.
- 📂 **Multi-Format Reports:** Exports to **PDF**, **JSON**, and **CSV** for evidence review and downstream analysis.
- 🌐 **Operator-Supplied Proxy Support:** Optional proxy configuration for approved network environments, with protocol detection and pre-scan validation.
- 🎨 **Responsive Terminal UI:** Dynamic progress tracking, category/module views, and clear result reporting.

---

<a id="installation"></a>
<sub><strong>03 // 🚀 Installation</strong></sub>

<a id="via-pypi-recommended"></a>
<sub><strong>04 // 🐍 Via PyPI (Recommended)</strong></sub>

```bash
# Upgrade pip and install user-scanner
python3 -m pip install --upgrade pip
pip install user-scanner

# Optional: Install with MCP Server support for AI agents
pip install "user-scanner[mcp]"
```

<a id="virtual-environment-setup"></a>
<sub><strong>05 // 📦 Virtual Environment Setup</strong></sub>

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install package
pip install user-scanner
```

<a id="via-nix-linux-macos"></a>
<sub><strong>06 // ❄️ Via Nix (Linux & macOS)</strong></sub>

```bash
# Run instantly without installing permanently
nix run github:kaifcodec/user-scanner/main -- --help

# Drop into a temporary shell with user-scanner active
nix shell github:kaifcodec/user-scanner/main
```

---

<a id="usage-guide"></a>
<sub><strong>07 // 💻 Usage Guide</strong></sub>

> [!CAUTION]
> The examples below use synthetic identifiers. Substitute a real identifier only when it is in your authorized scope. Respect platform terms, legal restrictions, data-minimization requirements, and rate limits.

<a id="1-basic-username-email-scanning"></a>
<sub><strong>08 // 1. Basic Username and Email Scanning</strong></sub>

Run a bounded scan for a single authorized username or email identifier:

```bash
user-scanner -u johndoe             # Single username scan
user-scanner -e johndoe@gmail.com   # Single email scan
```

<a id="2-cross-scan-pivot-intelligence"></a>
<sub><strong>09 // 2. Cross-Scan & Pivot Intelligence</strong></sub>

An email or username scan can return a **registration or profile indicator**; it does not prove account ownership or activity. `--cross-scan` can collect exposed handles, public profile links, and secondary public identifiers from in-scope results and use them as additional investigative leads. Review pivots before drawing identity conclusions.

| Pivot Direction | What it Collects |
| :--- | :--- |
| `-e` → **username** | Handles or social links exposed on an in-scope public profile |
| `-u` → **username** | Secondary aliases advertised on an in-scope public profile |
| `-u` → **email** | Public email addresses explicitly published on an in-scope profile |
| `-e` → **email** | Secondary public addresses exposed by an in-scope result |

```bash
user-scanner -u johndoe --cross-scan                                  # Pivot from username scan
user-scanner -e johndoe@gmail.com --cross-scan                        # Pivot from email scan
user-scanner -e johndoe@gmail.com --cross-scan --cross-links verified # Platform-verified links only
user-scanner -u johndoe --cross-scan --cross-depth 2                  # Follow approved links two hops deep
```

> 💡 *For confidence scoring, link classification rules, and cost models, see **[docs/CROSS_SCAN.md](docs/CROSS_SCAN.md)**.*

<a id="3-hudson-rock-malware-breach-intelligence"></a>
<sub><strong>10 // 3. Hudson Rock Malware Breach Intelligence</strong></sub>

Where authorized and lawful, add infostealer exposure context for an in-scope username or email identifier:

```bash
user-scanner -u johndoe --hudson
user-scanner -e johndoe@gmail.com --hudson
```

Treat any returned material as sensitive investigative context. Do not republish breach-derived personal data.

> 🖼️ *To view output terminal screenshots and visual previews, see **[docs/EXAMPLES.md](docs/EXAMPLES.md)**.*

<a id="4-targeted-category-module-scanning"></a>
<sub><strong>11 // 4. Targeted Category & Module Scanning</strong></sub>

Prefer the smallest module/category set that answers the authorized investigative question:

```bash
user-scanner -u johndoe -c dev                # Developer platforms only
user-scanner -e johndoe@gmail.com -m github   # Single module check
user-scanner -u johndoe -m github,instagram   # Explicit module set

user-scanner -lu                              # List username categories/modules
user-scanner -le                              # List email categories/modules
```

<a id="5-bulk-file-scanning"></a>
<sub><strong>12 // 5. Bulk File Scanning</strong></sub>

Bulk inputs increase privacy and rate-limit impact. Use them only when every identifier is covered by the same authorization and evidence-handling policy:

```bash
user-scanner -uf usernames.txt
user-scanner -ef emails.txt
```

<a id="6-report-exports-options-proxies"></a>
<sub><strong>13 // 6. Reports, Output and Approved Network Configuration</strong></sub>

```bash
# Export results to PDF, JSON, or CSV
user-scanner -u johndoe -f pdf -o report.pdf
user-scanner -u johndoe -f json -o results.json

# Verbose URL reporting and show all results (including not found)
user-scanner -u johndoe -v --all

# Optional proxy configuration for an approved network environment
user-scanner -u johndoe -P proxies.txt --validate-proxies
```

<a id="7-ai-llm-agent-integration-mcp-server"></a>
<sub><strong>14 // 7. AI & LLM Agent Integration (MCP Server)</strong></sub>

Connect `user-scanner` to compatible AI clients through the **Model Context Protocol (MCP)**. Agent access does not expand authorization: every identifier, module set, pivot, proxy and output remains subject to the same defensive scope and evidence rules as direct CLI use.

<a id="starting-the-server"></a>
<sub><strong>15 // Starting the Server</strong></sub>

```bash
# Start the MCP server over standard I/O (stdio)
user-scanner-mcp

# Optional: Enable verbose logging to stderr
user-scanner-mcp -v
```

<a id="mcp-client-configuration"></a>
<sub><strong>16 // MCP Client Configuration</strong></sub>

Add `user-scanner` to your client configuration (e.g. `claude_desktop_config.json` or `mcp_config.json`):

```json
{
  "mcpServers": {
    "user-scanner": {
      "command": "user-scanner-mcp"
    }
  }
}
```

<a id="exposed-ai-tools"></a>
<sub><strong>17 // Exposed AI Tools</strong></sub>

| Tool | Description | Scope rule |
| :--- | :--- | :--- |
| `scan_username` | Scoped username OSINT and public-profile enrichment | Authorized identifiers/modules only; review recursive pivots |
| `scan_email` | Scoped email OSINT and registration-signal collection | Treat results as indicators, not identity proof |
| `list_available_modules` | Dynamic module/catalog discovery | Discovery does not authorize use against a target |

---

<a id="documentation-hub"></a>
<sub><strong>18 // 📚 Documentation Hub</strong></sub>

Explore detailed documentation guides in the [`docs/`](docs/) directory:

- 📋 **[CLI Flags Reference](docs/FLAGS.md)** — Complete breakdown of every CLI flag and option.
- 🔀 **[Cross-Scan & Pivoting Guide](docs/CROSS_SCAN.md)** — Multi-pass correlation, confidence, and scope controls.
- 🔀 **[Pattern Syntax Guide](docs/PATTERNS.md)** — Wildcard and permutation patterns for candidate aliases.
- 🐍 **[Library Mode Guide](docs/USAGE.md)** — Calling the Python engine programmatically.
- 🌐 **[Proxy & Network Guide](docs/PROXIES.md)** — Proxy formats, validation, and network configuration.
- 🖼️ **[Media & Output Gallery](docs/EXAMPLES.md)** — Demonstrations and screenshots.

---

<a id="python-library-mode"></a>
<sub><strong>19 // 🐍 Python Library Mode</strong></sub>

Integrate the User Scanner engine into an authorized application workflow:

```python
import asyncio
from user_scanner.core import engine
from user_scanner.email_scan.shopping import etsy

async def main():
    # Use only an identifier covered by your authorization.
    result = await engine.check(etsy, "test@gmail.com")
    print(result.to_json())

asyncio.run(main())
```

> 💡 *For complete Python API documentation and batch category checking examples, see **[docs/USAGE.md](docs/USAGE.md)**.*

---

<a id="support-the-project"></a>
<sub><strong>20 // 💖 Support the Project</strong></sub>

Web platforms constantly update their public interfaces. Maintaining a large module set requires ongoing work to keep results useful and defensible for the cybersecurity community.

If `user-scanner` has saved time in an authorized investigation or defensive review, consider supporting the upstream project:

👉 **[Sponsor on GitHub](https://github.com/sponsors/kaifcodec)**

<a id="project-sponsors"></a>
<sub><strong>21 // Project Sponsors</strong></sub>

Huge thanks to contributors and sponsors supporting the upstream project.

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/soxoj">
        <img src="https://github.com/soxoj.png?size=100" width="50px;" alt="soxoj"/>
        <br />
        <sub><b>@soxoj</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/hienyimba">
        <img src="https://github.com/hienyimba.png?size=100" width="50px;" alt="hienyimba"/>
        <br />
        <sub><b>@hienyimba</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/InDieTasten">
        <img src="https://github.com/InDieTasten.png?size=100" width="50px;" alt="InDieTasten"/>
        <br />
        <sub><b>@InDieTasten</b></sub>
      </a>
    </td>
  </tr>
</table>

---

<a id="contributing"></a>
<sub><strong>22 // 📜 Contributing</strong></sub>

We welcome community contributions. Please read the **[Contributing Guidelines](CONTRIBUTING.md)** and **[Security Policy](SECURITY.md)** before opening a PR or submitting a new module.

---

<a id="disclaimer"></a>
<sub><strong>23 // ⚠️ Disclaimer</strong></sub>

This fork is provided for **educational use**, **authorized security research**, and **defensive OSINT investigations**. Authorization, lawful basis, scope, platform terms, rate limits, data minimization, retention, and disclosure obligations remain the operator's responsibility. Scanner output is an investigative indicator and must not be presented as proof that two identities belong to the same person or that a person performed any activity.

<p align="center"><sub>GER1E // USER SCANNER // MOBILE-SAFE DOCUMENTATION</sub></p>
