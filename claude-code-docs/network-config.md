url: https://docs.anthropic.com/en/docs/claude-code/network-config

---

Claude Code supports various enterprise network and security configurations through environment variables. This includes routing traffic through corporate proxy servers, trusting custom Certificate Authorities \(CA\), and authenticating with mutual Transport Layer Security \(mTLS\) certificates for enhanced security.

All environment variables shown on this page can also be configured in [`settings.json`](/en/docs/claude-code/settings).

## Proxy configuration

### Environment variables

Claude Code respects standard proxy environment variables:

Copy
[code]
    # HTTPS proxy (recommended)
    export HTTPS_PROXY=https://proxy.example.com:8080

    # HTTP proxy (if HTTPS not available)
    export HTTP_PROXY=http://proxy.example.com:8080

    # Bypass proxy for specific requests - space-separated format
    export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
    # Bypass proxy for specific requests - comma-separated format
    export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
    # Bypass proxy for all requests
    export NO_PROXY="*"

[/code]

Claude Code does not support SOCKS proxies.

### Basic authentication

If your proxy requires basic authentication, include credentials in the proxy URL:

Copy
[code]
    export HTTPS_PROXY=http://username:password@proxy.example.com:8080

[/code]

Avoid hardcoding passwords in scripts. Use environment variables or secure credential storage instead.

For proxies requiring advanced authentication \(NTLM, Kerberos, etc.\), consider using an LLM Gateway service that supports your authentication method.

## Custom CA certificates

If your enterprise environment uses custom CAs for HTTPS connections \(whether through a proxy or direct API access\), configure Claude Code to trust them:

Copy
[code]
    export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem

[/code]

## mTLS authentication

For enterprise environments requiring client certificate authentication:

Copy
[code]
    # Client certificate for authentication
    export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

    # Client private key
    export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

    # Optional: Passphrase for encrypted private key
    export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"

[/code]

## Network access requirements

Claude Code requires access to the following URLs:

  * `api.anthropic.com` \- Claude API endpoints
  * `claude.ai` \- WebFetch safeguards
  * `statsig.anthropic.com` \- Telemetry and metrics
  * `sentry.io` \- Error reporting

Ensure these URLs are allowlisted in your proxy configuration and firewall rules. This is especially important when using Claude Code in containerized or restricted network environments.

## Additional resources

  * [Claude Code settings](/en/docs/claude-code/settings)
  * [Environment variables reference](/en/docs/claude-code/settings#environment-variables)
  * [Troubleshooting guide](/en/docs/claude-code/troubleshooting)

Was this page helpful?

YesNo

[Google Vertex AI](/en/docs/claude-code/google-vertex-ai)[LLM gateway](/en/docs/claude-code/llm-gateway)
