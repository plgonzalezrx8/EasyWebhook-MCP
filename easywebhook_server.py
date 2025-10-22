#!/usr/bin/env python3
"""
Simple EasyWebhook MCP Server - Send webhooks to any HTTP endpoint
"""
import os
import sys
import logging
import json
from datetime import datetime, timezone
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("easywebhook-server")

# Load environment variables from .env file
load_dotenv()

# Initialize MCP server - NO PROMPT PARAMETER!
mcp = FastMCP("easywebhook")

# === UTILITY FUNCTIONS ===

def get_webhook_url(alias: str = "") -> str:
    """Get webhook URL from environment variable by alias."""
    if not alias.strip():
        return ""
    
    # Try direct match first (e.g., DISCORD_WEBHOOK)
    url = os.getenv(alias.upper())
    if url:
        return url
    
    # Try with WEBHOOK_ prefix (e.g., WEBHOOK_DISCORD)
    url = os.getenv(f"WEBHOOK_{alias.upper()}")
    if url:
        return url
    
    return ""

def list_stored_webhooks() -> str:
    """List all webhook aliases stored in environment variables."""
    webhooks = []
    
    for key, value in os.environ.items():
        # Look for variables that contain webhook URLs
        if "WEBHOOK" in key.upper() and value.startswith(("http://", "https://")):
            # Mask the URL for security
            masked_url = value[:30] + "..." if len(value) > 30 else value
            webhooks.append(f"  • {key}: {masked_url}")
    
    return webhooks

def format_headers(headers_str: str = ""):
    """Parse headers from string format to dictionary."""
    if not headers_str.strip():
        return {}
    
    headers = {}
    try:
        # Support JSON format
        if headers_str.strip().startswith("{"):
            headers = json.loads(headers_str)
        else:
            # Support key:value format, one per line or comma-separated
            pairs = headers_str.replace(",", "\n").split("\n")
            for pair in pairs:
                if ":" in pair:
                    key, value = pair.split(":", 1)
                    headers[key.strip()] = value.strip()
    except Exception as e:
        logger.warning(f"Could not parse headers: {e}")
    
    return headers

def format_payload(payload_str: str = ""):
    """Parse payload from string format."""
    if not payload_str.strip():
        return {}
    
    try:
        # Try to parse as JSON
        return json.loads(payload_str)
    except json.JSONDecodeError:
        # If not JSON, return as text
        return {"content": payload_str}

def parse_color(color_str: str = "") -> int:
    """Parse color from hex or decimal string to decimal integer."""
    if not color_str.strip():
        return None
    
    color = color_str.strip()
    
    try:
        # If it starts with # or is 6 hex chars, treat as hex
        if color.startswith("#"):
            color = color[1:]
        
        if len(color) == 6 and all(c in '0123456789ABCDEFabcdef' for c in color):
            return int(color, 16)
        
        # Otherwise try as decimal
        return int(color)
    except ValueError:
        return None

def build_discord_embed(message: str = "", title: str = "", color: str = ""):
    """Build Discord embed from message, title, and color."""
    # Try to parse message as JSON embed first
    if message.strip().startswith("{"):
        try:
            embed_data = json.loads(message)
            # If it has embed fields, use it as-is
            if any(key in embed_data for key in ["title", "description", "fields", "color"]):
                return embed_data
        except json.JSONDecodeError:
            pass
    
    # Build embed from components
    embed = {}
    
    if title.strip():
        embed["title"] = title.strip()
    
    if message.strip():
        embed["description"] = message.strip()
    
    # Parse color if provided
    parsed_color = parse_color(color)
    if parsed_color is not None:
        embed["color"] = parsed_color
    
    return embed

# === MCP TOOLS ===

@mcp.tool()
async def send_webhook(webhook_url: str = "", payload: str = "", headers: str = "", method: str = "POST") -> str:
    """Send a webhook request to any HTTP endpoint with custom payload and headers."""
    logger.info(f"Sending webhook to {webhook_url}")
    
    # Validate webhook URL
    if not webhook_url.strip():
        return "❌ Error: webhook_url is required"
    
    if not webhook_url.startswith("http://") and not webhook_url.startswith("https://"):
        return "❌ Error: webhook_url must start with http:// or https://"
    
    # Validate and normalize method
    method = method.strip().upper()
    if method not in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        return f"❌ Error: Invalid HTTP method '{method}'. Supported: GET, POST, PUT, PATCH, DELETE"
    
    # Parse payload and headers
    parsed_payload = format_payload(payload)
    parsed_headers = format_headers(headers)
    
    # Set default content-type if not provided
    if "Content-Type" not in parsed_headers and "content-type" not in parsed_headers:
        parsed_headers["Content-Type"] = "application/json"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Send request based on method
            if method == "GET":
                response = await client.get(webhook_url, headers=parsed_headers)
            elif method == "POST":
                response = await client.post(webhook_url, json=parsed_payload, headers=parsed_headers)
            elif method == "PUT":
                response = await client.put(webhook_url, json=parsed_payload, headers=parsed_headers)
            elif method == "PATCH":
                response = await client.patch(webhook_url, json=parsed_payload, headers=parsed_headers)
            elif method == "DELETE":
                response = await client.delete(webhook_url, headers=parsed_headers)
            
            # Log response
            logger.info(f"Response status: {response.status_code}")
            
            # Check response status
            if 200 <= response.status_code < 300:
                response_preview = response.text[:200] if response.text else "No content"
                return f"✅ Webhook sent successfully!\n\n📊 Status: {response.status_code}\n🌐 URL: {webhook_url}\n⚡ Method: {method}\n\n📄 Response:\n{response_preview}"
            else:
                error_body = response.text[:200] if response.text else "No error message"
                return f"⚠️ Webhook sent but received non-success status\n\n📊 Status: {response.status_code}\n🌐 URL: {webhook_url}\n\n❌ Response:\n{error_body}"
                
    except httpx.TimeoutException:
        logger.error("Webhook request timed out")
        return f"⏱️ Error: Request timed out after 30 seconds\n🌐 URL: {webhook_url}"
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        return f"❌ HTTP Error: {e.response.status_code}\n🌐 URL: {webhook_url}\n\n{str(e)}"
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        return f"❌ Network Error: Could not reach webhook URL\n🌐 URL: {webhook_url}\n\n{str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def send_webhook_by_alias(alias: str = "", payload: str = "", headers: str = "", method: str = "POST") -> str:
    """Send a webhook using a stored alias from .env file with custom payload and headers."""
    logger.info(f"Sending webhook using alias: {alias}")
    
    # Validate alias
    if not alias.strip():
        return "❌ Error: alias is required"
    
    # Get webhook URL from environment
    webhook_url = get_webhook_url(alias.strip())
    
    if not webhook_url:
        return f"❌ Error: No webhook found for alias '{alias}'. Check your .env file."
    
    # Use the existing send_webhook function
    return await send_webhook(webhook_url, payload, headers, method)

@mcp.tool()
async def send_discord_webhook_by_alias(alias: str = "", message: str = "", title: str = "", color: str = "", username: str = "", avatar_url: str = "") -> str:
    """Send a Discord embed message using a stored webhook alias from .env file with optional title, color, username and avatar."""
    logger.info(f"Sending Discord webhook using alias: {alias}")
    
    # Validate inputs
    if not alias.strip():
        return "❌ Error: alias is required"
    
    if not message.strip():
        return "❌ Error: message is required"
    
    # Get webhook URL from environment
    webhook_url = get_webhook_url(alias.strip())
    
    if not webhook_url:
        return f"❌ Error: No webhook found for alias '{alias}'. Check your .env file."
    
    # Use the existing discord webhook function
    return await send_discord_webhook(webhook_url, message, title, color, username, avatar_url)

@mcp.tool()
async def send_slack_webhook_by_alias(alias: str = "", message: str = "") -> str:
    """Send a Slack message using a stored webhook alias from .env file."""
    logger.info(f"Sending Slack webhook using alias: {alias}")
    
    # Validate inputs
    if not alias.strip():
        return "❌ Error: alias is required"
    
    if not message.strip():
        return "❌ Error: message is required"
    
    # Get webhook URL from environment
    webhook_url = get_webhook_url(alias.strip())
    
    if not webhook_url:
        return f"❌ Error: No webhook found for alias '{alias}'. Check your .env file."
    
    # Use the existing slack webhook function
    return await send_slack_webhook(webhook_url, message)

@mcp.tool()
async def list_webhooks() -> str:
    """List all webhook aliases configured in the .env file."""
    logger.info("Listing stored webhooks")
    
    webhooks = list_stored_webhooks()
    
    if not webhooks:
        return "📭 No webhooks found in .env file.\n\nTo add webhooks, create a .env file with entries like:\nDISCORD_WEBHOOK=https://discord.com/api/webhooks/...\nSLACK_WEBHOOK=https://hooks.slack.com/services/..."
    
    webhook_list = "\n".join(webhooks)
    return f"📋 Stored Webhooks:\n\n{webhook_list}\n\nUse these aliases with the *_by_alias tools."

@mcp.tool()
async def send_discord_webhook(webhook_url: str = "", message: str = "", title: str = "", color: str = "", username: str = "", avatar_url: str = "") -> str:
    """Send an embed message to Discord using a Discord webhook URL with optional title, color, username and avatar."""
    logger.info(f"Sending Discord webhook with embed")
    
    # Validate inputs
    if not webhook_url.strip():
        return "❌ Error: webhook_url is required"
    
    if not message.strip():
        return "❌ Error: message is required"
    
    if "discord.com/api/webhooks/" not in webhook_url:
        return "❌ Error: This doesn't appear to be a valid Discord webhook URL"
    
    # Build embed
    embed = build_discord_embed(message, title, color)
    
    if not embed:
        return "❌ Error: Could not create embed from message"
    
    # Build Discord payload with embed
    discord_payload = {
        "embeds": [embed]
    }
    
    if username.strip():
        discord_payload["username"] = username.strip()
    
    if avatar_url.strip():
        discord_payload["avatar_url"] = avatar_url.strip()
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                webhook_url,
                json=discord_payload,
                headers={"Content-Type": "application/json"}
            )
            
            logger.info(f"Discord response status: {response.status_code}")
            
            if response.status_code == 204 or response.status_code == 200:
                preview = message[:100] if len(message) <= 100 else message[:100] + "..."
                result = f"✅ Discord embed sent successfully!\n\n💬 Message: {preview}"
                if title.strip():
                    result += f"\n📌 Title: {title.strip()}"
                if username.strip():
                    result += f"\n👤 Username: {username.strip()}"
                return result
            else:
                error_body = response.text[:200] if response.text else "No error message"
                return f"⚠️ Discord webhook failed\n\n📊 Status: {response.status_code}\n\n❌ Response:\n{error_body}"
                
    except httpx.TimeoutException:
        logger.error("Discord webhook timed out")
        return "⏱️ Error: Request timed out after 30 seconds"
    except Exception as e:
        logger.error(f"Error sending Discord webhook: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def send_slack_webhook(webhook_url: str = "", message: str = "") -> str:
    """Send a message to Slack using a Slack webhook URL."""
    logger.info(f"Sending Slack webhook")
    
    # Validate inputs
    if not webhook_url.strip():
        return "❌ Error: webhook_url is required"
    
    if not message.strip():
        return "❌ Error: message is required"
    
    if "hooks.slack.com" not in webhook_url:
        return "❌ Error: This doesn't appear to be a valid Slack webhook URL"
    
    # Build Slack payload
    slack_payload = {
        "text": message.strip()
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                webhook_url,
                json=slack_payload,
                headers={"Content-Type": "application/json"}
            )
            
            logger.info(f"Slack response status: {response.status_code}")
            
            if response.status_code == 200:
                return f"✅ Slack message sent successfully!\n\n💬 Message: {message[:100]}{'...' if len(message) > 100 else ''}"
            else:
                error_body = response.text[:200] if response.text else "No error message"
                return f"⚠️ Slack webhook failed\n\n📊 Status: {response.status_code}\n\n❌ Response:\n{error_body}"
                
    except httpx.TimeoutException:
        logger.error("Slack webhook timed out")
        return "⏱️ Error: Request timed out after 30 seconds"
    except Exception as e:
        logger.error(f"Error sending Slack webhook: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting EasyWebhook MCP server...")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
