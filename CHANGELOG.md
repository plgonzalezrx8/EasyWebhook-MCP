# EasyWebhook-MCP Changelog

## Version 2.0 - .env File Support

### New Features

#### 🎉 Environment Variable Configuration
- Added `.env` file support for storing webhook URLs
- No more copy/pasting webhook URLs repeatedly
- Store unlimited webhooks with custom aliases

#### 🔧 New Tools
- `list_webhooks` - List all configured webhook aliases
- `send_webhook_by_alias` - Send webhooks using stored aliases
- `send_discord_webhook_by_alias` - Discord webhooks by alias
- `send_slack_webhook_by_alias` - Slack webhooks by alias

#### 📁 New Files
- `.env.example` - Template for webhook configuration
- `SETUP_GUIDE.md` - Comprehensive setup instructions
- `custom.yaml` - Updated catalog with new tools

### Improvements
- Added `python-dotenv` dependency
- Updated Dockerfile to include .env files
- Enhanced security with URL masking in list output
- Flexible alias naming (works with or without WEBHOOK_ prefix)

### Backward Compatibility
- ✅ All original tools still work
- ✅ Direct URL passing still supported
- ✅ No breaking changes

### Usage

**Before (v1.0):**
```
"Send Discord webhook to https://discord.com/api/webhooks/long-url-here..."
```

**After (v2.0):**
```
1. Add to .env: DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
2. Use: "Send Discord message using DISCORD_WEBHOOK saying 'Hello!'"
```

### Migration Guide

#### Existing Users
1. Create `.env` file in project directory
2. Copy your frequently-used webhook URLs
3. Rebuild Docker image
4. Update custom.yaml catalog with new tools
5. Restart Claude Desktop

#### New Users
Follow the SETUP_GUIDE.md for complete instructions.

---

## Version 1.0 - Initial Release

### Features
- `send_webhook` - Universal HTTP webhook sender
- `send_discord_webhook` - Discord-specific webhook
- `send_slack_webhook` - Slack-specific webhook
- Support for GET, POST, PUT, PATCH, DELETE methods
- Custom headers and JSON payloads
- Comprehensive error handling
- Docker containerization
