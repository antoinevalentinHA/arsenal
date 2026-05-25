# Security Policy

## Scope

This repository contains a personal Home Assistant architecture, configuration
patterns, documentation, and validation scripts.

It is published for transparency, learning, and architectural reference.

This is not a packaged product, a managed service, or a security-critical framework.

## Reporting a vulnerability

If you believe you have found a security issue in this repository, please report
it privately using [GitHub private vulnerability reporting][gh-pvr].

Do not open a public issue for suspected security problems involving:

- exposed secrets or credentials
- unsafe Home Assistant configuration patterns
- authentication or access-control weaknesses
- network, VPN, NAS, or infrastructure exposure
- automation logic that could cause unsafe physical behavior

## What to include

When possible, provide:

- the affected file or area
- a short description of the issue
- the potential impact
- steps to reproduce or verify
- suggested mitigation, if known

## Out of scope

- generic Home Assistant hardening advice
- issues caused by local deployment choices
- missing features
- theoretical attacks without plausible impact
- vulnerabilities in upstream projects or integrations

## Response expectations

This is a personal project maintained on a best-effort basis.  
There is no guaranteed response time, SLA, or bug bounty program.  
Valid reports will be reviewed and addressed when appropriate.

## Public disclosure

Please allow reasonable time for review before publicly disclosing any
security-sensitive finding.

[gh-pvr]: https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability