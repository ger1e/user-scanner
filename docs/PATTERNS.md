<!-- GER1E-DOC-SCHEMA: v1 -->
<a id="pattern-syntax-guide"></a>
<div align="center">

<strong>Pattern Syntax Guide</strong><br/>
<sub>GER1E // USER SCANNER // DOCUMENTATION</sub>

</div>

The pattern system allows you to generate multiple username or email variations from a single compact pattern definition. This is useful for searching variations of a username/email similar to your desire.

<a id="quick-start"></a>
<sub><strong>01 // Quick Start</strong></sub>

Use patterns directly with the `-u` (username) or `-e` (email) flags:

```bash
# Scan "johna", "johnb", "johnc"
user-scanner -u "john[a-c]"

# Scan up to 50 permutations instead of default 100
user-scanner -u "john[0-9]{0-2}" -s 50

# Scan multiple variations with case differences
user-scanner -u "[jJ]ohn[0-9]{1-2}"

# With emails
user-scanner -e "user[a-z]{0-1}@example.com"
```

The `-s` flag (short for `--stop`) limits how many permutations are scanned. By default, only the first 100 are checked.

<a id="pattern-syntax"></a>
<sub><strong>02 // Pattern Syntax</strong></sub>

<a id="character-sets-chars"></a>
<sub><strong>03 // Character Sets: `[chars]`</strong></sub>

Define a character set using square brackets. Characters between the brackets will each become a separate variation.

**Examples:**

```
john[abc]         → "johna", "johnb", "johnc"
user[0-9]         → "user0", "user1", ..., "user9"
test[a-zA-Z]      → "testa", "testb", ..., "testZ"
site[_.-]         → "site_", "site.", "site-"
```

**Character Range Syntax:**

- `[a-z]` - lowercase letters a through z
- `[A-Z]` - uppercase letters A through Z
- `[0-9]` - digits 0 through 9
- `[a-zA-Z0-9]` - combined ranges
- `[abc]` - literal characters a, b, c

**Note**: "-" must be placed at the beginning or at the end of the range to be interpreted as a character.

<a id="length-control-charslen"></a>
<sub><strong>04 // Length Control: `[chars]{len}`</strong></sub>

Specify the length of expansions from a character set.

**Examples:**

```
john[a-z]{0-2}    → "john", "johna", "johnb", ..., "johnz", "johnaa", ..., "johnzz"
code[0-9]{2}      → "code00", "code01", ..., "code99"
user[a-c]{1;3}    → "usera", "userb", "userc", "useraaa", ..., "userccc"
text[0-1]{1-3}    → "text0", "text1", "text00", "text01", "text10", "text11", ..., "text111"
```

**Length Syntax:**

- `{n}` - exactly n characters
- `{n-m}` - between n and m characters (inclusive)
- `{n;m}` - exactly n or m characters
- `{0-n}` - zero to n characters

<a id="common-use-cases"></a>
<sub><strong>05 // Common Use Cases</strong></sub>

<a id="username-variations-with-numbers"></a>
<sub><strong>06 // Username Variations with Numbers</strong></sub>

```bash
user-scanner -u "john[0-9]{0-3}"
```

Scans up to 100 variations: `john`, `john0`–`john9`, `john00`–`john99`, `john000`–`john999`

<a id="multiple-name-parts-with-case-variations"></a>
<sub><strong>07 // Multiple Name Parts with Case Variations</strong></sub>

```bash
user-scanner -u "[jJ]ohn[0-9]{0-2}"
```

Scans variations like: `john`, `John`, `john0`–`john99`, `John0`–`John99`

<a id="underscore-and-dot-variations"></a>
<sub><strong>08 // Underscore and Dot Variations</strong></sub>

```bash
user-scanner -u "user[_.]name"
```

Scans: `user_name`, `user.name`

<a id="email-with-variations"></a>
<sub><strong>09 // Email with Variations</strong></sub>

```bash
user-scanner -e "user[a-z]{0-1}@example.com"
```

Scans email addresses: `user@example.com`, `usera@example.com`–`userz@example.com`

<a id="limiting-scan-results"></a>
<sub><strong>10 // Limiting Scan Results</strong></sub>

Use the `-s` or `--stop` flag to limit how many permutations are checked:

```bash
# Check only 10 permutations instead of default 100
user-scanner -u "john[0-9]{0-3}" -s 10
```

The tool will show you how many permutations are available:

```
[+] Scanning 10 of 1111 permutations
```

<a id="viewing-available-permutations"></a>
<sub><strong>11 // Viewing Available Permutations</strong></sub>

The tool automatically shows how many variations were found and scans up to the limit you set.

<a id="performance-tips"></a>
<sub><strong>12 // Performance Tips</strong></sub>

1. **Start with limits** - Always use `-s` to limit how many permutations you scan:

   ```bash
   user-scanner -u "pattern[0-9]{0-3}" -s 25
   ```

2. **Check pattern complexity** - A pattern like `[a-z]{5}` would generate 11,881,376 combinations. Start small and increase gradually.

3. **Use moderate ranges** - Keep character sets and length ranges reasonable:
   - Good: `[a-c]{0-2}` (~15 variations)
   - Risky: `[a-z]{0-3}` (~18,278 variations)

4. **Combine with other filters** - Use `-c` (category) or `-m` (module) to narrow the scope:

   ```bash
   user-scanner -u "user[a-z]{0-1}" -c social -s 50
   ```

5. **Add delays between requests** - Use the `--delay` flag to avoid rate limiting:
   ```bash
   user-scanner -u "test[0-9]{1-2}" --delay 1.0
   ```

<a id="cli-examples"></a>
<sub><strong>13 // CLI Examples</strong></sub>

<a id="simple-usernames-with-numbers"></a>
<sub><strong>14 // Simple usernames with numbers</strong></sub>

```bash
user-scanner -u "johnny[0-9]{0-2}"
```

<a id="case-variations"></a>
<sub><strong>15 // Case variations</strong></sub>

```bash
user-scanner -u "[jJ]ohn[0-9]{1-2}"
```

<a id="multiple-separators"></a>
<sub><strong>16 // Multiple separators</strong></sub>

```bash
user-scanner -u "john[._-]doe"
```

<a id="complex-pattern-with-limited-scans"></a>
<sub><strong>17 // Complex pattern with limited scans</strong></sub>

```bash
user-scanner -u "user[a-z]{0-1}[0-9]{0-2}" -s 50
```

<a id="email-pattern-variations"></a>
<sub><strong>18 // Email pattern variations</strong></sub>

```bash
user-scanner -e "[jJ]ohn[_.]doe@example.com"
```

<a id="combining-with-other-flags"></a>
<sub><strong>19 // Combining with other flags</strong></sub>

```bash
# Scan a pattern with verbose output and delay between requests
user-scanner -u "admin[0-9]{1-2}" -v --delay 0.5 -s 25

# Scan with a specific category
user-scanner -u "user[a-c]" -c social -s 50
```

<a id="pattern-limitations"></a>
<sub><strong>20 // Pattern Limitations</strong></sub>

- Do not nest brackets: `[[a-z]]` is invalid
- Ranges must go from lower to higher ASCII values (e.g., `[z-a]` is invalid)
- The pattern engine is designed for generating variations, not complex regex-like patterns

<p align="center"><sub>GER1E // USER SCANNER // MOBILE-SAFE DOCUMENTATION</sub></p>
