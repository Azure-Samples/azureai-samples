# Azure AI Foundry - Modern Workplace Assistant

**Tutorial 1** of the Azure AI Foundry enterprise tutorial series. This sample demonstrates how to build AI agents that combine internal knowledge (SharePoint) with external technical guidance (Microsoft Learn) for realistic business scenarios.

> **🚀 Preview SDK**: This sample uses preview versions of the Azure AI SDK. These features will be GA at Microsoft Ignite.

## 🎯 Business Scenario: Modern Workplace Assistant

This sample creates an AI assistant that helps employees with:
- **Company policies** (from SharePoint documents)
- **Technical implementation** (from Microsoft Learn)
- **Complete solutions** (combining both sources)

**Example Questions:**
- "What is our remote work security policy?" → *Uses SharePoint*
- "How do I set up Azure AD conditional access?" → *Uses Microsoft Learn*  
- "Our policy requires MFA - how do I implement it in Azure?" → *Uses both sources*

## � Quick Start

### 1. Run the Main Sample

```bash
python main.py
```

This demonstrates the core functionality with sample business scenarios.

### 2. Run Evaluation

```bash
python evaluate.py
```

Tests the agent with predefined questions and measures quality.

## 📁 Ultra-Minimal Sample Structure

This sample contains only **10 essential files** - nothing extraneous:

### Core Sample (3 files)

- **`main.py`** - Complete Modern Workplace Assistant (148 lines)
- **`evaluate.py`** - Business evaluation framework (54 lines)
- **`questions.jsonl`** - Business test scenarios (4 questions)

### Setup & Documentation (7 files)

- **`requirements.txt`** - Python dependencies
- **`.env.template`** - Environment variables template
- **`setup_sharepoint.py`** - SharePoint diagnostic tool
- **`MCP_SERVERS.md`** - MCP server configuration guide
- **`SAMPLE_SHAREPOINT_CONTENT.md`** - Sample business documents
- **`README.md`** - Complete setup instructions
- **`.env`** - Your actual configuration (create from template)

## 📁 SharePoint Business Documents Setup

To demonstrate the complete business scenario, you need to upload sample documents to your SharePoint site. The sample includes realistic Contoso Corp business documents that create scenarios where employees need both company policy information and technical implementation guidance.

### Step 1: Prepare Your SharePoint Site

1. **Navigate to your SharePoint site** (the one configured in your Azure AI Foundry SharePoint connection)
2. **Create or use a document library** called "Company Policies" or use the default "Documents" library
3. **Ensure you have edit permissions** to upload documents

### Step 2: Create Sample Business Documents

The `SAMPLE_SHAREPOINT_CONTENT.md` file contains four realistic business documents. Create these as Word documents (.docx) in your SharePoint site:

#### 📄 Document 1: `remote-work-policy.docx`
**Content**: Remote work security requirements including VPN usage, MFA requirements, device compliance, and data access policies. References Azure AD and Microsoft 365 security features.

#### 📄 Document 2: `security-guidelines.docx`  
**Content**: Azure security standards including conditional access policies, identity governance, and compliance requirements. Establishes company standards for Azure resource security.

#### 📄 Document 3: `collaboration-standards.docx`
**Content**: Microsoft Teams and SharePoint usage policies, including data sharing guidelines, external collaboration rules, and communication standards.

#### 📄 Document 4: `data-governance-policy.docx`
**Content**: Data classification, retention policies, and governance requirements for Azure and Microsoft 365 data. Includes sensitivity labels and compliance procedures.

### Step 3: Upload Documents to SharePoint

1. **For each document in `SAMPLE_SHAREPOINT_CONTENT.md`**:
   - Create a new Word document in SharePoint
   - Copy the content from the corresponding section  
   - Save with the specified filename (e.g., `remote-work-policy.docx`)

2. **Verify document access**:
   - Ensure documents are searchable
   - Check that your Azure AI Foundry connection can access the site
   - Test that documents appear in SharePoint search results

### Why These Documents Matter

These sample documents create realistic business scenarios:

- **"What is our remote work security policy?"** → Searches `remote-work-policy.docx`
- **"How do I set up Azure AD conditional access?"** → Uses Microsoft Learn MCP
- **"Our policy requires MFA - how do I implement it in Azure?"** → Combines both sources

This demonstrates how modern workplace assistants help employees by connecting company policies with technical implementation guidance.

## 🚀 Quick Start (5 minutes)

### Step 1: Prerequisites Check

Make sure you have:

- [x] **Azure AI Foundry project** with a deployed model (e.g., `gpt-4o-mini`)
- [x] **Python 3.10+** installed (`python --version`)
- [x] **SharePoint connection** configured in your Azure AI Foundry project
- [x] **MCP server endpoint** (or use a placeholder for testing)
- [x] **Azure CLI** authenticated (`az login`)

### Step 2: Environment Setup

1. **Copy the environment template:**

   ```bash
   cp .env.template .env
   ```

2. **Edit `.env` with your actual values:**

   ```bash
   PROJECT_ENDPOINT=https://your-project.aiservices.azure.com
   MODEL_DEPLOYMENT_NAME=gpt-4o-mini
   SHAREPOINT_RESOURCE_NAME=your-sharepoint-connection
   SHAREPOINT_SITE_URL=https://your-company.sharepoint.com/teams/your-site
   MCP_SERVER_URL=https://your-mcp-server.com
   ```

3. **Install dependencies (with preview features):**

   ```bash
   pip install --pre -r requirements.txt
   ```

### Step 3: Test Single Agent

Run the main agent script:

```bash
python main.py
```

**Expected output:**

```text
Created agent: <agent-id>
SharePoint Response: <response about your remote work policy>
```

> **Note**: You'll get a "Resource not found" error until you configure actual SharePoint and MCP connections in Azure AI Foundry.

### Step 4: Test Multi-Agent System

In Python interactive mode:

```python
from agent import test_multi_agent
test_multi_agent()
```

**Expected output:**

```text
Multi-agent system: Main <main-id>, Research <research-id>
Multi-agent response: <delegated research response>
```

### Step 5: Run Evaluation

Evaluate your agent with test questions:

```bash
python eval.py <agent-id-from-step-3>
```

**Expected output:**

```json
Evaluation: 3/4 passed
[
  {
    "question": "What's our remote work policy?",
    "response": "According to SharePoint...",
    "contains_expected": true
  }
  ...
]
```

## 🔧 Troubleshooting

### Common Issues

#### Authentication failed

- Run `az login` and ensure you're logged into the correct tenant
- Verify your `PROJECT_ENDPOINT` is correct

#### SharePoint Connection Issues

**🔍 The Problem**: SharePoint connections are tied to individual agents in the portal, but this sample creates agents programmatically.

**🔧 The Solutions**:

**Option 1: Fix Existing Connection (Recommended)**
1. Go to [Azure AI Foundry portal](https://ai.azure.com) → Your Project
2. **Management Center** → **Connected Resources** 
3. Find your SharePoint connection (e.g., "Documentor")
4. **Edit** the connection and update **Target URL** from `_` to your actual site
5. Use format: `https://company.sharepoint.com/teams/site-name`

**Option 2: Create Fresh Connection**
- **Management Center** → **Connected Resources** → **Add SharePoint**
- Connection name: Match your `SHAREPOINT_RESOURCE_NAME` in `.env`
- Site URL: Your actual SharePoint site
- Update `.env` with new connection name if different

**Option 3: MCP-Only Mode**
- Comment out SharePoint variables in `.env`
- Sample works perfectly with just Microsoft Learn integration

#### MCP server unreachable

- For testing, you can comment out MCP tool lines in `agent.py`
- Or use a mock endpoint: `https://httpbin.org/json`

#### Model deployment not found

- Verify your `MODEL_DEPLOYMENT_NAME` matches exactly what's deployed
- Check Azure AI Foundry portal → Models → Deployments

### Debug Mode

Add debug logging to see what's happening:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Understanding the Code

### `agent.py` - Main Agent Logic

- **`create_single_agent()`**: Creates an agent with SharePoint + MCP tools
- **`create_multi_agent()`**: Creates connected agents for delegation
- **`chat_with_agent()`**: Handles conversations with memory persistence
- **`test_multi_agent()`**: Demonstrates agent-to-agent communication

### `eval.py` - Quality Assessment

- **`run_evaluation()`**: Batch tests agent responses against expected keywords
- Uses `questions.jsonl` as test data
- Provides pass/fail summary with detailed results

### `questions.jsonl` - Test Dataset

Each line is a JSON object with:

- **`question`**: What to ask the agent
- **`expected`**: Keyword that should appear in the response

## 🚀 Deploy to Azure AI Foundry

### Option 1: Portal Deployment

1. Go to [Azure AI Foundry](https://ai.azure.com)
2. Navigate to your project → **Agents**
3. Click **+ Create** → **Import from code**
4. Upload your `agent.py` file
5. Configure deployment settings
6. Click **Deploy**

### Option 2: CLI Deployment

```bash
# Install Azure AI CLI extension
az extension add --name azure-ai

# Deploy agent
az ai agent create --file agent.py --project <project-name>
```

### Get Share Link

After deployment:

1. Go to **Agents** → Your deployed agent
2. Click **Share** → **Create public link**
3. Test with friends/colleagues!

## 🎓 Learning Path

**Completed this sample?** Here's what to explore next:

1. **Add more tools**: Azure AI Search, Bing Web Search, Function Calling
2. **Advanced evaluation**: Custom metrics, A/B testing, human feedback
3. **Production setup**: Monitoring, logging, error handling
4. **Scale up**: RAG with vector stores, complex multi-agent workflows

## 📚 Resources

- [Azure AI Foundry Documentation](https://docs.microsoft.com/azure/ai-foundry)
- [Agent Service Overview](https://docs.microsoft.com/azure/ai-foundry/agents)
- [SharePoint Tool Guide](https://docs.microsoft.com/azure/ai-foundry/agents/tools/sharepoint)
- [MCP Integration](https://docs.microsoft.com/azure/ai-foundry/agents/tools/mcp)

## 🤝 Support

**Questions?**

- Check the [troubleshooting section](#-troubleshooting) above
- Review the [full tutorial](https://docs.microsoft.com/azure/ai-foundry/tutorials/developer-journey-stage-1)
- File issues in the Azure AI Foundry feedback portal

---

**Happy coding!** 🎉 This sample gets you from zero to working enterprise agent in minutes.
