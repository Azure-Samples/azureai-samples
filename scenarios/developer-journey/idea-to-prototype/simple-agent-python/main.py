#!/usr/bin/env python3
"""
Azure AI Foundry Agent Sample - Tutorial 1: Modern Workplace Assistant

This sample demonstrates a complete business scenario combining:
- SharePoint integration for internal company knowledge
- Microsoft Learn MCP integration for external technical guidance  
- Intelligent orchestration of multiple data sources
- Robust error handling and graceful degradation

Educational Focus:
- Enterprise AI patterns with multiple data sources
- Real-world business scenarios that enterprises face daily
- Production-ready error handling and diagnostics
- Foundation for governance, evaluation, and monitoring (Tutorials 2-3)

Business Scenario:
An employee needs to implement Azure AD multi-factor authentication. They need:
1. Company security policy requirements (from SharePoint)
2. Technical implementation steps (from Microsoft Learn)
3. Combined guidance showing how policy requirements map to technical implementation
"""

import os
import time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.ai.agents.models import SharepointTool, McpTool, ToolResources
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# AUTHENTICATION SETUP
# ============================================================================
# Support both default Azure credentials and specific tenant authentication
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
    """
    Create a Modern Workplace Assistant combining internal and external knowledge.
    
    This demonstrates enterprise AI patterns:
    1. Multi-source data integration (SharePoint + MCP)
    2. Robust error handling with graceful degradation
    3. Dynamic agent capabilities based on available resources
    4. Clear diagnostic information for troubleshooting
    
    Educational Value:
    - Shows real-world complexity of enterprise AI systems
    - Demonstrates how to handle partial system failures
    - Provides patterns for combining internal and external data
    
    Returns:
        tuple: (agent, mcp_tool) for further interaction and testing
    """
    
    print("🤖 Creating Modern Workplace Assistant...")
    
    # ========================================================================
    # SHAREPOINT INTEGRATION SETUP
    # ========================================================================
    # SharePoint provides access to internal company knowledge:
    # - Company policies and procedures
    # - Security guidelines and requirements  
    # - Governance and compliance documentation
    # - Internal process documentation
    
    sharepoint_resource_name = os.environ["SHAREPOINT_RESOURCE_NAME"]
    sharepoint_site_url = os.getenv("SHAREPOINT_SITE_URL")
    
    print(f"📁 Configuring SharePoint integration...")
    print(f"   Connection: {sharepoint_resource_name}")
    print(f"   Site URL: {sharepoint_site_url}")
    
    try:
        # Attempt to retrieve pre-configured SharePoint connection
        sharepoint_conn = project_client.connections.get(name=sharepoint_resource_name)
        current_target = getattr(sharepoint_conn, 'target', 'N/A')
        
        # Validate connection configuration (common preview issue)
        if current_target == "_" or not current_target or current_target == "N/A":
            print(f"⚠️  SharePoint connection has invalid target: '{current_target}'")
            print(f"   Expected: {sharepoint_site_url}")
            print("   🔧 SOLUTION: Update connection target in Azure AI Foundry portal")
            print("      1. Go to Management Center > Connected Resources")
            print(f"      2. Edit '{sharepoint_resource_name}' connection")
            print(f"      3. Set target URL to: {sharepoint_site_url}")
            sharepoint_tool = None
        else:
            sharepoint_tool = SharepointTool(connection_id=sharepoint_conn.id)
            print(f"✅ SharePoint successfully connected")
            print(f"   Active target: {current_target}")
            
    except Exception as e:
        # Graceful degradation - system continues without SharePoint
        print(f"⚠️  SharePoint connection failed: {e}")
        print("   Agent will operate in technical guidance mode only")
        print("   📝 To enable full functionality:")
        print("      1. Create SharePoint connection in Azure AI Foundry portal")
        print(f"      2. Connection name: {sharepoint_resource_name}")
        print(f"      3. Site URL: {sharepoint_site_url}")
        sharepoint_tool = None
    
    # ========================================================================
    # MICROSOFT LEARN MCP INTEGRATION SETUP  
    # ========================================================================
    # Microsoft Learn MCP provides access to current technical documentation:
    # - Azure service configuration guides
    # - Best practices and implementation patterns
    # - Troubleshooting and diagnostic information
    # - Latest feature updates and capabilities
    
    print(f"📚 Configuring Microsoft Learn MCP integration...")
    mcp_tool = McpTool(
        server_label="microsoft_learn",
        server_url=os.environ["MCP_SERVER_URL"],
        allowed_tools=[]  # Allow all available tools
    )
    # Disable approval workflow for seamless demonstration
    mcp_tool.set_approval_mode("never")
    print(f"✅ Microsoft Learn MCP connected: {os.environ['MCP_SERVER_URL']}")
    
    # ========================================================================
    # AGENT CREATION WITH DYNAMIC CAPABILITIES
    # ========================================================================
    # Create agent instructions based on available data sources
    # This demonstrates adaptive system design
    
    if sharepoint_tool:
        instructions = """You are a Modern Workplace Assistant for Contoso Corporation.

CAPABILITIES:
- Search SharePoint for company policies, procedures, and internal documentation
- Access Microsoft Learn for current Azure and Microsoft 365 technical guidance
- Provide comprehensive solutions combining internal requirements with external implementation

RESPONSE STRATEGY:
- For policy questions: Search SharePoint for company-specific requirements and guidelines
- For technical questions: Use Microsoft Learn for current Azure/M365 documentation and best practices
- For implementation questions: Combine both sources to show how company policies map to technical implementation
- Always cite your sources and provide step-by-step guidance
- Explain how internal requirements connect to external implementation steps

EXAMPLE SCENARIOS:
- "What is our MFA policy?" → Search SharePoint for security policies
- "How do I configure Azure AD Conditional Access?" → Use Microsoft Learn for technical steps
- "Our policy requires MFA - how do I implement this?" → Combine policy requirements with implementation guidance"""
    else:
        instructions = """You are a Technical Assistant with access to Microsoft Learn documentation.

CAPABILITIES:
- Access Microsoft Learn for current Azure and Microsoft 365 technical guidance
- Provide detailed implementation steps and best practices
- Explain Azure services, features, and configuration options

LIMITATIONS:
- SharePoint integration is not available
- Cannot access company-specific policies or internal documentation
- When asked about company policies, explain that internal document access requires SharePoint configuration

RESPONSE STRATEGY:  
- Provide comprehensive technical guidance from Microsoft Learn
- Include step-by-step implementation instructions
- Reference official documentation and best practices
- Suggest how technical implementations typically align with enterprise requirements"""

    # Create the agent with appropriate tool configuration
    print(f"🛠️  Configuring agent tools...")
    available_tools = (sharepoint_tool.definitions if sharepoint_tool else []) + mcp_tool.definitions
    print(f"   Available tools: {len(available_tools)}")
    
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="Modern Workplace Assistant",
        instructions=instructions,
        tools=available_tools,
    )
    
    print(f"✅ Agent created successfully: {agent.id}")
    return agent, mcp_tool, sharepoint_tool

def demonstrate_business_scenarios(agent, mcp_tool, sharepoint_tool):
    """
    Demonstrate realistic business scenarios combining internal and external knowledge.
    
    This function showcases the practical value of the Modern Workplace Assistant
    by walking through scenarios that enterprise employees face regularly.
    
    Educational Value:
    - Shows real business problems that AI agents can solve
    - Demonstrates integration between internal policies and external guidance
    - Illustrates how AI can bridge the gap between requirements and implementation
    """
    
    scenarios = [
        {
            "title": "📋 Company Policy Question",
            "question": "What is our remote work security policy regarding multi-factor authentication?",
            "context": "Employee needs to understand company MFA requirements",
            "expected_source": "SharePoint",
            "learning_point": "Internal policy retrieval and interpretation"
        },
        {
            "title": "🔧 Technical Implementation Question", 
            "question": "How do I set up Azure Active Directory conditional access policies?",
            "context": "IT administrator needs technical implementation steps",
            "expected_source": "Microsoft Learn MCP",
            "learning_point": "External technical documentation access"
        },
        {
            "title": "🔄 Combined Business Implementation Question",
            "question": "Our company security policy requires multi-factor authentication for remote workers. How do I implement this requirement using Azure AD?",
            "context": "Need to combine policy requirements with technical implementation",
            "expected_source": "Both SharePoint and MCP",
            "learning_point": "Multi-source intelligence combining internal requirements with external implementation"
        }
    ]
    
    print("\n" + "="*70)
    print("🏢 MODERN WORKPLACE ASSISTANT - BUSINESS SCENARIO DEMONSTRATION")  
    print("="*70)
    print("This demonstration shows how AI agents solve real business problems")
    print("by combining internal company knowledge with external technical guidance.")
    print("="*70)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📊 SCENARIO {i}/3: {scenario['title']}")
        print("-" * 50)
        print(f"❓ QUESTION: {scenario['question']}")
        print(f"🎯 BUSINESS CONTEXT: {scenario['context']}")
        print(f"📚 EXPECTED SOURCE: {scenario['expected_source']}")
        print(f"🎓 LEARNING POINT: {scenario['learning_point']}")
        print("-" * 50)
        
        # Get response from the agent
        print("🤖 ASSISTANT RESPONSE:")
        response, status = chat_with_assistant(agent.id, mcp_tool, scenario['question'])
        
        # Display response with analysis
        if status == 'completed' and response and len(response.strip()) > 10:
            print(f"✅ SUCCESS: {response[:300]}...")
            if len(response) > 300:
                print(f"   📏 Full response: {len(response)} characters")
        else:
            print(f"⚠️  LIMITED RESPONSE: {response}")
            if not sharepoint_tool and scenario['expected_source'] in ['SharePoint', 'Both SharePoint and MCP']:
                print("   💡 This demonstrates graceful degradation when SharePoint is unavailable")
        
        print(f"📈 STATUS: {status}")
        print("-" * 50)
    
    print(f"\n✅ DEMONSTRATION COMPLETED!")
    print("🎓 Key Learning Outcomes:")
    print("   • Multi-source data integration in enterprise AI")
    print("   • Robust error handling and graceful degradation")  
    print("   • Real business value through combined intelligence")
    print("   • Foundation for governance and monitoring (Tutorials 2-3)")
    
    return True

def chat_with_assistant(agent_id, mcp_tool, message):
    """
    Execute a conversation with the workplace assistant.
    
    This function demonstrates the conversation pattern for Azure AI Foundry agents
    and includes comprehensive error handling for production readiness.
    
    Educational Value:
    - Shows proper thread management and conversation flow
    - Demonstrates streaming response handling
    - Includes timeout and error management patterns
    """
    
    try:
        # Create conversation thread (maintains conversation context)
        thread = project_client.agents.threads.create()
        
        # Add user message to thread
        project_client.agents.messages.create(
            thread_id=thread.id, 
            role="user", 
            content=message
        )
        
        # Execute the conversation with streaming response
        run = project_client.agents.runs.create_and_stream(
            thread_id=thread.id,
            assistant_id=agent_id,
        )
        
        # Collect streaming response
        response_parts = []
        run_info = None
        
        for event_type, event_data, run_status in run:
            run_info = run_status
            if event_type == 'MessageDelta':
                for content_part in event_data.delta.content:
                    if hasattr(content_part, 'text') and content_part.text.value:
                        response_parts.append(content_part.text.value)
        
        full_response = ''.join(response_parts)
        final_status = run_info.status if run_info else 'unknown'
        
        return full_response, final_status
        
    except Exception as e:
        return f"Error in conversation: {e}", 'failed'

def interactive_mode(agent, mcp_tool):
    """
    Interactive mode for testing the workplace assistant.
    
    This provides a simple interface for users to test the agent with their own questions
    and see how it combines different data sources for comprehensive answers.
    """
    
    print("\n" + "="*60)
    print("💬 INTERACTIVE MODE - Test Your Workplace Assistant!")
    print("="*60)
    print("Ask questions that combine company policies with technical guidance:")
    print("• 'What's our remote work policy for Azure access?'")
    print("• 'How do I configure SharePoint security?'") 
    print("• 'Our policy requires encryption - how do I set this up in Azure?'")
    print("Type 'quit' to exit.")
    print("-" * 60)
    
    while True:
        try:
            question = input("\n❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'bye']:
                break
                
            if not question:
                print("💡 Please ask a question about policies or technical implementation.")
                continue
            
            print(f"\n🤖 Workplace Assistant: ", end="", flush=True)
            response, status = chat_with_assistant(agent.id, mcp_tool, question)
            print(response)
            
            if status != 'completed':
                print(f"\n⚠️  Response status: {status}")
            
            print("-" * 60)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("-" * 60)
    
    print("\n👋 Thank you for testing the Modern Workplace Assistant!")

def main():
    """
    Main execution flow demonstrating the complete sample.
    
    This orchestrates the full demonstration:
    1. Agent creation with diagnostic information
    2. Business scenario demonstration  
    3. Interactive testing mode
    4. Clean completion with next steps
    """
    
    print("🚀 Azure AI Foundry - Modern Workplace Assistant")
    print("Tutorial 1: Building Enterprise Agents with SharePoint + MCP Integration")
    print("="*70)
    
    # Create the agent with full diagnostic output
    agent, mcp_tool, sharepoint_tool = create_workplace_assistant()
    
    # Demonstrate business scenarios  
    demonstrate_business_scenarios(agent, mcp_tool, sharepoint_tool)
    
    # Offer interactive testing
    print(f"\n🎯 Try interactive mode? (y/n): ", end="")
    if input().lower().startswith('y'):
        interactive_mode(agent, mcp_tool)
    
    print(f"\n🎉 Sample completed successfully!")
    print("📚 This foundation supports Tutorial 2 (Governance) and Tutorial 3 (Production)")
    print("🔗 Next: Add evaluation metrics, monitoring, and production deployment")

if __name__ == "__main__":
    main()