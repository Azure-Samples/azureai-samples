#!/usr/bin/env python3
"""
SharePoint Connection Setup Guide and Diagnostic Tool
Helps configure SharePoint for the tutorial series foundation.
"""

import os
from agent import project_client
from dotenv import load_dotenv

load_dotenv()

def check_sharepoint_connection_detailed():
    """Get detailed SharePoint connection information"""
    
    print("🔍 SharePoint Connection Analysis")
    print("="*50)
    
    try:
        connection_name = os.environ["SHAREPOINT_RESOURCE_NAME"]
        conn = project_client.connections.get(name=connection_name)
        
        print(f"✅ Connection Found: {conn.name}")
        print(f"🆔 ID: {conn.id}")
        print(f"🏷️  Type: {conn.type}")
        print(f"📋 Metadata: {conn.metadata}")
        print(f"🔐 Credentials: {conn.credentials}")
        print(f"🎯 Target: {conn.target}")
        print(f"🔧 Is Default: {conn.is_default}")
        
        # Analyze the issue
        if conn.target == "_":
            print(f"\n❌ ISSUE IDENTIFIED: SharePoint site URL is not configured")
            print(f"   The 'target' field should contain your SharePoint site URL")
            print(f"   Current value: '{conn.target}'")
            return False
        else:
            print(f"\n✅ SharePoint site URL is configured: {conn.target}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def provide_sharepoint_setup_instructions():
    """Provide step-by-step SharePoint setup instructions"""
    
    print(f"\n🛠️  SHAREPOINT CONNECTION SETUP GUIDE")
    print("="*50)
    
    print("To fix the SharePoint connection for this tutorial series:")
    
    print(f"\n1️⃣  **Go to Azure AI Foundry Portal:**")
    print("   - Navigate to https://ai.azure.com")
    print("   - Sign in with your Azure account")
    print("   - Select your AI Foundry project")
    
    print(f"\n2️⃣  **Configure SharePoint Connection:**")
    print("   - Go to 'Settings' > 'Connections'")
    print("   - Find your 'Documentor' connection")
    print("   - Click 'Edit' or 'Configure'")
    
    print(f"\n3️⃣  **Set SharePoint Site URL:**")
    print("   - Enter your SharePoint site URL in format:")
    print("     • https://[tenant].sharepoint.com/sites/[sitename]")
    print("     • Example: https://contoso.sharepoint.com/sites/documents")
    print("   - OR use root site: https://[tenant].sharepoint.com")
    
    print(f"\n4️⃣  **Verify Authentication:**")
    print("   - Ensure the connection has proper permissions")
    print("   - Test the connection in the portal")
    print("   - Make sure your Azure AI service can access SharePoint")
    
    print(f"\n5️⃣  **Alternative: Use Microsoft 365 Developer Tenant:**")
    print("   - Get free access: https://developer.microsoft.com/microsoft-365/dev-program")
    print("   - Includes SharePoint Online with sample data")
    print("   - Perfect for tutorials and development")
    
    print(f"\n💡 **For Tutorial Series Success:**")
    print("   This SharePoint connection will be used across all 3 tutorials for:")
    print("   • Evaluation datasets (Tutorial 2)")
    print("   • Red-teaming scenarios (Tutorial 2)")  
    print("   • Production monitoring data (Tutorial 3)")
    print("   • AI gateway integration (Tutorial 3)")

def suggest_sharepoint_content_structure():
    """Suggest SharePoint content structure for the tutorial series"""
    
    print(f"\n📁 RECOMMENDED SHAREPOINT CONTENT STRUCTURE")
    print("="*50)
    print("For maximum tutorial effectiveness, organize your SharePoint with:")
    
    print(f"\n📂 **Document Libraries:**")
    print("   • 'Shared Documents' - Main content library")
    print("   • 'Policies' - Company policies and guidelines")
    print("   • 'Projects' - Project documentation")
    print("   • 'Training Materials' - Learning resources")
    
    print(f"\n📄 **Sample Documents to Add:**")
    print("   • Remote work policy document")
    print("   • Employee handbook")
    print("   • Project status reports")
    print("   • Technical documentation")
    print("   • Meeting notes and minutes")
    
    print(f"\n🎯 **Why This Helps the Tutorial Series:**")
    print("   • Tutorial 1: Agent can find and discuss real content")
    print("   • Tutorial 2: Realistic evaluation scenarios with actual data")
    print("   • Tutorial 3: Production-like monitoring with meaningful content")

def test_sharepoint_once_fixed():
    """Provide a test script for once SharePoint is fixed"""
    
    print(f"\n🧪 TEST SCRIPT (Run After Fixing SharePoint)")
    print("="*50)
    
    test_script = '''
# Save this as test_fixed_sharepoint.py and run after fixing the connection:

from agent import create_single_agent, project_client, create_mcp_tool
from azure.ai.agents.models import SharepointTool
import time
import os

def test_real_sharepoint():
    """Test SharePoint with real connection"""
    
    # Create SharePoint-only agent
    sharepoint_conn = project_client.connections.get(name=os.environ["SHAREPOINT_RESOURCE_NAME"])
    sharepoint_tool = SharepointTool(connection_id=sharepoint_conn.id)
    
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="sharepoint-tester",
        instructions="You are a SharePoint assistant. Search and provide information from the connected SharePoint site.",
        tools=sharepoint_tool.definitions
    )
    
    # Test questions that should work with real SharePoint
    test_questions = [
        "What documents are in the Shared Documents library?",
        "Are there any policy documents available?", 
        "What files can you find on this SharePoint site?",
        "List the document libraries available"
    ]
    
    print("Testing SharePoint connection...")
    for question in test_questions:
        thread = project_client.agents.threads.create()
        project_client.agents.messages.create(thread_id=thread.id, role="user", content=question)
        run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)
        
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)
        
        messages = list(project_client.agents.messages.list(thread_id=thread.id))
        for msg in messages:
            if msg.role.value == "assistant" and msg.content:
                print(f"Q: {question}")
                print(f"A: {msg.content[0].text.value[:200]}...")
                print("-" * 50)
                break

if __name__ == "__main__":
    test_real_sharepoint()
'''
    
    print(test_script)

def main():
    """Main diagnostic and setup guide"""
    
    print("🚀 SharePoint Setup for Azure AI Foundry Tutorial Series")
    print("This ensures your foundation supports all 3 tutorials")
    
    # Check current state
    is_working = check_sharepoint_connection_detailed()
    
    if not is_working:
        # Provide setup instructions
        provide_sharepoint_setup_instructions()
        suggest_sharepoint_content_structure()
        test_sharepoint_once_fixed()
    else:
        print("✅ SharePoint connection appears to be configured correctly!")
        print("💡 Proceed with testing the actual SharePoint functionality.")

if __name__ == "__main__":
    main()