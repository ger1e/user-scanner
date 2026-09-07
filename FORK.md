# GER1E fork status

`ger1e/user-scanner` is a security-hardening fork of [`kaifcodec/user-scanner`](https://github.com/kaifcodec/user-scanner).

The upstream project remains the authoritative source for upstream releases, scan-module counts, sponsors, package publishing, and general feature development. This fork carries GER1E-specific changes around CI, network and request boundaries, MCP exposure, reporting, and defensive hardening. It intentionally does not track upstream line-for-line, so upstream may have newer features or more scan vectors at any given time.

When evaluating this repository, distinguish three things:

- **Upstream functionality:** inherited from `kaifcodec/user-scanner`.
- **GER1E hardening:** commits unique to this fork.
- **Upstream drift:** changes present upstream but not yet reviewed or adopted here.

Upstream changes should be reviewed before being merged into this fork rather than synchronized blindly, especially where they alter outbound requests, parsing, proxy behavior, file/media handling, MCP tools, or report generation.

Current upstream: https://github.com/kaifcodec/user-scanner

Current fork: https://github.com/ger1e/user-scanner
