# EasyWebhook-MCP Server

**Send webhooks to any HTTP endpoint from Claude Desktop with .env file support!**

[![MCP](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-green)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

EasyWebhook-MCP is a Model Context Protocol (MCP) server that enables Claude to send webhooks to Discord, Slack, or any custom HTTP endpoint. It provides a secure interface for AI assistants to send webhook requests to various services without requiring direct API access or file system permissions. Now with **`.env` file support** for easy webhook management!

## ✨ Features

### 🎯 Core Capabilities

- ✅ Send webhooks to **any HTTP endpoint**
- ✅ Support for GET, POST, PUT, PATCH, DELETE methods
- ✅ Custom headers and JSON payloads
- ✅ **Discord embeds** with title, color, and fields
- ✅ **Slack integration** for team notifications
- ✅ **Store webhooks in .env file** for easy management
- ✅ **Reference webhooks by alias** - no more copy/paste!
- ✅ Detailed response feedback with status codes
- ✅ Error handling with clear error messages

### 🔐 Security

- No file system access required
- Runs in isolated Docker container as non-root user
- Webhook URLs masked in list output
- 30-second timeout protection prevents hanging
- HTTPS recommended for all webhook URLs
- `.env` file protected by `.gitignore`

### 🛠️ Available Tools

**Alias-Based Tools** (use stored webhooks from .env):

- `list_webhooks` - List all configured webhook aliases
- `send_webhook_by_alias` - Send webhook using stored alias
- `send_discord_webhook_by_alias` - Discord embed by alias (supports title, color, username, avatar)
- `send_slack_webhook_by_alias` - Slack message by alias

**Direct URL Tools** (pass webhook URL each time):

- `send_webhook` - Universal webhook sender (GET, POST, PUT, PATCH, DELETE)
- `send_discord_webhook` - Discord embed with URL (supports title, color, username, avatar)
- `send_slack_webhook` - Slack message with URL

## 🚀 Quick Start

### Prerequisites
- Docker Desktop with MCP Toolkit
- Claude Desktop app

### Installation

**1. Create .env file:**
```bash
cd c:\Users\plgon\Downloads\EasyWebhook-MCP
copy .env.example .env
notepad .env
```

Add your webhooks:
```env
DISCORD_WEBHOOK=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
MY_CUSTOM_API=https://api.example.com/webhook
```

**2. Build Docker image:**
```bash
docker build -t easywebhook-mcp-server .
```

**3. Configure Claude Desktop:**
```bash
# Copy catalog
copy custom.yaml $env:USERPROFILE\.docker\mcp\catalogs\custom.yaml

# Update registry
notepad $env:USERPROFILE\.docker\mcp\registry.yaml
```

Add to registry under `registry:`:
```yaml
  easywebhook:
    ref: ""
```

Update Claude config at `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/var/run/docker.sock:/var/run/docker.sock",
        "-v", "C:\\Users\\plgon\\.docker\\mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/docker-mcp.yaml",
        "--catalog=/mcp/catalogs/custom.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--tools-config=/mcp/tools.yaml",
        "--transport=stdio"
      ]
    }
  }
}
```

**4. Restart Claude Desktop**

## 💡 Usage Examples

### Using Stored Webhooks (Recommended)

**List configured webhooks:**

```text
You: "List my webhooks"

Claude: 📋 Stored Webhooks:
  • DISCORD_WEBHOOK: https://discord.com/api/webh...
  • SLACK_WEBHOOK: https://hooks.slack.com/serv...
  • MY_CUSTOM_HOOK: https://example.com/webhook...
```

**Simple Discord message:**

```text
You: "Send Discord message using DISCORD_WEBHOOK saying 'Hello World!'"

Claude: ✅ Discord embed sent successfully!
```

**Discord with title and color:**

```text
You: "Send to DISCORD_WEBHOOK with title 'Deployment Status' message 'All systems operational' and color 00FF00"

Claude: ✅ Discord embed sent successfully!
📌 Title: Deployment Status
```

**Discord with full embed (JSON):**

```text
You: "Send to DISCORD_WEBHOOK: {'title': 'Server Metrics', 'description': 'Current status', 'color': 3447003, 'fields': [{'name': 'CPU', 'value': '45%', 'inline': true}, {'name': 'RAM', 'value': '62%', 'inline': true}]}"

Claude: ✅ Discord embed sent successfully!
```

**Slack message:**

```text
You: "Send to SLACK_WEBHOOK: 'Deployment complete'"

Claude: ✅ Slack message sent successfully!
```

**Custom webhook:**

```text
You: "Use MY_CUSTOM_HOOK to send {\"status\": \"active\", \"uptime\": 3600}"

Claude: ✅ Webhook sent successfully!
📊 Status: 200
```

### Using Direct URLs

**Generic webhook:**

```text
You: "Send POST webhook to https://example.com/hook with payload {\"test\": true}"

Claude: ✅ Webhook sent successfully!
```

**Discord with URL:**

```text
You: "Send Discord webhook to [URL] with message 'Alert!' and color FF0000"

Claude: ✅ Discord embed sent successfully!
```

### Payload Formats

**Simple text:**

```json
{"message": "Hello World"}
```

**JSON payload:**

```json
{"title": "Alert", "status": "active", "priority": 1}
```

**Custom headers:**

```json
{"Authorization": "Bearer token123", "X-Custom-Header": "value"}
```

Or comma-separated:

```text
"Authorization: Bearer token123, X-Custom-Header: value"
```

## 📐 Architecture

```text
Claude Desktop → MCP Gateway → EasyWebhook MCP Server → Target Webhook URL
                                         ↓
                                .env file (local)
                                         ↓
                            Discord/Slack/Custom API
```

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive setup instructions
- **[CLAUDE.md](CLAUDE.md)** - Developer implementation guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[VISUAL_GUIDE.txt](VISUAL_GUIDE.txt)** - Visual walkthrough

## 🎯 Why Use .env Files?

**Before:**
```
❌ Copy/paste long URLs every time
❌ Risk of typos
❌ Hard to manage multiple webhooks
```

**After:**
```
✅ Simple aliases like "DISCORD_WEBHOOK"
✅ Store once, use everywhere
✅ Easy to update and manage
✅ More secure (URLs in local file)
```

## 🔧 Updating Webhooks

1. Edit `.env` file
2. Rebuild: `docker build -t easywebhook-mcp-server .`
3. Restart Claude Desktop

## 🔧 Development

### Local Testing

```bash
# Run server directly
python easywebhook_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python easywebhook_server.py
```

### Testing Webhooks

**Discord Webhook:**

Create a webhook in Discord: Server Settings → Integrations → Webhooks

**Slack Webhook:**

Create an app at [api.slack.com/apps](https://api.slack.com/apps) and enable Incoming Webhooks

**Custom Webhook:**

Any HTTP endpoint that accepts POST/GET/PUT/PATCH/DELETE requests

## 🐛 Troubleshooting

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

### "No webhook found for alias"

- Check `.env` file exists in project directory
- Verify alias name matches (case-insensitive)
- Rebuild Docker image: `docker build -t easywebhook-mcp-server .`
- Ensure the URL starts with `http://` or `https://`

### Invalid URL Errors

- Ensure URL includes `http://` or `https://`
- Verify no typos in the webhook URL
- Check that the URL is properly formatted

**Full troubleshooting guide in [SETUP_GUIDE.md](SETUP_GUIDE.md)**

## 📁 Project Structure

```
EasyWebhook-MCP/
├── .env.example              # Webhook configuration template
├── .env                      # Your webhooks (create this)
├── .gitignore                # Git ignore rules (protects .env)
├── easywebhook_server.py     # Main MCP server
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── custom.yaml               # MCP catalog definition
├── README.md                 # This file (complete documentation)
├── QUICK_START.md           # Fast setup guide
├── SETUP_GUIDE.md           # Detailed instructions
├── VISUAL_GUIDE.txt         # Visual walkthrough
├── CHANGELOG.md             # Version history
└── CLAUDE.md                # Implementation guide
```

## 🤝 Contributing

Contributions are welcome! This is an open-source MCP server and we'd love your help making it better.

### Ways to Contribute

- 🐛 **Report bugs** - Open an issue describing the problem
- 💡 **Suggest features** - Share ideas for new tools or improvements
- 📝 **Improve documentation** - Fix typos, clarify instructions, add examples
- 🔧 **Submit code** - Fix bugs, add features, improve performance
- ⭐ **Star the repo** - Show your support!

### Development Setup

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/EasyWebhook-MCP.git
   cd EasyWebhook-MCP
   ```

2. **Create a `.env` file for testing**

   ```bash
   cp .env.example .env
   # Add your test webhook URLs
   ```

3. **Make your changes**

   - Follow existing code style
   - Use single-line docstrings for MCP tools
   - Add error handling for new features
   - Test thoroughly before submitting

4. **Test your changes**

   ```bash
   # Build Docker image
   docker build -t easywebhook-mcp-server .

   # Test locally
   python easywebhook_server.py
   ```

5. **Submit a pull request**

   - Describe what your PR does
   - Reference any related issues
   - Include examples if adding new features

### Adding New Tools

To add a new webhook tool:

1. **Add the function to `easywebhook_server.py`**

   ```python
   @mcp.tool()
   async def send_my_service_webhook(webhook_url: str = "", message: str = "") -> str:
       """Send a message to MyService using a webhook URL.""  # Single-line only!
       # Implementation here
       return "✅ Message sent successfully!"
   ```

2. **Use these guidelines:**

   - Decorate with `@mcp.tool()`
   - Use **single-line docstrings only** (multi-line causes errors)
   - Use empty string defaults: `param: str = ""` not `param: str = None`
   - Return formatted strings with emojis (✅ ❌ ⚠️ 📊)
   - Add comprehensive error handling
   - Log actions to stderr

3. **Update `custom.yaml`**

   ```yaml
   tools:
     - name: send_my_service_webhook
   ```

4. **Update documentation**

   - Add usage examples to README.md
   - Update SETUP_GUIDE.md if needed
   - Update CHANGELOG.md

5. **Rebuild and test**

   ```bash
   docker build -t easywebhook-mcp-server .
   # Test in Claude Desktop
   ```

### Code Style Guidelines

- **Python:** Follow PEP 8, use async/await for HTTP operations
- **Error messages:** User-friendly with emoji indicators
- **Logging:** Use `logger.info()` and `logger.error()` for important events
- **Security:** Never log full webhook URLs, mask sensitive data
- **Type hints:** Use simple types (str, int), avoid Optional/Union

### Testing Guidelines

**Before submitting:**

- ✅ Test all new tools with real webhook URLs
- ✅ Test error conditions (invalid URLs, timeouts, etc.)
- ✅ Verify changes work in Docker container
- ✅ Check that Claude Desktop recognizes new tools
- ✅ Ensure no secrets are hardcoded or logged

### Documentation Guidelines

- Keep README.md concise and user-focused
- Add detailed examples for complex features
- Update CHANGELOG.md for all changes
- Use clear, friendly language
- Include emoji for visual clarity 🎨

### Getting Help

- **Questions?** Open a discussion or issue
- **Stuck?** Check [CLAUDE.md](CLAUDE.md) for implementation details
- **Need examples?** See existing tools in `easywebhook_server.py`

### License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 📄 License

MIT License - Use freely in your projects

## 🔗 Resources

- [Model Context Protocol](https://modelcontextprotocol.io)
- [Docker MCP](https://docs.docker.com/desktop/mcp)
- [FastMCP](https://github.com/jlowin/fastmcp)

## ⚙️ Response Format

All tools return formatted strings with:

- ✅ Success indicators
- ❌ Error messages  
- 📊 Status codes
- 🌐 URL information
- ⚡ Method used
- 📄 Response previews (first 200 chars)

## ⚠️ Limitations

- Maximum 30-second timeout per request
- Response body limited to 200 characters in output
- JSON payload format required for most structured data
- No support for file uploads via webhooks

## 🎉 What's New in v2.0

- ✨ `.env` file support for webhook storage
- 🔧 Four new alias-based tools
- 📋 `list_webhooks` tool to view configurations
- 🔒 Enhanced security with URL masking
- 🎨 Discord embeds with full customization (title, color, fields)
- 📚 Comprehensive documentation

---

**Ready to send webhooks from Claude?** Follow [QUICK_START.md](QUICK_START.md) to get started in 5 minutes! 🚀
