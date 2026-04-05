# Security Policy

## Scope

This repository contains **documentation and SDK code** for the AsterDex API. It does not contain the AsterDex platform itself.

## Reporting Security Issues

### In this repository

If you find a security issue in the SDK code (e.g., improper key handling, signature vulnerability):

1. **Do not open a public issue**
2. Email: security@kairoslab.xyz
3. Include: description, reproduction steps, impact assessment

We will acknowledge within 48 hours and provide a fix timeline within 7 days.

### In AsterDex itself

If you find a security vulnerability in the AsterDex platform:

- Use the [Immunefi bug bounty program](https://immunefi.com/) if available
- Contact AsterDex support directly via their Discord
- **Do not disclose publicly until the issue is resolved**

## Supported Versions

| Version | Supported |
|---|---|
| SDK latest | Yes |
| SDK < latest | Best effort |

## Secret Scanning

This repository has GitHub secret scanning enabled. If you accidentally commit credentials:

1. **Rotate the compromised credentials immediately**
2. Open an issue so we can scrub git history
3. Never reuse the exposed credentials
