#!/usr/bin/env python3
"""
PreToolUse scope enforcement hook for the bug bounty harness.

Reads the Claude Code PreToolUse hook JSON on stdin, extracts every hostname the
tool call would contact, and hard-blocks the call if any host is not covered by
the campaign allowlist.

A prompt can only ask an agent to stay in scope. This can actually stop it.

WHAT IS COVERED
    - WebFetch                     (the `url` field)
    - Bash                         (URLs, bare hosts passed to known network CLIs,
                                    and hosts inside target-list files such as
                                    `-l targets.txt` / `-dL scope.txt` / `-iL hosts`)
    - any `mcp__*` tool            (deep extraction over the tool input, because an
                                    MCP server such as Burp can send arbitrary
                                    requests and would otherwise bypass scope
                                    entirely -- see `docs/02-mcp-servers.md`)
    - WebSearch is deliberately NOT enforced: a search does not contact the target.

Exit codes (Claude Code hook contract):
    0  allow  (prints nothing, or a JSON advisory)
    2  BLOCK  (blocking error; the tool call does not run)

Allowlist file (default ``scope/allowlist.txt``, override with BB_ALLOWLIST):

    # comments and blank lines ignored
    example.com                 -> exact host only
    *.example.com               -> any subdomain, at any depth, plus example.com
    !blog.example.com           -> explicit deny; overrides any wildcard match
    @mcp-local semgrep          -> this MCP server never touches the target, so
                                   skip host checks for its calls. Use ONLY for
                                   servers you know run locally (semgrep over
                                   stdio, a filesystem server). Never for Burp,
                                   a recon wrapper, or anything that fetches.

Environment:
    BB_ALLOWLIST     path to the allowlist (default <project>/scope/allowlist.txt)
    BB_BLOCK_LOCAL=1 also block localhost/loopback/RFC1918 (default: allowed, so
                     local proxies and collaborator listeners keep working)
    BB_MCP_STRICT=1  for mcp__* tools, scan EVERY string in the tool input for
                     bare hostnames, not just host-ish fields and URLs. Fewer
                     bypasses, more false positives on tools that legitimately
                     carry hostnames in data (e.g. a code-analysis server).
    BB_FAIL_OPEN=1   debugging only. Allow when parsing fails, instead of blocking.
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
import sys
from urllib.parse import urlparse

# Fail CLOSED: if we cannot parse the request, block it rather than let an
# unknown host through. Set BB_FAIL_OPEN=1 only while debugging.
FAIL_OPEN = os.environ.get("BB_FAIL_OPEN") == "1"
BLOCK_LOCAL = os.environ.get("BB_BLOCK_LOCAL") == "1"
MCP_STRICT = os.environ.get("BB_MCP_STRICT") == "1"

# Built-in tools that can reach the network. Any `mcp__*` tool is also treated as
# network-capable unless the allowlist marks its server `@mcp-local`.
NETWORK_TOOLS = {"WebFetch", "Bash"}
# A web search does not contact the target, so there is nothing to enforce.
IGNORED_TOOLS = {"WebSearch"}

LOCAL_HOSTNAMES = {"localhost", "127.0.0.1", "::1", "0.0.0.0", "burp", "collaborator"}

# Keys whose values are host-ish in essentially every tool schema.
# Note the leading `:` alternative -- HTTP/2 pseudo-headers (`:authority`) carry the
# target host, and Burp's MCP send_http2_request passes them as a dict. Without it,
# an HTTP/2 request to an out-of-scope host slips past. Caught by the test suite.
_HOST_KEY_RE = re.compile(
    r"(?:^|_|:)(?:host|hostname|target|targets|domain|domains|url|urls|uri|endpoint|"
    r"origin|authority|server|site|address|base_?url|request_?url)s?$",
    re.I,
)
# Keys whose values are a raw HTTP request/response we should parse a Host header from.
_RAW_HTTP_KEY_RE = re.compile(r"(?:^|_)(?:request|raw|message|http|body|content)s?$", re.I)

_URL_RE = re.compile(r"\bhttps?://([^\s/'\"|;<>)\\\]}]+)", re.I)
_HOST_HEADER_RE = re.compile(r"^\s*Host\s*:\s*([^\r\n\s]+)", re.I | re.M)

# bare host[:port] appearing as an argument to a known network CLI
_NET_CLI_RE = re.compile(
    r"\b(?:curl|wget|httpx|nuclei|ffuf|feroxbuster|gobuster|dirsearch|nmap|masscan|"
    r"subfinder|amass|dnsx|katana|hakrawler|whatweb|nikto|sqlmap|wpscan|testssl|"
    r"openssl\s+s_client|nc|ncat|netcat|dig|host|nslookup)\b([^\n;|&]*)",
    re.I,
)
_BARE_HOST_RE = re.compile(
    r"(?<![\w.\-/@:])((?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?\.)+[a-z]{2,})(?![\w\-])", re.I
)
# Flags whose argument is a file listing targets, one per line.
_TARGET_FILE_RE = re.compile(
    r"(?:^|\s)(?:-l|-dL|-iL|-L|--list|--target-file|--targets|--hosts|--urls)"
    r"[=\s]+([^\s;|&'\"]+)",
    re.I,
)

# Extensions that are filenames, not hostnames.
_FILE_EXTS = {
    "txt", "json", "md", "sh", "py", "js", "yaml", "yml", "csv", "log", "conf",
    "xml", "html", "zip", "gz", "jsonl", "ini", "toml", "lst", "out", "tmp",
}

MAX_SCAN_BYTES = 2_000_000  # cap deep-scan work on pathological inputs


def log(msg: str) -> None:
    sys.stderr.write(f"[scope-guard] {msg}\n")


def load_allowlist(path: str) -> tuple[list[str], list[str], set[str]]:
    """Return (allow_patterns, deny_patterns, mcp_local_servers)."""
    allow: list[str] = []
    deny: list[str] = []
    mcp_local: set[str] = set()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.split("#", 1)[0].strip()
                if not line:
                    continue
                low = line.lower()
                if low.startswith("@mcp-local"):
                    parts = line.split(None, 1)
                    if len(parts) == 2:
                        mcp_local.add(parts[1].strip().lower())
                    continue
                if low.startswith("@"):
                    continue  # unknown directive: ignore rather than treat as a host
                if low.startswith("!"):
                    deny.append(low[1:].strip())
                else:
                    allow.append(low)
    except FileNotFoundError:
        return ([], [], set())
    return (allow, deny, mcp_local)


def host_matches(host: str, pattern: str) -> bool:
    host = host.lower().rstrip(".")
    pattern = pattern.lower().rstrip(".")
    if pattern.startswith("*."):
        base = pattern[2:]
        # '*.example.com' covers example.com and any depth of subdomain
        return host == base or host.endswith("." + base)
    return host == pattern


def is_local(host: str) -> bool:
    if host in LOCAL_HOSTNAMES or host.endswith(".local") or host.endswith(".internal"):
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return ip.is_loopback or ip.is_private or ip.is_link_local


def _looks_like_filename(candidate: str) -> bool:
    return candidate.rsplit(".", 1)[-1].lower() in _FILE_EXTS


def _norm_host(value: str) -> str | None:
    """Pull a bare hostname out of a URL-ish or host:port-ish string."""
    value = value.strip().strip("'\"")
    if not value:
        return None
    try:
        parsed = urlparse(value if "://" in value else "//" + value)
        host = parsed.hostname
    except ValueError:
        return None
    if not host:
        return None
    host = host.lower().rstrip(".")
    if not host or _looks_like_filename(host):
        return None
    return host


def _hosts_from_text(text: str) -> set[str]:
    """URLs and Host: headers anywhere in a blob of text. High confidence."""
    out: set[str] = set()
    if not text:
        return out
    text = text[:MAX_SCAN_BYTES]
    for m in _URL_RE.finditer(text):
        h = _norm_host(m.group(1))
        if h:
            out.add(h)
    for m in _HOST_HEADER_RE.finditer(text):
        h = _norm_host(m.group(1))
        if h:
            out.add(h)
    return out


def _read_target_file(path: str, project_dir: str) -> set[str]:
    """Hosts listed inside a -l/-dL/-iL target file, if we can read it."""
    out: set[str] = set()
    candidates = [path]
    if not os.path.isabs(path):
        candidates.append(os.path.join(project_dir, path))
    for cand in candidates:
        try:
            if os.path.getsize(cand) > MAX_SCAN_BYTES:
                return out
            with open(cand, "r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.split("#", 1)[0].strip()
                    if not line:
                        continue
                    h = _norm_host(line)
                    if h and "." in h:
                        out.add(h)
            return out
        except OSError:
            continue
    return out


def _walk_strings(node, key: str | None = None, depth: int = 0):
    """Yield (key, string) pairs from an arbitrarily nested tool input."""
    if depth > 12:
        return
    if isinstance(node, str):
        yield (key, node)
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from _walk_strings(v, str(k), depth + 1)
    elif isinstance(node, (list, tuple)):
        for v in node:
            yield from _walk_strings(v, key, depth + 1)


def extract_hosts_mcp(tool_input: dict) -> set[str]:
    """
    Deep extraction for MCP tools, whose schemas we cannot know in advance.

    High-confidence sources, always scanned:
      - any value under a host-ish key (host, url, target, domain, endpoint, ...)
      - any http(s):// URL anywhere in any string
      - any `Host:` header inside a raw-request-ish field

    With BB_MCP_STRICT=1, additionally treat any dot-shaped token in any string as
    a hostname. That closes schema-shaped bypasses at the cost of false positives
    on servers that carry hostnames as data.
    """
    hosts: set[str] = set()
    for key, value in _walk_strings(tool_input):
        hosts |= _hosts_from_text(value)
        if key and _HOST_KEY_RE.search(key):
            h = _norm_host(value)
            if h:
                hosts.add(h)
        if key and _RAW_HTTP_KEY_RE.search(key):
            for m in _HOST_HEADER_RE.finditer(value[:MAX_SCAN_BYTES]):
                h = _norm_host(m.group(1))
                if h:
                    hosts.add(h)
        if MCP_STRICT:
            for m in _BARE_HOST_RE.finditer(value[:MAX_SCAN_BYTES]):
                cand = m.group(1).lower()
                if not _looks_like_filename(cand):
                    hosts.add(cand)
    return hosts


def extract_hosts(tool_name: str, tool_input: dict, project_dir: str) -> set[str]:
    hosts: set[str] = set()

    if tool_name.startswith("mcp__"):
        return extract_hosts_mcp(tool_input)

    if tool_name == "WebFetch":
        url = tool_input.get("url")
        if isinstance(url, str):
            h = _norm_host(url)
            if h:
                hosts.add(h)
        return hosts

    if tool_name == "Bash":
        cmd = tool_input.get("command")
        if not isinstance(cmd, str):
            return hosts
        hosts |= _hosts_from_text(cmd)
        # bare hostnames passed to recon/network CLIs
        for m in _NET_CLI_RE.finditer(cmd):
            for hm in _BARE_HOST_RE.finditer(m.group(1)):
                cand = hm.group(1).lower()
                if not _looks_like_filename(cand):
                    hosts.add(cand)
        # hosts inside target-list files (-l targets.txt, -dL scope.txt, -iL hosts)
        for m in _TARGET_FILE_RE.finditer(cmd):
            hosts |= _read_target_file(m.group(1), project_dir)
    return hosts


def block(reason: str, detail: str) -> None:
    payload = {
        "continue": False,
        "stopReason": f"scope-guard: {reason}",
        "systemMessage": detail,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": detail,
        },
    }
    print(json.dumps(payload))
    sys.exit(2)


def main() -> None:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as exc:
        if FAIL_OPEN:
            log(f"unparseable hook input, failing open: {exc}")
            sys.exit(0)
        block("unparseable hook input", f"Could not parse hook JSON: {exc}")
        return

    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}

    if tool_name in IGNORED_TOOLS:
        sys.exit(0)

    is_mcp = tool_name.startswith("mcp__")
    if tool_name not in NETWORK_TOOLS and not is_mcp:
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    allowlist_path = os.environ.get(
        "BB_ALLOWLIST", os.path.join(project_dir, "scope", "allowlist.txt")
    )
    allow, deny, mcp_local = load_allowlist(allowlist_path)

    # An MCP server explicitly marked local never touches the target.
    if is_mcp:
        parts = tool_name.split("__")
        server = parts[1].lower() if len(parts) > 1 else ""
        # plugin-bundled servers arrive as mcp__plugin_<plugin>_<server>__<tool>
        server_alt = server.split("_")[-1] if "_" in server else server
        if server in mcp_local or server_alt in mcp_local:
            sys.exit(0)

    hosts = extract_hosts(tool_name, tool_input, project_dir)
    if not hosts:
        sys.exit(0)

    # No allowlist at all: refuse to let network traffic out of the harness.
    if not allow:
        block(
            "no allowlist configured",
            f"No scope allowlist found at {allowlist_path}. "
            f"Blocked contact with: {', '.join(sorted(hosts))}. "
            "Run the scope-guard skill to create the allowlist before testing.",
        )
        return

    offenders: list[str] = []
    for host in sorted(hosts):
        if is_local(host) and not BLOCK_LOCAL:
            continue
        if any(host_matches(host, p) for p in deny):
            offenders.append(f"{host} (explicitly denied)")
            continue
        if not any(host_matches(host, p) for p in allow):
            offenders.append(f"{host} (not on allowlist)")

    if offenders:
        via = f" via {tool_name}" if tool_name else ""
        block(
            "out-of-scope host",
            f"Blocked out-of-scope target(s){via}: "
            + "; ".join(offenders)
            + f". Allowlist: {allowlist_path}. "
            "If this asset really is in scope, add it to the allowlist and "
            "re-verify the program policy first.",
        )
        return

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - hook must never crash silently
        if FAIL_OPEN:
            log(f"internal error, failing open: {exc}")
            sys.exit(0)
        block("internal error", f"scope-guard hook failed: {exc}")
