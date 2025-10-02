#!/usr/bin/env python3
"""
Azure AI Foundry Agent Sample - Tutorial 1

A minimal sample demonstrating enterprise AI agents with:
- SharePoint integration for internal knowledge
- Microsoft Learn MCP integration for technical guidance
- Combined intelligence for business scenarios

This sample serves as the foundation for Tutorial 2 (Governance & Evaluation) 
and Tutorial 3 (Production & Monitoring).
"""

import os
import time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.ai.agents.models import SharepointTool, McpTool, ToolResources
from dotenv import load_dotenv

load_dotenv()

# Authenticate to Azure AI Foundry
ai_foundry_tenant_id = os.getenv("AI_FOUNDRY_TENANT_ID")
if ai_foundry_tenant_id:
    print(f"🔐 Using AI Foundry tenant: {ai_foundry_tenant_id}")
    credential = AzureCliCredential()
else:
    credential = DefaultAzureCredential()

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=credential,
)

def create_workplace_assistant():
    """Create an AI agent with SharePoint and Microsoft Learn integration"""
    
    print("🤖 Creating Modern Workplace Assistant...")
    
    # Configure SharePoint tool for internal knowledge
    sharepoint_resource_name = os.environ["SHAREPOINT_RESOURCE_NAME"]
    sharepoint_site_url = os.getenv("SHAREPOINT_SITE_URL")
    
    try:
        # Try to get existing connection first
        sharepoint_conn = project_client.connections.get(name=sharepoint_resource_name)
        current_target = getattr(sharepoint_conn, 'target', 'N/A')
        
        # Check if connection has proper target
        if current_target == "_" or not current_target or current_target == "N/A":
            print(f"⚠️  SharePoint connection '{sharepoint_resource_name}' has invalid target: '{current_target}'")
            if sharepoint_site_url:
                print(f"   Expected: {sharepoint_site_url}")
                print("   🔧 SOLUTION: Update connection target in Azure AI Foundry portal")
                print("      1. Go to Management Center > Connected Resources")
                print(f"      2. Edit '{sharepoint_resource_name}' connection")
                print(f"      3. Set target URL to: {sharepoint_site_url}")
            else:
                print("   Set SHAREPOINT_SITE_URL in .env file")
            sharepoint_tool = None
        else:
            sharepoint_tool = SharepointTool(connection_id=sharepoint_conn.id)
            print(f"✅ SharePoint connected: {sharepoint_resource_name}")
            print(f"   Target: {current_target}")
            if sharepoint_site_url and current_target != sharepoint_site_url:
                print(f"   ⚠️  Target mismatch! Expected: {sharepoint_site_url}")
                
    except Exception as e:
        print(f"⚠️  SharePoint connection '{sharepoint_resource_name}' not found")
        print(f"   Error: {e}")
        print("   � SOLUTION: Create SharePoint connection in Azure AI Foundry portal")
        print("      1. Management Center > Connected Resources > Add SharePoint")
        print(f"      2. Connection name: {sharepoint_resource_name}")
        if sharepoint_site_url:
            print(f"      3. Site URL: {sharepoint_site_url}")
        else:
            print("      3. Site URL: Set SHAREPOINT_SITE_URL in .env file")
        sharepoint_tool = None
    
    # Configure Microsoft Learn MCP tool for technical guidance
    mcp_tool = McpTool(
        server_label="microsoft_learn",
        server_url=os.environ["MCP_SERVER_URL"],
        allowed_tools=[]
    )
    mcp_tool.set_approval_mode("never")  # Enable seamless experience
    
    # Combine tool resources
    tool_resources = {}
    if sharepoint_tool and hasattr(sharepoint_tool, 'resources') and sharepoint_tool.resources:
        tool_resources.update(sharepoint_tool.resources)
    if hasattr(mcp_tool, 'resources') and mcp_tool.resources:
        tool_resources.update(mcp_tool.resources)
    
    # Create dynamic instructions based on available tools
    if sharepoint_tool:
        instructions = """You are a Modern Workplace Assistant for Contoso Corp.

Your capabilities:
- Search SharePoint for company policies, procedures, and internal documents
- Access Microsoft Learn for current Azure and Microsoft 365 technical guidance
- Provide comprehensive answers combining internal policies with implementation guidance

When responding:
- For policy questions: Search SharePoint for company documents
- For technical questions: Use Microsoft Learn for current Azure/M365 guidance  
- For implementation questions: Combine both sources to show policy requirements AND technical steps
- Always cite your sources and provide actionable guidance"""
    else:
        instructions = """You are a Technical Assistant with access to Microsoft Learn documentation.

Your capabilities:
- Access Microsoft Learn for current Azure and Microsoft 365 technical guidance
- Provide detailed technical implementation steps and best practices

Note: SharePoint integration is not configured. You can only provide technical guidance from Microsoft Learn.
When users ask about company policies, explain that SharePoint integration needs to be configured."""

    # Create the agent
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="Modern Workplace Assistant",
        instructions=instructions,
        tools=(sharepoint_tool.definitions if sharepoint_tool else []) + mcp_tool.definitions,
        tool_resources=ToolResources(**tool_resources) if tool_resources else None
    )
    
    print(f"✅ Agent created: {agent.id}")
    return agent, mcp_tool

def chat_with_assistant(agent_id, mcp_tool, message):
    """Send a message to the workplace assistant and get a response"""
    
    # Create conversation thread
    thread = project_client.agents.threads.create()
    project_client.agents.messages.create(thread_id=thread.id, role="user", content=message)
    
    # Run the agent with both SharePoint and MCP tools
    run = project_client.agents.runs.create(
        thread_id=thread.id,
        agent_id=agent_id,
        tool_resources=mcp_tool.resources
    )
    
    # Wait for completion
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)
    
    # Get the response
    messages = list(project_client.agents.messages.list(thread_id=thread.id))
    for msg in messages:
        if msg.role.value == "assistant" and msg.content:
            return msg.content[0].text.value
    
    return f"No response received (Status: {run.status})"

def run_sample_demo():
    """Demonstrate the workplace assistant with sample business scenarios"""
    
    print("🏢 Modern Workplace Assistant Demo")
    print("="*50)
    
    # Create the assistant
    agent, mcp_tool = create_workplace_assistant()
    
    # Sample business scenarios that demonstrate both data sources
    scenarios = [
        {
            "type": "📋 Policy Question",
            "question": "What is our remote work policy regarding security requirements?",
            "note": "Should search SharePoint for company policies"
        },
        {
            "type": "🔧 Technical Question", 
            "question": "How do I set up Azure Active Directory conditional access?",
            "note": "Should use Microsoft Learn documentation"
        },
        {
            "type": "🔄 Implementation Question", 
            "question": "Our security policy requires multi-factor authentication - how do I implement this in Azure AD?",
            "note": "Should combine internal policy with Azure implementation guidance"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{scenario['type']} {i}/3")
        print(f"❓ {scenario['question']}")
        print(f"💡 {scenario['note']}")
        print("-" * 50)
        
        response = chat_with_assistant(agent.id, mcp_tool, scenario['question'])
        
        # Show response preview
        preview = response[:300] + "..." if len(response) > 300 else response
        print(f"🤖 {preview}")
        print("-" * 50)
    
    print(f"\n✅ Demo completed! The assistant successfully handled {len(scenarios)} business scenarios.")
    return agent, mcp_tool

def interactive_mode(agent, mcp_tool):
    """Interactive chat mode for testing the workplace assistant"""
    
    print(f"\n💬 Interactive Mode - Ask Your Workplace Questions!")
    print("="*50)
    print("Try questions about:")
    print("• Company policies and procedures (uses SharePoint)")
    print("• Azure/Microsoft 365 technical guidance (uses Microsoft Learn)")  
    print("• Implementation scenarios (combines both sources)")
    print("Type 'quit' to exit.\n")
    
    while True:
        question = input("❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
        elif not question:
            continue
        
        response = chat_with_assistant(agent.id, mcp_tool, question)
        print(f"\n🤖 Workplace Assistant: {response}\n")
        print("-" * 60)

def main():
    """Main function to run the workplace assistant sample"""
    
    print("🚀 Azure AI Foundry - Modern Workplace Assistant")
    print("Tutorial 1: Building Enterprise Agents with SharePoint + MCP Integration")
    print("="*70)
    
    try:
        # Run demonstration
        agent, mcp_tool = run_sample_demo()
        
        # Offer interactive mode
        choice = input("\n🎯 Try interactive mode? (y/n): ").lower()
        if choice in ['y', 'yes']:
            interactive_mode(agent, mcp_tool)
        
        print("\n🎉 Sample completed successfully!")
        print("📚 This foundation supports Tutorial 2 (Governance) and Tutorial 3 (Production)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Setup Help:")
        print("1. Verify your .env configuration matches .env.template")
        print("2. Ensure SharePoint connection is configured in Azure AI Foundry portal")
        print("3. Run 'python setup_sharepoint.py' for detailed setup guidance")

if __name__ == "__main__":
    main()