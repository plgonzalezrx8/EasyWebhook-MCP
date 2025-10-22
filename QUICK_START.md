# EasyWebhook-MCP Quick Start

## 🚀 5-Minute Setup

### 1. Create .env File (30 seconds)
```bash
cd c:\Users\plgon\Downloads\EasyWebhook-MCP
copy .env.example .env
notepad .env
```

Add your webhooks:
```env
DISCORD_WEBHOOK=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 2. Build Docker Image (1 minute)
```bash
docker build -t easywebhook-mcp-server .
```

### 3. Setup Catalog (2 minutes)
```bash
# Copy the provided catalog
copy custom.yaml $env:USERPROFILE\.docker\mcp\catalogs\custom.yaml

# Update registry
notepad $env:USERPROFILE\.docker\mcp\registry.yaml
```

Add to registry.yaml under `registry:`:
```yaml
  easywebhook:
    ref: ""
```

### 4. Update Claude Config (1 minute)
```bash
notepad $env:APPDATA\Claude\claude_desktop_config.json
```

Ensure the args include:
```json
"--catalog=/mcp/catalogs/custom.yaml",
```

### 5. Restart Claude Desktop (30 seconds)
Quit and restart Claude Desktop completely.

## ✅ Test It

Ask Claude:
> "List my webhooks"

Then try:
> "Send Discord message using DISCORD_WEBHOOK saying 'It works!'"

## 📖 Common Commands

### List Webhooks
> "List my webhooks"
> "Show me configured webhooks"

### Send Discord (by alias)
> "Send Discord message using DISCORD_WEBHOOK: 'Hello!'"
> "Post to DISCORD_ALERTS saying 'System online'"

### Send Slack (by alias)
> "Send to SLACK_WEBHOOK: 'Deployment complete'"
> "Message SLACK_TEAM: 'Meeting in 5 minutes'"

### Send Custom Webhook (by alias)
> "Use MY_API to send {\"status\": \"active\"}"
> "Send to MONITORING webhook: {\"alert\": \"CPU high\"}"

### Direct URL (no .env needed)
> "Send webhook to https://... with payload {\"test\": true}"

## 🎯 Pro Tips

1. **Use descriptive names**: `DISCORD_ALERTS`, `SLACK_DEPLOYMENTS`
2. **Group by purpose**: `PROD_WEBHOOK`, `TEST_WEBHOOK`
3. **Keep .env updated**: Rebuild after changes
4. **Check logs**: `docker ps` then `docker logs [container]`

## 🆘 Troubleshooting

**"No webhook found"**
→ Rebuild: `docker build -t easywebhook-mcp-server .`

**Tools not showing**
→ Restart Claude Desktop completely

**Check if working**
→ `docker mcp server list` should show `easywebhook`

## 📚 Full Documentation

- `SETUP_GUIDE.md` - Detailed setup instructions
- `readme.txt` - Complete feature documentation
- `CLAUDE.md` - Developer implementation guide
- `.env.example` - Configuration template

---

**Ready to send webhooks!** 🎉
