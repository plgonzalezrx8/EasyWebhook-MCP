# EasyWebhook-MCP Server

**Send webhooks to any HTTP endpoint from Claude Desktop with .env file support!**

[![MCP](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-green)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

EasyWebhook-MCP is a Model Context Protocol server that enables Claude to send webhooks to Discord, Slack, or any custom HTTP endpoint. Now with **`.env` file support** for easy webhook management!

## ✨ Features

### 🎯 Core Capabilities
- ✅ Send webhooks to **any HTTP endpoint**
- ✅ Support for GET, POST, PUT, PATCH, DELETE methods
- ✅ Custom headers and JSON payloads
- ✅ Specialized Discord & Slack integrations
- ✅ **NEW: Store webhooks in .env file**
- ✅ **NEW: Reference webhooks by alias**

### 🔐 Security
- No file system access required
- Runs in isolated Docker container
- Webhook URLs masked in output
- 30-second timeout protection

### 🛠️ Tools Available

**With .env Aliases (Recommended):**
- `list_webhooks` - View all configured webhooks
- `send_webhook_by_alias` - Send using stored webhook
- `send_discord_webhook_by_alias` - Discord by alias
- `send_slack_webhook_by_alias` - Slack by alias

**Direct URL (Also Supported):**
- `send_webhook` - Universal webhook sender
- `send_discord_webhook` - Discord with URL
- `send_slack_webhook` - Slack with URL

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

### View Your Webhooks
```
You: "List my webhooks"

Claude: 📋 Stored Webhooks:
  • DISCORD_WEBHOOK: https://discord.com/api/webh...
  • SLACK_WEBHOOK: https://hooks.slack.com/serv...
```

### Send Discord Message (by alias)
```
You: "Send Discord message using DISCORD_WEBHOOK saying 'Hello World!'"

Claude: ✅ Discord message sent successfully!
```

### Send Slack Message (by alias)
```
You: "Send to SLACK_WEBHOOK: 'Deployment complete'"

Claude: ✅ Slack message sent successfully!
```

### Send Custom Webhook (by alias)
```
You: "Use MY_CUSTOM_API to send this JSON: {\"status\": \"active\"}"

Claude: ✅ Webhook sent successfully!
```

### Send with Direct URL (no .env)
```
You: "Send webhook to https://example.com/hook with payload {\"test\": true}"

Claude: ✅ Webhook sent successfully!
```

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive setup instructions
- **[readme.txt](readme.txt)** - Full feature documentation
- **[CLAUDE.md](CLAUDE.md)** - Developer implementation guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

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

## 🐛 Troubleshooting

**Tools not appearing?**
- Check: `docker images | grep easywebhook`
- Verify catalog: `~/.docker/mcp/catalogs/custom.yaml`
- Restart Claude Desktop completely

**"No webhook found for alias"?**
- Check `.env` file exists in project directory
- Verify webhook URL starts with `http://` or `https://`
- Rebuild Docker image

**Full troubleshooting guide in [SETUP_GUIDE.md](SETUP_GUIDE.md)**

## 📁 Project Structure

```
EasyWebhook-MCP/
├── .env.example              # Webhook configuration template
├── .env                      # Your webhooks (create this)
├── easywebhook_server.py     # Main MCP server
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── custom.yaml               # MCP catalog definition
├── README.md                 # This file
├── QUICK_START.md           # Fast setup guide
├── SETUP_GUIDE.md           # Detailed instructions
├── CHANGELOG.md             # Version history
├── readme.txt               # Full documentation
└── CLAUDE.md                # Implementation guide
```

## 🤝 Contributing

Suggestions and improvements welcome! This is an open-source MCP server.

## 📄 License

MIT License - Use freely in your projects

## 🔗 Resources

- [Model Context Protocol](https://modelcontextprotocol.io)
- [Docker MCP](https://docs.docker.com/desktop/mcp)
- [FastMCP](https://github.com/jlowin/fastmcp)

## 🎉 What's New in v2.0

- ✨ `.env` file support for webhook storage
- 🔧 Four new alias-based tools
- 📋 `list_webhooks` tool to view configurations
- 🔒 Enhanced security with URL masking
- 📚 Comprehensive documentation

---

**Ready to send webhooks from Claude?** Follow [QUICK_START.md](QUICK_START.md) to get started in 5 minutes! 🚀
