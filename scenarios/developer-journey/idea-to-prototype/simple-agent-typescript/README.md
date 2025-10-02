# Modern Workplace Assistant - TypeScript Sample

This sample demonstrates building enterprise AI agents with Azure AI Foundry, combining SharePoint integration for internal company knowledge with Microsoft Learn MCP integration for external technical guidance.

## 🎯 Business Scenario

The **Modern Workplace Assistant** helps Contoso Corporation employees with:

- **Company Policy Questions**: "What is our remote work security policy?"
- **Technical Implementation**: "How do I configure Azure AD Conditional Access?"  
- **Combined Guidance**: "Our policy requires MFA - how do I implement this in Azure AD?"

This represents realistic enterprise scenarios where employees need both internal requirements and external implementation guidance.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Modern Workplace Assistant                  │
├─────────────────────────────────────────────────────────────┤
│  🤖 Azure AI Foundry Agent (gpt-4o)                       │
│     ├── 📁 SharePoint Tool (Internal Knowledge)           │
│     │   └── Company policies, procedures, governance      │
│     └── 📚 Microsoft Learn MCP (External Knowledge)       │
│         └── Azure docs, best practices, implementation    │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Sample Structure

```
simple-agent-typescript/
├── 📁 src/
│   ├── 🔧 main.ts                      # Core agent implementation (400+ lines)
│   └── 📊 evaluate.ts                  # Business-focused evaluation system  
├── ❓ questions.jsonl                  # Test questions for evaluation
├── 📖 README.md                        # This comprehensive guide
├── ⚙️ .env.template                    # Configuration template
├── 🔨 package.json                     # npm dependencies and scripts
├── 🔧 tsconfig.json                    # TypeScript configuration
├── 📄 SAMPLE_SHAREPOINT_CONTENT.md     # Business documents to upload
└── 🔧 setup_sharepoint.py              # SharePoint document upload utility
```

## 🚀 Quick Start

### 1. Prerequisites

- **Node.js 18+** with npm
- **Azure AI Foundry Project** with SharePoint connection configured
- **Microsoft Learn MCP Server** running (see MCP_SERVERS.md)
- **Azure CLI** authenticated to your tenant

### 2. Installation

Install dependencies:

```bash
npm install
```

### 3. Configuration

Copy the environment template and configure your settings:

```bash
cp .env.template .env
```

Edit `.env` with your specific values:

```properties
# Azure AI Foundry Configuration
PROJECT_ENDPOINT=https://your-project.cognitiveservices.azure.com/
MODEL_DEPLOYMENT_NAME=gpt-4o
AI_FOUNDRY_TENANT_ID=your-tenant-id

# SharePoint Integration  
SHAREPOINT_RESOURCE_NAME=Benefits
SHAREPOINT_SITE_URL=https://yourtenant.sharepoint.com/sites/benefits

# Microsoft Learn MCP Server
MCP_SERVER_URL=https://learn.microsoft.com/api/mcp
```

### 4. SharePoint Document Setup

Upload sample business documents to your SharePoint site:

```bash
# Use the Python setup script (requires Python)
python setup_sharepoint.py

# Or manually upload SAMPLE_SHAREPOINT_CONTENT.md files to:
# https://yourtenant.sharepoint.com/sites/benefits/Shared Documents/
```

**Required Documents:**

1. **Remote Work Security Policy** - Company MFA and security requirements
2. **IT Security Guidelines** - Technical implementation standards  
3. **Employee Handbook** - General policies and procedures
4. **Compliance Requirements** - Governance and regulatory requirements

### 5. Build and Run

```bash
# Build TypeScript to JavaScript
npm run build

# Run the main sample
npm start

# Or run directly with ts-node (development)
npm run dev

# Run evaluation system
npm run evaluate
```

## 🧪 Interactive Testing

The sample includes an interactive mode for testing:

```bash
npm run dev
# Choose 'y' when prompted for interactive mode

# Try these example questions:
❓ What is our company MFA policy?
❓ How do I configure Azure Conditional Access?  
❓ Our policy requires encryption - how do I set this up?
```

## 📊 Evaluation System

Run comprehensive evaluation with business-focused metrics:

```bash
npm run evaluate
```

**Evaluation Dimensions:**

- **Completeness**: Does it answer the full question?
- **Accuracy**: Is the information technically correct?
- **Actionability**: Can users take concrete next steps?
- **Source Integration**: Does it combine internal/external sources?
- **Business Context**: Does it understand enterprise requirements?
- **Performance**: Response time and user experience

## 🔧 Troubleshooting

### SharePoint Connection Issues

If you see `SharePoint connection has invalid target: '_'`:

1. **Check Azure AI Foundry Portal**:
   - Go to Management Center > Connected Resources
   - Edit your SharePoint connection
   - Verify the target URL matches your site

2. **Verify Permissions**:
   - Ensure your Azure identity has access to the SharePoint site
   - Test SharePoint access manually in browser

3. **Connection Name**:
   - Verify `SHAREPOINT_RESOURCE_NAME` matches the connection name exactly
   - Connection names are case-sensitive

### MCP Server Issues

If Microsoft Learn MCP connection fails:

1. **Check Server URL**: Verify `MCP_SERVER_URL` is accessible
2. **Network Access**: Ensure your environment can reach external URLs
3. **Approval Mode**: The sample sets approval mode to "never" for demos

### Authentication Issues

If you see authentication errors:

1. **Azure CLI Login**: Run `az login` and select correct tenant
2. **Tenant ID**: Verify `AI_FOUNDRY_TENANT_ID` matches your Azure AI Foundry tenant
3. **Permissions**: Ensure your identity has AI Foundry access

### TypeScript/Node.js Issues

1. **Node Version**: Ensure Node.js 18+ is installed
2. **Dependencies**: Run `npm install` if you see module not found errors
3. **Build Issues**: Run `npm run build` to compile TypeScript

## 🎓 Educational Value

This sample teaches enterprise AI development patterns:

### **Multi-Source Data Integration**

- Combining internal company knowledge (SharePoint) with external guidance (MCP)
- Dynamic agent capabilities based on available data sources
- Graceful degradation when data sources are unavailable

### **Production-Ready Error Handling**

- Comprehensive diagnostic information during setup
- Clear troubleshooting guidance when connections fail
- User-friendly error messages with actionable solutions

### **Business-Focused Evaluation**

- Evaluation metrics that matter for enterprise deployment
- Assessment of business value, not just technical accuracy
- Foundation for governance and monitoring (Tutorials 2-3)

### **Modern TypeScript Patterns**

- Strong typing with interfaces and type safety
- Async/await patterns throughout
- Modern ES2020+ features and syntax
- Proper module organization and exports

## 🔗 Tutorial Series Context

This is **Tutorial 1** in the Azure AI Foundry enterprise development series:

- **Tutorial 1** (This Sample): Build foundation with SharePoint + MCP integration
- **Tutorial 2**: Add governance, monitoring, and evaluation frameworks  
- **Tutorial 3**: Production deployment, scaling, and operations

## 📚 Key Learning Outcomes

After completing this sample, you'll understand:

✅ **Enterprise AI Agent Architecture**: Multi-source data integration patterns  
✅ **SharePoint Integration**: Internal knowledge access for AI agents  
✅ **MCP Integration**: External knowledge source integration  
✅ **Business Scenario Design**: Realistic enterprise use cases  
✅ **Error Handling**: Production-ready resilience patterns  
✅ **Evaluation Frameworks**: Business-focused quality assessment  
✅ **TypeScript Development**: Modern patterns for enterprise applications  

## 🚀 Next Steps

1. **Customize for Your Business**: Replace sample policies with your actual documents
2. **Extend Agent Capabilities**: Add more tools and data sources
3. **Implement Governance**: Move to Tutorial 2 for monitoring and compliance
4. **Production Deployment**: Use Tutorial 3 for scaling and operations

## 🔍 Code Highlights

### TypeScript Specific Features:

- **Type Safety**: Full TypeScript typing with interfaces and generics
- **Modern Async/Await**: Promise-based patterns throughout
- **ES Modules**: Proper import/export organization
- **Build Pipeline**: TypeScript to JavaScript compilation
- **Development Workflow**: ts-node for rapid development iteration

### Main Features:

- **400+ lines** of comprehensive enterprise AI implementation
- **Educational comments** explaining each business pattern and technical decision
- **Interactive demonstration mode** with 3 realistic business scenarios
- **Robust error handling** with clear troubleshooting guidance
- **Dynamic agent configuration** based on available data sources

This sample provides a complete foundation for building production-ready enterprise AI agents with Azure AI Foundry using TypeScript and Node.js! 🎉