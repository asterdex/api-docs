# Contributing to AsterDex API Docs (Community Fork)

Thank you for helping improve the AsterDex API documentation. This fork is maintained by the community to fill gaps in the official documentation.

## How to Contribute

### Reporting Issues

Use the [issue templates](./.github/ISSUE_TEMPLATE/) for:
- **Missing endpoint** — An endpoint that works but isn't documented
- **Doc error** — Incorrect parameter, wrong response format, broken example
- **Feature request** — SDK improvements, new examples, tooling

### Submitting Changes

1. Fork this repository
2. Create a feature branch: `git checkout -b fix/endpoint-description`
3. Make your changes
4. Run the linter: `npm run lint` (if applicable)
5. Submit a Pull Request with a clear description

### Documentation Standards

When documenting an endpoint:

```markdown
## Endpoint Name (AUTH_TYPE)

> **Response:**

\`\`\`json
{ "example": "response" }
\`\`\`

\`\`METHOD /fapi/v3/endpoint\`\`

**Weight:** N

**Parameters:**

| Name | Type | Mandatory | Description |
|---|---|---|---|
| param | TYPE | YES/NO | What it does |
```

### Code Examples

- Python examples go in `examples/python/`
- JavaScript examples go in `examples/javascript/`
- Go examples go in `examples/go/`
- **Never commit real private keys, API secrets, or wallet addresses with funds**
- Use placeholder values: `0x0000...`, `your_private_key_here`

### SDK Changes

- Python SDK: `sdk/python/`
- JavaScript SDK: `sdk/javascript/`
- Include tests for new functionality
- Follow existing code style

## Code of Conduct

Be respectful. This is a community effort to make AsterDex more accessible to developers. Constructive feedback only.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
