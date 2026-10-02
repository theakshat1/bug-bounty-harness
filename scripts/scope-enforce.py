#!/usr/bin/env python3
"""
PreToolUse scope enforcement hook for the bug bounty harness.

Reads the Claude Code PreToolUse hook JSON on stdin, extracts every hostname the
tool call would contact, and hard-blocks the call if any host is not covered by
the campaign allowlist.

A prompt can only ask an agent to stay in scope. This can actually stop it.

Exit codes (Claude Code hook contract):
    0  allow  (prints nothing, or a JSON advisory)
    2  BLOCK  (blocking error; the tool call does not run)
    1  internal error -> fail CLOSED by default (see FAIL_OPEN below)

Allowlist file (default ``scope/allowlist.txt``, override with BB_ALLOWLIST):
    # comments and blank lines ignored
    example.com            -> exact host only
    *.example.com          -> any subdomain, at any depth, plus example.com
    !blog.example.com      -> explicit deny; overrides any wildcard match

Localhost, loopback and RFC1918 collaborator/listener addresses are allowed by
default so local tooling keeps working; set BB_BLOCK_LOCAL=1 to tighten that.
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

# Tools that can reach the network and therefore need scope enforcement.
NETWORK_TOOLS = {"WebFetch", "Bash", "WebSearch"}

LOCAL_HOSTNAMES = {"localhost", "127.0.0.1", "::1", "0.0.0.0", "burp", "collaborator"}

# Hostname/URL extraction from shell command lines.
_URL_RE = re.compile(r"\bhttps?://([^\s/'\"|;<>)\\]+)", re.I)
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


def log(msg: str) -> None:
    sys.stderr.write(f"[scope-guard] {msg}\n")


def load_allowlist(path: str) -> tuple[list[str], list[str]]:
    """Return (allow_patterns, deny_patterns)."""
    allow: list[str] = []
    deny: list[str] = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.split("#", 1)[0].strip().lower()
                if not line:
                    continue
                if line.startswith("!"):
                    deny.append(line[1:].strip())
                else:
                    allow.append(line)
    except FileNotFoundError:
        return ([], [])
    return (allow, deny)


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


def extract_hosts(tool_name: str, tool_input: dict) -> set[str]:
    hosts: set[str] = set()

    def add_from_url(value: str) -> None:
        try:
            parsed = urlparse(value if "://" in value else "//" + value)
            if parsed.hostname:
                hosts.add(parsed.hostname.lower())
        except ValueError:
            pass

    if tool_name == "WebFetch":
        url = tool_input.get("url")
        if isinstance(url, str):
            add_from_url(url)
        return hosts

    if tool_name == "WebSearch":
        # A web search does not contact the target; nothing to enforce.
        return hosts

    if tool_name == "Bash":
        cmd = tool_input.get("command") or ""
        if not isinstance(cmd, str):
            return hosts
        for m in _URL_RE.finditer(cmd):
            add_from_url(m.group(1))
        # bare hostnames passed to recon/network CLIs
        for m in _NET_CLI_RE.finditer(cmd):
            for hm in _BARE_HOST_RE.finditer(m.group(1)):
                candidate = hm.group(1).lower()
                # skip things that are obviously filenames
                if candidate.rsplit(".", 1)[-1] in {
                    "txt", "json", "md", "sh", "py", "js", "yaml", "yml",
                    "csv", "log", "conf", "xml", "html", "zip", "gz",
                }:
                    continue
                hosts.add(candidate)
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
    tool_input = event.get("tool_input") or {}

    if tool_name not in NETWORK_TOOLS:
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    allowlist_path = os.environ.get(
        "BB_ALLOWLIST", os.path.join(project_dir, "scope", "allowlist.txt")
    )
    allow, deny = load_allowlist(allowlist_path)

    hosts = extract_hosts(tool_name, tool_input)
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
        block(
            "out-of-scope host",
            "Blocked out-of-scope target(s): "
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
