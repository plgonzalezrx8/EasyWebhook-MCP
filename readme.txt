# EasyWebhook MCP Server

A Model Context Protocol (MCP) server that sends webhooks to any HTTP endpoint.

## Purpose

This MCP server provides a secure interface for AI assistants to send webhook requests to various services like Discord, Slack, or any custom HTTP endpoint. It simplifies webhook integration without requiring direct API access or file system permissions.

## Features

### Current Implementation

**Direct URL Tools** (pass webhook URL each time):
- **`send_webhook`** - Send a webhook request to any HTTP endpoint with custom payload, headers, and HTTP method (GET, POST, PUT, PATCH, DELETE)
- **`send_discord_webhook`** - Send a message to Discord using a Discord webhook URL with optional custom username and avatar
- **`send_slack_webhook`** - Send a message to Slack using a Slack webhook URL

**Alias Tools** (use stored webhooks from .env file):
- **`send_webhook_by_alias`** - Send a webhook using a stored alias with custom payload and headers
- **`send_discord_webhook_by_alias`** - Send a Discord message using a stored webhook alias
- **`send_slack_webhook_by_alias`** - Send a Slack message using a stored webhook alias
- **`list_webhooks`** - List all webhook aliases configured in your .env file

### Key Capabilities

- Support for multiple HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Custom headers and JSON payloads
- Specialized Discord webhook support with username/avatar customization
- Specialized Slack webhook support
- Detailed response feedback with status codes
- Error handling with clear error messages
- 30-second timeout protection
- No file system access required

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
- Webhook URLs from your target services (Discord, Slack, etc.)

## Installation

### Quick Setup with .env File

1. Copy `.env.example` to `.env` in the project directory
2. Add your webhook URLs to the `.env` file
3. Follow the installation instructions below

Example `.env` file:
```
DISCORD_WEBHOOK=https://discord.com/api/webhooks/123456/abcdef
SLACK_WEBHOOK=https://hooks.slack.com/services/ABC/DEF/xyz
MY_CUSTOM_HOOK=https://example.com/webhook
```

See the step-by-step instructions below.

## Usage Examples

In Claude Desktop, you can ask:

### Using Stored Webhooks (Recommended)
- "List my webhooks" - See all configured webhooks
- "Send a Discord message using DISCORD_WEBHOOK alias saying 'Hello!'"
- "Send to my SLACK_WEBHOOK alias: 'Deployment complete'"
- "Use MY_CUSTOM_HOOK to send this data: {\"status\": \"active\"}"

### Discord Webhooks (Direct URL)
- "Send a Discord webhook to [URL] with the message 'Hello from Claude!'"
- "Post to my Discord webhook with message 'Task completed' and username 'Bot Assistant'"
- "Send a Discord notification to [URL] saying 'System alert' with avatar URL [URL]"

### Slack Webhooks (Direct URL)
- "Send a Slack webhook to [URL] with the message 'Deployment successful!'"
- "Post to Slack saying 'Meeting reminder in 5 minutes'"

### Generic Webhooks (Direct URL)
- "Send a POST webhook to [URL] with payload {\"status\": \"completed\"}"
- "Send a PUT request to [URL] with custom headers and this JSON data: {\"id\": 123}"
- "Make a webhook call to [URL] using DELETE method"

### Payload Formats

**Simple text:**
```
message: "Hello World"
```

**JSON format:**
```
payload: {"title": "Alert", "status": "active", "priority": 1}
```

**Custom headers:**
```
headers: {"Authorization": "Bearer token123", "X-Custom-Header": "value"}
```

Or comma-separated:
```
headers: "Authorization: Bearer token123, X-Custom-Header: value"
```

## Architecture

```
Claude Desktop → MCP Gateway → EasyWebhook MCP Server → Target Webhook URL
                                                        ↓
                                               Discord/Slack/Custom API
```

## Development

### Local Testing

```bash
# Run directly
python easywebhook_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python easywebhook_server.py
```

### Adding New Tools

1. Add the function to easywebhook_server.py
2. Decorate with @mcp.tool()
3. Use single-line docstrings only
4. Return formatted strings with emojis for clarity
5. Update the catalog entry with the new tool name
6. Rebuild the Docker image

### Testing Webhooks

**Discord Webhook:**
Create a webhook in Discord Server Settings → Integrations → Webhooks

**Slack Webhook:**
Create an app at api.slack.com/apps and enable Incoming Webhooks

**Custom Webhook:**
Any HTTP endpoint that accepts POST/GET/PUT/PATCH/DELETE requests

## Troubleshooting

### Tools Not Appearing
- Verify Docker image built successfully: `docker images | grep easywebhook`
- Check catalog and registry files for syntax errors
- Ensure Claude Desktop config includes custom catalog path
- Restart Claude Desktop completely (quit and reopen)

### Webhook Failures
- Verify the webhook URL is correct and accessible
- Check that the webhook hasn't been deleted or revoked
- Ensure payload format matches the expected format for the service
- Review error messages for HTTP status codes

### Timeout Errors
- Webhook endpoint may be slow or unavailable
- Check network connectivity
- Verify the target service is operational

### Invalid URL Errors
- Ensure URL includes http:// or https://
- Verify no typos in the webhook URL
- Check that the URL is properly formatted

## Security Considerations

- No secrets stored (webhook URLs are provided per-request)
- No file system access
- Running as non-root user in Docker
- 30-second timeout prevents hanging requests
- All requests logged to stderr for audit trail
- HTTPS recommended for all webhook URLs

## Response Format

All tools return formatted strings with:
- ✅ Success indicators
- ❌ Error messages
- 📊 Status codes
- 🌐 URL information
- ⚡ Method used
- 📄 Response previews

## Limitations

- Maximum 30-second timeout per request
- Response body limited to 200 characters in output
- JSON payload format required for most structured data
- No support for file uploads via webhooks

## License

MIT License - Use freely in your projects
