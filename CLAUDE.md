# EasyWebhook MCP Server - Implementation Guide

## Overview

EasyWebhook is a Model Context Protocol (MCP) server designed to send webhook requests to any HTTP endpoint. It provides a simple, secure way for Claude to interact with external services through webhooks without requiring file system access or complex authentication.

## Architecture

### Components

1. **FastMCP Server** - MCP protocol handler
2. **HTTPX Client** - Async HTTP request handler
3. **Tool Functions** - Three webhook tools with different specializations
4. **Error Handling** - Comprehensive error catching and user-friendly messages

### Design Decisions

**Why No Type Hints?**
- Type hints from the `typing` module cause compatibility issues with Claude Desktop
- Using simple type annotations (str, int) without Optional, Union, etc.
- Default empty strings instead of None values

**Why Single-Line Docstrings?**
- Multi-line docstrings cause "gateway panic" errors
- Single-line format ensures compatibility
- Tool descriptions must be clear and concise

**Why String Returns?**
- MCP tools must return formatted strings
- Allows for emoji-enhanced, human-readable responses
- Makes error messages more accessible to users

## Tool Implementations

### 1. send_webhook

**Purpose:** Universal webhook sender for any HTTP endpoint

**Parameters:**
- `webhook_url` (required) - Target URL
- `payload` (optional) - JSON payload as string
- `headers` (optional) - Custom headers
- `method` (optional) - HTTP method (default: POST)

**Features:**
- Supports GET, POST, PUT, PATCH, DELETE
- Flexible payload parsing (JSON or plain text)
- Custom header support
- Comprehensive error handling

**Use Cases:**
- Generic API webhooks
- Custom integrations
- Testing HTTP endpoints
- Non-standard webhook formats

### 2. send_discord_webhook

**Purpose:** Specialized Discord webhook sender

**Parameters:**
- `webhook_url` (required) - Discord webhook URL
- `message` (required) - Message content
- `username` (optional) - Custom bot username
- `avatar_url` (optional) - Custom bot avatar

**Features:**
- Discord-specific payload formatting
- Username and avatar customization
- URL validation for Discord domains
- Handles 204 (no content) success response

**Use Cases:**
- Discord notifications
- Bot message sending
- Server alerts
- Custom Discord integrations

### 3. send_slack_webhook

**Purpose:** Specialized Slack webhook sender

**Parameters:**
- `webhook_url` (required) - Slack webhook URL
- `message` (required) - Message text

**Features:**
- Slack-specific payload formatting
- URL validation for Slack domains
- Simple text message format
- Compatible with Slack incoming webhooks

**Use Cases:**
- Slack notifications
- Team alerts
- Deployment notifications
- System monitoring alerts

## Error Handling Strategy

### Validation Errors
- Check for empty required parameters
- Validate URL formats
- Verify HTTP methods
- Return clear error messages with ❌ emoji

### Network Errors
- Catch timeout exceptions (30s limit)
- Handle connection errors
- Report HTTP status errors
- Provide detailed error context

### Parsing Errors
- Handle invalid JSON gracefully
- Fall back to text format when JSON fails
- Log warnings for malformed input
- Continue execution when possible

## Response Formatting

### Success Format
```
✅ Webhook sent successfully!

📊 Status: 200
🌐 URL: https://example.com
⚡ Method: POST

📄 Response:
[Response preview]
```

### Error Format
```
❌ Error: [Error description]
🌐 URL: [URL if available]

[Additional context]
```

## Best Practices

### Code Style
1. Use async/await for all HTTP operations
2. Always log important actions to stderr
3. Include context in error messages
4. Keep functions focused and single-purpose
5. Use emoji consistently for visual parsing

### Security
1. No hardcoded credentials
2. Validate all URLs
3. Limit response body exposure
4. Run as non-root user
5. Use timeouts to prevent hanging

### Performance
1. Use httpx.AsyncClient for efficiency
2. Set reasonable timeouts (30s)
3. Close connections properly with context managers
4. Limit response body reads

### User Experience
1. Clear, actionable error messages
2. Visual indicators with emojis
3. Preview long responses
4. Show relevant context in outputs
5. Guide users toward solutions

## Extension Points

### Adding New Webhook Types

To add a new specialized webhook (e.g., Microsoft Teams):

1. **Create new tool function:**
```python
@mcp.tool()
async def send_teams_webhook(webhook_url: str = "", message: str = "") -> str:
    """Send a message to Microsoft Teams using a Teams webhook URL."""
    # Validate inputs
    if not webhook_url.strip():
        return "❌ Error: webhook_url is required"
    
    # Build Teams-specific payload
    teams_payload = {
        "text": message.strip()
    }
    
    # Send request and handle response
    ...
```

2. **Update catalog.yaml** with new tool name

3. **Update readme.txt** with usage examples

4. **Rebuild Docker image**

### Adding New Features

**Request Retries:**
```python
from httpx import AsyncClient
import asyncio

max_retries = 3
for attempt in range(max_retries):
    try:
        response = await client.post(...)
        break
    except httpx.RequestError:
        if attempt == max_retries - 1:
            raise
        await asyncio.sleep(2 ** attempt)
```

**Webhook Validation:**
```python
def validate_webhook_signature(payload, signature, secret):
    """Validate webhook signature for security."""
    import hmac
    import hashlib
    
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)
```

## Common Issues and Solutions

### Issue: Gateway Panic Error
**Cause:** Multi-line docstrings or prompt decorators
**Solution:** Use single-line docstrings only, no @mcp.prompt()

### Issue: Type Error in Parameters
**Cause:** Using Optional, Union, or List type hints
**Solution:** Use simple types (str, int) with default empty strings

### Issue: Tool Not Showing in Claude
**Cause:** Catalog not registered or syntax error
**Solution:** Check custom.yaml syntax, verify registry.yaml entry

### Issue: Webhook Timeout
**Cause:** Slow or unreachable endpoint
**Solution:** Check endpoint status, consider increasing timeout

### Issue: Invalid JSON Payload
**Cause:** Malformed JSON string
**Solution:** Use format_payload utility to handle both JSON and text

## Testing Guidelines

### Unit Testing
```python
import pytest
from easywebhook_server import format_headers, format_payload

def test_format_headers():
    result = format_headers('{"Auth": "Bearer token"}')
    assert result == {"Auth": "Bearer token"}

def test_format_payload():
    result = format_payload('{"key": "value"}')
    assert result == {"key": "value"}
```

### Integration Testing
```bash
# Test with curl
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  python easywebhook_server.py
```

### Manual Testing
1. Build Docker image
2. Run container locally
3. Use Claude Desktop to test each tool
4. Verify webhooks received at destination
5. Test error conditions

## Deployment Checklist

- [ ] All files created (5 total)
- [ ] Dockerfile builds successfully
- [ ] Python dependencies installed
- [ ] Server starts without errors
- [ ] Tools appear in tools/list
- [ ] Custom catalog created
- [ ] Registry updated
- [ ] Claude Desktop config updated
- [ ] Claude Desktop restarted
- [ ] Tools visible in Claude
- [ ] Test webhooks successful
- [ ] Error handling verified

## Maintenance

### Updating Dependencies
```bash
# Update requirements.txt
pip install --upgrade mcp httpx
pip freeze > requirements.txt

# Rebuild image
docker build -t easywebhook-mcp-server .
```

### Monitoring
- Check Docker logs: `docker logs [container]`
- Review stderr output for errors
- Monitor webhook success rates
- Track response times

### Version Control
- Tag releases: `v1.0.0`, `v1.1.0`
- Document breaking changes
- Keep changelog updated
- Archive old versions

## Support Resources

- **MCP Documentation:** https://modelcontextprotocol.io
- **FastMCP GitHub:** https://github.com/jlowin/fastmcp
- **HTTPX Documentation:** https://www.python-httpx.org
- **Docker MCP:** https://docs.docker.com/desktop/mcp

## Contributing

To contribute improvements:
1. Test changes locally
2. Update documentation
3. Follow existing code style
4. Add error handling
5. Update catalog and readme
6. Rebuild and test Docker image
