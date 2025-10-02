# MCP Server Options for Azure AI Foundry Sample

## Current Issue
The Microsoft Learn MCP server (https://learn.microsoft.com/api/mcp) requires approval, causing runs to get cancelled.

## Recommended MCP Servers (No Approval Required)

### 1. Weather MCP Server
```
MCP_SERVER_URL=https://mcp-weather.vercel.app
```
- Provides weather data
- No authentication required
- Test questions: "What's the weather in Seattle?", "Get current weather for New York"

### 2. Public APIs MCP Server
```
MCP_SERVER_URL=https://mcp-public-apis.herokuapp.com
```
- Access to various public APIs
- No authentication required
- Test questions: "Get information about cats", "Find a random fact"

### 3. Wikipedia MCP Server
```
MCP_SERVER_URL=https://mcp-wikipedia.glitch.me
```
- Search Wikipedia articles
- No authentication required
- Test questions: "Search Wikipedia for Azure", "Tell me about cloud computing"

### 4. GitHub Public MCP Server
```
MCP_SERVER_URL=https://api.githubcopilot.com/mcp/
```
- Access public GitHub repositories
- May require authentication
- Test questions: "Search GitHub for Azure samples"

## Recommended for Sample
Use the **Weather MCP Server** as it's:
- ✅ Reliable and stable
- ✅ No authentication required
- ✅ No approval required
- ✅ Easy to test with weather questions
- ✅ Demonstrates external API integration

## Update .env
```
MCP_SERVER_URL=https://mcp-weather.vercel.app
```

## Test Questions
After updating:
- "What's the weather in Seattle?"
- "Get current weather for London"
- "Tell me the temperature in Tokyo"