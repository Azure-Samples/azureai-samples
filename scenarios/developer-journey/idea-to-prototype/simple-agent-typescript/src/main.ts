/**
 * Azure AI Foundry Agent Sample - Tutorial 1: Modern Workplace Assistant
 * 
 * This sample demonstrates a complete business scenario combining:
 * - SharePoint integration for internal company knowledge
 * - Microsoft Learn MCP integration for external technical guidance  
 * - Intelligent orchestration of multiple data sources
 * - Robust error handling and graceful degradation
 * 
 * Educational Focus:
 * - Enterprise AI patterns with multiple data sources
 * - Real-world business scenarios that enterprises face daily
 * - Production-ready error handling and diagnostics
 * - Foundation for governance, evaluation, and monitoring (Tutorials 2-3)
 * 
 * Business Scenario:
 * An employee needs to implement Azure AD multi-factor authentication. They need:
 * 1. Company security policy requirements (from SharePoint)
 * 2. Technical implementation steps (from Microsoft Learn)
 * 3. Combined guidance showing how policy requirements map to technical implementation
 */

import { AIProjectClient } from '@azure/ai-projects';
import { DefaultAzureCredential, AzureCliCredential } from '@azure/identity';
import { Agent, SharepointTool, McpTool, ToolDefinition } from '@azure/ai-agents';
import * as dotenv from 'dotenv';
import * as readline from 'readline';

// Load environment configuration
dotenv.config();

// ============================================================================
// AUTHENTICATION SETUP
// ============================================================================
// Support both default Azure credentials and specific tenant authentication
const aiFundryTenantId = process.env.AI_FOUNDRY_TENANT_ID;
let credential: DefaultAzureCredential | AzureCliCredential;

if (aiFundryTenantId) {
    console.log(`🔐 Using AI Foundry tenant: ${aiFundryTenantId}`);
    credential = new AzureCliCredential();
} else {
    credential = new DefaultAzureCredential();
}

const projectClient = new AIProjectClient(
    process.env.PROJECT_ENDPOINT!,
    credential
);

// ============================================================================
// INTERFACES AND TYPES
// ============================================================================

interface AgentConfiguration {
    agent: Agent;
    mcpTool: McpTool;
    sharepointTool: SharepointTool | null;
}

interface BusinessScenario {
    title: string;
    question: string;
    context: string;
    expectedSource: string;
    learningPoint: string;
}

interface ChatResult {
    content: string;
    status: string;
}

/**
 * Create a Modern Workplace Assistant combining internal and external knowledge.
 * 
 * This demonstrates enterprise AI patterns:
 * 1. Multi-source data integration (SharePoint + MCP)
 * 2. Robust error handling with graceful degradation
 * 3. Dynamic agent capabilities based on available resources
 * 4. Clear diagnostic information for troubleshooting
 * 
 * Educational Value:
 * - Shows real-world complexity of enterprise AI systems
 * - Demonstrates how to handle partial system failures
 * - Provides patterns for combining internal and external data
 * 
 * @returns AgentConfiguration for further interaction and testing
 */
async function createWorkplaceAssistant(): Promise<AgentConfiguration> {
    console.log('🤖 Creating Modern Workplace Assistant...');
    
    // ========================================================================
    // SHAREPOINT INTEGRATION SETUP
    // ========================================================================
    // SharePoint provides access to internal company knowledge:
    // - Company policies and procedures
    // - Security guidelines and requirements  
    // - Governance and compliance documentation
    // - Internal process documentation
    
    const sharepointResourceName = process.env.SHAREPOINT_RESOURCE_NAME!;
    const sharepointSiteUrl = process.env.SHAREPOINT_SITE_URL!;
    
    console.log('📁 Configuring SharePoint integration...');
    console.log(`   Connection: ${sharepointResourceName}`);
    console.log(`   Site URL: ${sharepointSiteUrl}`);
    
    let sharepointTool: SharepointTool | null = null;
    try {
        // Attempt to retrieve pre-configured SharePoint connection
        const sharepointConnection = await projectClient.connections.get(sharepointResourceName);
        const currentTarget = sharepointConnection.target || 'N/A';
        
        // Validate connection configuration (common preview issue)
        if (currentTarget === '_' || !currentTarget || currentTarget === 'N/A') {
            console.log(`⚠️  SharePoint connection has invalid target: '${currentTarget}'`);
            console.log(`   Expected: ${sharepointSiteUrl}`);
            console.log('   🔧 SOLUTION: Update connection target in Azure AI Foundry portal');
            console.log('      1. Go to Management Center > Connected Resources');
            console.log(`      2. Edit '${sharepointResourceName}' connection`);
            console.log(`      3. Set target URL to: ${sharepointSiteUrl}`);
            sharepointTool = null;
        } else {
            sharepointTool = new SharepointTool({ connectionId: sharepointConnection.id });
            console.log('✅ SharePoint successfully connected');
            console.log(`   Active target: ${currentTarget}`);
        }
        
    } catch (error) {
        // Graceful degradation - system continues without SharePoint
        console.log(`⚠️  SharePoint connection failed: ${error}`);
        console.log('   Agent will operate in technical guidance mode only');
        console.log('   📝 To enable full functionality:');
        console.log('      1. Create SharePoint connection in Azure AI Foundry portal');
        console.log(`      2. Connection name: ${sharepointResourceName}`);
        console.log(`      3. Site URL: ${sharepointSiteUrl}`);
        sharepointTool = null;
    }
    
    // ========================================================================
    // MICROSOFT LEARN MCP INTEGRATION SETUP  
    // ========================================================================
    // Microsoft Learn MCP provides access to current technical documentation:
    // - Azure service configuration guides
    // - Best practices and implementation patterns
    // - Troubleshooting and diagnostic information
    // - Latest feature updates and capabilities
    
    console.log('📚 Configuring Microsoft Learn MCP integration...');
    const mcpTool = new McpTool({
        serverLabel: 'microsoft_learn',
        serverUrl: process.env.MCP_SERVER_URL!,
        allowedTools: [] // Allow all available tools
    });
    
    // Disable approval workflow for seamless demonstration
    mcpTool.setApprovalMode('never');
    console.log(`✅ Microsoft Learn MCP connected: ${process.env.MCP_SERVER_URL}`);
    
    // ========================================================================
    // AGENT CREATION WITH DYNAMIC CAPABILITIES
    // ========================================================================
    // Create agent instructions based on available data sources
    // This demonstrates adaptive system design
    
    let instructions: string;
    if (sharepointTool) {
        instructions = `You are a Modern Workplace Assistant for Contoso Corporation.

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
- "Our policy requires MFA - how do I implement this?" → Combine policy requirements with implementation guidance`;
    } else {
        instructions = `You are a Technical Assistant with access to Microsoft Learn documentation.

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
- Suggest how technical implementations typically align with enterprise requirements`;
    }

    // Create the agent with appropriate tool configuration
    console.log('🛠️  Configuring agent tools...');
    const availableTools: ToolDefinition[] = [];
    if (sharepointTool) {
        availableTools.push(...sharepointTool.definitions);
    }
    availableTools.push(...mcpTool.definitions);
    console.log(`   Available tools: ${availableTools.length}`);
    
    const agent = await projectClient.agents.create({
        model: process.env.MODEL_DEPLOYMENT_NAME!,
        name: 'Modern Workplace Assistant',
        instructions: instructions,
        tools: availableTools
    });
    
    console.log(`✅ Agent created successfully: ${agent.id}`);
    return { agent, mcpTool, sharepointTool };
}

/**
 * Demonstrate realistic business scenarios combining internal and external knowledge.
 * 
 * This function showcases the practical value of the Modern Workplace Assistant
 * by walking through scenarios that enterprise employees face regularly.
 * 
 * Educational Value:
 * - Shows real business problems that AI agents can solve
 * - Demonstrates integration between internal policies and external guidance
 * - Illustrates how AI can bridge the gap between requirements and implementation
 */
async function demonstrateBusinessScenarios(config: AgentConfiguration): Promise<void> {
    const scenarios: BusinessScenario[] = [
        {
            title: '📋 Company Policy Question',
            question: 'What is our remote work security policy regarding multi-factor authentication?',
            context: 'Employee needs to understand company MFA requirements',
            expectedSource: 'SharePoint',
            learningPoint: 'Internal policy retrieval and interpretation'
        },
        {
            title: '🔧 Technical Implementation Question', 
            question: 'How do I set up Azure Active Directory conditional access policies?',
            context: 'IT administrator needs technical implementation steps',
            expectedSource: 'Microsoft Learn MCP',
            learningPoint: 'External technical documentation access'
        },
        {
            title: '🔄 Combined Business Implementation Question',
            question: 'Our company security policy requires multi-factor authentication for remote workers. How do I implement this requirement using Azure AD?',
            context: 'Need to combine policy requirements with technical implementation',
            expectedSource: 'Both SharePoint and MCP',
            learningPoint: 'Multi-source intelligence combining internal requirements with external implementation'
        }
    ];
    
    console.log('\n' + '='.repeat(70));
    console.log('🏢 MODERN WORKPLACE ASSISTANT - BUSINESS SCENARIO DEMONSTRATION');  
    console.log('='.repeat(70));
    console.log('This demonstration shows how AI agents solve real business problems');
    console.log('by combining internal company knowledge with external technical guidance.');
    console.log('='.repeat(70));
    
    for (let i = 0; i < scenarios.length; i++) {
        const scenario = scenarios[i];
        console.log(`\n📊 SCENARIO ${i + 1}/3: ${scenario.title}`);
        console.log('-'.repeat(50));
        console.log(`❓ QUESTION: ${scenario.question}`);
        console.log(`🎯 BUSINESS CONTEXT: ${scenario.context}`);
        console.log(`📚 EXPECTED SOURCE: ${scenario.expectedSource}`);
        console.log(`🎓 LEARNING POINT: ${scenario.learningPoint}`);
        console.log('-'.repeat(50));
        
        // Get response from the agent
        console.log('🤖 ASSISTANT RESPONSE:');
        const response = await chatWithAssistant(config.agent.id, config.mcpTool, scenario.question);
        
        // Display response with analysis
        if (response.status === 'completed' && response.content && response.content.trim().length > 10) {
            const preview = response.content.length > 300 ? response.content.substring(0, 300) + '...' : response.content;
            console.log(`✅ SUCCESS: ${preview}`);
            if (response.content.length > 300) {
                console.log(`   📏 Full response: ${response.content.length} characters`);
            }
        } else {
            console.log(`⚠️  LIMITED RESPONSE: ${response.content}`);
            if (!config.sharepointTool && scenario.expectedSource.includes('SharePoint')) {
                console.log('   💡 This demonstrates graceful degradation when SharePoint is unavailable');
            }
        }
        
        console.log(`📈 STATUS: ${response.status}`);
        console.log('-'.repeat(50));
    }
    
    console.log('\n✅ DEMONSTRATION COMPLETED!');
    console.log('🎓 Key Learning Outcomes:');
    console.log('   • Multi-source data integration in enterprise AI');
    console.log('   • Robust error handling and graceful degradation');  
    console.log('   • Real business value through combined intelligence');
    console.log('   • Foundation for governance and monitoring (Tutorials 2-3)');
}

/**
 * Execute a conversation with the workplace assistant.
 * 
 * This function demonstrates the conversation pattern for Azure AI Foundry agents
 * and includes comprehensive error handling for production readiness.
 * 
 * Educational Value:
 * - Shows proper thread management and conversation flow
 * - Demonstrates streaming response handling
 * - Includes timeout and error management patterns
 */
async function chatWithAssistant(agentId: string, mcpTool: McpTool, message: string): Promise<ChatResult> {
    try {
        // Create conversation thread (maintains conversation context)
        const thread = await projectClient.agents.threads.create();
        
        // Add user message to thread
        await projectClient.agents.messages.create(thread.id, {
            role: 'user',
            content: message
        });
        
        // Execute the conversation with streaming response
        const runStream = await projectClient.agents.runs.createAndStream(
            thread.id,
            { assistantId: agentId }
        );
        
        // Collect streaming response
        const responseParts: string[] = [];
        let finalStatus = 'unknown';
        
        for await (const event of runStream) {
            if (event.eventType === 'MessageDelta') {
                const delta = event.data as any;
                for (const contentPart of delta.delta.content || []) {
                    if (contentPart.text?.value) {
                        responseParts.push(contentPart.text.value);
                    }
                }
            }
            if (event.runStatus) {
                finalStatus = event.runStatus.status;
            }
        }
        
        const fullResponse = responseParts.join('');
        return { content: fullResponse, status: finalStatus };
        
    } catch (error) {
        return { content: `Error in conversation: ${error}`, status: 'failed' };
    }
}

/**
 * Interactive mode for testing the workplace assistant.
 * 
 * This provides a simple interface for users to test the agent with their own questions
 * and see how it combines different data sources for comprehensive answers.
 */
async function interactiveMode(config: AgentConfiguration): Promise<void> {
    console.log('\n' + '='.repeat(60));
    console.log('💬 INTERACTIVE MODE - Test Your Workplace Assistant!');
    console.log('='.repeat(60));
    console.log('Ask questions that combine company policies with technical guidance:');
    console.log("• 'What's our remote work policy for Azure access?'");
    console.log("• 'How do I configure SharePoint security?'"); 
    console.log("• 'Our policy requires encryption - how do I set this up in Azure?'");
    console.log("Type 'quit' to exit.");
    console.log('-'.repeat(60));
    
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    const askQuestion = (): Promise<string> => {
        return new Promise((resolve) => {
            rl.question('\n❓ Your question: ', (answer) => {
                resolve(answer.trim());
            });
        });
    };
    
    try {
        while (true) {
            const question = await askQuestion();
            
            if (['quit', 'exit', 'bye'].includes(question.toLowerCase())) {
                break;
            }
            
            if (!question) {
                console.log('💡 Please ask a question about policies or technical implementation.');
                continue;
            }
            
            process.stdout.write('\n🤖 Workplace Assistant: ');
            const response = await chatWithAssistant(config.agent.id, config.mcpTool, question);
            console.log(response.content);
            
            if (response.status !== 'completed') {
                console.log(`\n⚠️  Response status: ${response.status}`);
            }
            
            console.log('-'.repeat(60));
        }
    } catch (error) {
        console.log(`\n❌ Error: ${error}`);
    } finally {
        rl.close();
    }
    
    console.log('\n👋 Thank you for testing the Modern Workplace Assistant!');
}

/**
 * Main execution flow demonstrating the complete sample.
 * 
 * This orchestrates the full demonstration:
 * 1. Agent creation with diagnostic information
 * 2. Business scenario demonstration  
 * 3. Interactive testing mode
 * 4. Clean completion with next steps
 */
async function main(): Promise<void> {
    console.log('🚀 Azure AI Foundry - Modern Workplace Assistant');
    console.log('Tutorial 1: Building Enterprise Agents with SharePoint + MCP Integration');
    console.log('='.repeat(70));
    
    try {
        // Create the agent with full diagnostic output
        const agentConfig = await createWorkplaceAssistant();
        
        // Demonstrate business scenarios  
        await demonstrateBusinessScenarios(agentConfig);
        
        // Offer interactive testing
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        const answer = await new Promise<string>((resolve) => {
            rl.question('\n🎯 Try interactive mode? (y/n): ', (answer) => {
                rl.close();
                resolve(answer.toLowerCase());
            });
        });
        
        if (answer.startsWith('y')) {
            await interactiveMode(agentConfig);
        }
        
        console.log('\n🎉 Sample completed successfully!');
        console.log('📚 This foundation supports Tutorial 2 (Governance) and Tutorial 3 (Production)');
        console.log('🔗 Next: Add evaluation metrics, monitoring, and production deployment');
        
    } catch (error) {
        console.error('❌ Sample failed:', error);
        process.exit(1);
    }
}

// Run the main function if this is the main module
if (require.main === module) {
    main();
}

export {
    createWorkplaceAssistant,
    demonstrateBusinessScenarios,
    chatWithAssistant,
    interactiveMode,
    AgentConfiguration,
    BusinessScenario,
    ChatResult
};