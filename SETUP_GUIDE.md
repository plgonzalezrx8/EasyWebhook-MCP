# EasyWebhook-MCP Setup Guide

## What's New: .env File Support! 🎉

You can now store your webhook URLs in a `.env` file and reference them by alias instead of pasting the full URL every time.

## Quick Start

### Step 1: Create Your .env File

Copy the example file and add your webhooks:

```bash
cd c:\Users\plgon\Downloads\EasyWebhook-MCP
copy .env.example .env
notepad .env
```

### Step 2: Add Your Webhook URLs

Edit `.env` and add your webhooks:

```env
# Discord Webhooks
DISCORD_WEBHOOK=https://discord.com/api/webhooks/123456789/your-token-here
DISCORD_ALERTS=https://discord.com/api/webhooks/987654321/another-token

# Slack Webhooks
SLACK_WEBHOOK=https://hooks.slack.com/services/T00/B00/xxxx
SLACK_TEAM=https://hooks.slack.com/services/T11/B11/yyyy

# Custom Webhooks
MY_API=https://api.example.com/webhook
MONITORING=https://monitor.example.com/hooks/123
```

**Naming Tips:**
- Use UPPERCASE names (e.g., `DISCORD_WEBHOOK`, `MY_HOOK`)
- You can use any name you want
- System accepts both `DISCORD_WEBHOOK` and `WEBHOOK_DISCORD` formats
- Be descriptive: `DISCORD_ALERTS`, `SLACK_DEPLOYMENTS`, etc.

### Step 3: Build Docker Image

```bash
docker build -t easywebhook-mcp-server .
```

The `.env` file will automatically be included in the Docker image.

### Step 4: Configure Claude Desktop

#### Create Custom Catalog

Create the catalog directory:
```bash
mkdir -p $env:USERPROFILE\.docker\mcp\catalogs
```

Copy the provided `custom.yaml` to your catalog directory:
```bash
copy custom.yaml $env:USERPROFILE\.docker\mcp\catalogs\custom.yaml
```

Or manually create `~/.docker/mcp/catalogs/custom.yaml` with the contents from `custom.yaml`.

#### Update Registry

Edit `~/.docker/mcp/registry.yaml` and add under the `registry:` key:

```yaml
registry:
  easywebhook:
    ref: ""
```

#### Update Claude Desktop Config

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
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

### Step 5: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Restart it
3. Your tools are ready!

## Usage Examples

### List Your Stored Webhooks

Ask Claude:
> "List my webhooks"

Output:
```
📋 Stored Webhooks:

  • DISCORD_WEBHOOK: https://discord.com/api/webh...
  • SLACK_WEBHOOK: https://hooks.slack.com/serv...
  • MY_API: https://api.example.com/webh...

Use these aliases with the *_by_alias tools.
```

### Using Aliases (Recommended)

**Discord:**
> "Send a Discord message using DISCORD_WEBHOOK saying 'Hello World!'"

**Slack:**
> "Send to SLACK_WEBHOOK: 'Deployment complete'"

**Custom Webhook:**
> "Use MY_API to send this JSON: {\"status\": \"online\", \"uptime\": 3600}"

### Using Direct URLs (Still Supported)

You can still use webhooks without storing them:

> "Send a Discord webhook to https://discord.com/... with message 'Test'"

## Benefits of Using .env

✅ **No Copy/Paste** - Just use the alias name  
✅ **Secure** - URLs stay in your local .env file  
✅ **Multiple Webhooks** - Store as many as you need  
✅ **Easy Updates** - Change URL once in .env, works everywhere  
✅ **Organized** - Keep all webhooks in one place  

## Security Notes

- ✅ `.env` file stays in your Docker container
- ✅ Webhooks are masked when listed (only first 30 chars shown)
- ✅ Never commit `.env` to version control (use `.env.example`)
- ✅ URLs are never exposed in logs

## Tools Available

### With Stored Webhooks
- `list_webhooks` - See all your configured webhooks
- `send_webhook_by_alias` - Send webhook using alias
- `send_discord_webhook_by_alias` - Discord with alias
- `send_slack_webhook_by_alias` - Slack with alias

### With Direct URLs
- `send_webhook` - Generic webhook sender
- `send_discord_webhook` - Discord webhook
- `send_slack_webhook` - Slack webhook

## Troubleshooting

### Webhooks Not Found

If you get "No webhook found for alias":

1. Check your `.env` file exists in the project directory
2. Verify the alias name matches (case-insensitive)
3. Rebuild the Docker image: `docker build -t easywebhook-mcp-server .`
4. Ensure the URL starts with `http://` or `https://`

### Can't See Tools

1. Verify Docker image built: `docker images | grep easywebhook`
2. Check catalog file syntax
3. Restart Claude Desktop completely
4. Check Docker logs: `docker ps` then `docker logs [container-id]`

### .env File Not Loaded

The Docker build copies `.env` automatically. If it's not working:

1. Ensure `.env` exists in the project root
2. Rebuild: `docker build -t easywebhook-mcp-server .`
3. Check Docker build logs for errors

## Updating Webhooks

To add or change webhooks:

1. Edit `.env` file
2. Rebuild Docker image: `docker build -t easywebhook-mcp-server .`
3. Restart Claude Desktop

## Example .env File

```env
# ============================================
# EasyWebhook Configuration
# ============================================

# Discord Webhooks
# Get these from: Server Settings → Integrations → Webhooks
DISCORD_MAIN=https://discord.com/api/webhooks/123456789/abcdefghijklmnop
DISCORD_ALERTS=https://discord.com/api/webhooks/987654321/qrstuvwxyz123456
DISCORD_LOGS=https://discord.com/api/webhooks/111222333/another-webhook

# Slack Webhooks  
# Get these from: https://api.slack.com/apps → Incoming Webhooks
SLACK_GENERAL=https://hooks.slack.com/services/T00/B00/xxxxxxxxxxxxx
SLACK_DEPLOYMENTS=https://hooks.slack.com/services/T11/B11/yyyyyyyyyyyyy
SLACK_ALERTS=https://hooks.slack.com/services/T22/B22/zzzzzzzzzzzzz

# Custom API Webhooks
API_PRODUCTION=https://api.example.com/webhooks/prod-12345
API_STAGING=https://api.example.com/webhooks/stage-67890
MONITORING_SERVICE=https://monitor.example.com/hooks/my-service
GITHUB_WEBHOOK=https://github.example.com/webhook/repo-123

# Development/Testing
TEST_WEBHOOK=https://webhook.site/unique-id-here
DEBUG_ENDPOINT=http://localhost:3000/webhook
```

## Tips & Best Practices

1. **Organize by Service** - Group webhooks by platform (Discord, Slack, etc.)
2. **Use Descriptive Names** - `DISCORD_ALERTS` instead of `WEBHOOK1`
3. **Document Purpose** - Add comments explaining each webhook
4. **Keep .env.example** - Update it when you add new webhook types
5. **Test Before Production** - Use test webhooks first
6. **Backup Your .env** - Keep a secure backup of your webhooks

## Next Steps

1. ✅ Create your `.env` file
2. ✅ Add your webhook URLs
3. ✅ Build the Docker image
4. ✅ Configure Claude Desktop
5. ✅ Test with "List my webhooks"
6. ✅ Start sending webhooks!

Enjoy your streamlined webhook workflow! 🚀
