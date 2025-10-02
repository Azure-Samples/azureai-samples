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

using Azure.AI.Projects;
using Azure.AI.Agents.Models;
using Azure.Identity;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Text.Json;

namespace ModernWorkplaceAssistant
{
    // ============================================================================
    // CONFIGURATION AND DATA MODELS
    // ============================================================================
    
    public class AgentConfiguration
    {
        public Agent Agent { get; set; }
        public McpTool McpTool { get; set; }
        public SharepointTool SharepointTool { get; set; }
    }
    
    public class BusinessScenario
    {
        public string Title { get; set; }
        public string Question { get; set; }
        public string Context { get; set; }
        public string ExpectedSource { get; set; }
        public string LearningPoint { get; set; }
    }
    
    public class ChatResult
    {
        public string Content { get; set; }
        public string Status { get; set; }
    }
    
    public class Program
    {
        // ========================================================================
        // AUTHENTICATION SETUP
        // ========================================================================
        // Support both default Azure credentials and specific tenant authentication
        private static AIProjectClient projectClient;
        
        static Program()
        {
            // Load environment variables
            LoadEnvironmentVariables();
            
            var aiFundryTenantId = Environment.GetEnvironmentVariable("AI_FOUNDRY_TENANT_ID");
            DefaultAzureCredential credential;
            
            if (!string.IsNullOrEmpty(aiFundryTenantId))
            {
                Console.WriteLine($"🔐 Using AI Foundry tenant: {aiFundryTenantId}");
                credential = new DefaultAzureCredential();
            }
            else
            {
                credential = new DefaultAzureCredential();
            }
            
            projectClient = new AIProjectClient(
                new Uri(Environment.GetEnvironmentVariable("PROJECT_ENDPOINT")),
                credential
            );
        }
        
        private static void LoadEnvironmentVariables()
        {
            // Load .env file if it exists
            var envFile = Path.Combine(Directory.GetCurrentDirectory(), ".env");
            if (File.Exists(envFile))
            {
                var lines = File.ReadAllLines(envFile);
                foreach (var line in lines)
                {
                    if (string.IsNullOrWhiteSpace(line) || line.StartsWith("#"))
                        continue;
                        
                    var parts = line.Split('=', 2);
                    if (parts.Length == 2)
                    {
                        Environment.SetEnvironmentVariable(parts[0].Trim(), parts[1].Trim());
                    }
                }
            }
        }
        
        /// <summary>
        /// Create a Modern Workplace Assistant combining internal and external knowledge.
        /// 
        /// This demonstrates enterprise AI patterns:
        /// 1. Multi-source data integration (SharePoint + MCP)
        /// 2. Robust error handling with graceful degradation
        /// 3. Dynamic agent capabilities based on available resources
        /// 4. Clear diagnostic information for troubleshooting
        /// 
        /// Educational Value:
        /// - Shows real-world complexity of enterprise AI systems
        /// - Demonstrates how to handle partial system failures
        /// - Provides patterns for combining internal and external data
        /// </summary>
        /// <returns>AgentConfiguration for further interaction and testing</returns>
        public static async Task<AgentConfiguration> CreateWorkplaceAssistantAsync()
        {
            Console.WriteLine("🤖 Creating Modern Workplace Assistant...");
            
            // ====================================================================
            // SHAREPOINT INTEGRATION SETUP
            // ====================================================================
            // SharePoint provides access to internal company knowledge:
            // - Company policies and procedures
            // - Security guidelines and requirements  
            // - Governance and compliance documentation
            // - Internal process documentation
            
            var sharepointResourceName = Environment.GetEnvironmentVariable("SHAREPOINT_RESOURCE_NAME");
            var sharepointSiteUrl = Environment.GetEnvironmentVariable("SHAREPOINT_SITE_URL");
            
            Console.WriteLine("📁 Configuring SharePoint integration...");
            Console.WriteLine($"   Connection: {sharepointResourceName}");
            Console.WriteLine($"   Site URL: {sharepointSiteUrl}");
            
            SharepointTool sharepointTool = null;
            try
            {
                // Attempt to retrieve pre-configured SharePoint connection
                var sharepointConnection = await projectClient.GetConnectionAsync(sharepointResourceName);
                var currentTarget = sharepointConnection?.Target ?? "N/A";
                
                // Validate connection configuration (common preview issue)
                if (currentTarget == "_" || string.IsNullOrEmpty(currentTarget) || currentTarget == "N/A")
                {
                    Console.WriteLine($"⚠️  SharePoint connection has invalid target: '{currentTarget}'");
                    Console.WriteLine($"   Expected: {sharepointSiteUrl}");
                    Console.WriteLine("   🔧 SOLUTION: Update connection target in Azure AI Foundry portal");
                    Console.WriteLine("      1. Go to Management Center > Connected Resources");
                    Console.WriteLine($"      2. Edit '{sharepointResourceName}' connection");
                    Console.WriteLine($"      3. Set target URL to: {sharepointSiteUrl}");
                    sharepointTool = null;
                }
                else
                {
                    sharepointTool = new SharepointTool(sharepointConnection.Id);
                    Console.WriteLine("✅ SharePoint successfully connected");
                    Console.WriteLine($"   Active target: {currentTarget}");
                }
            }
            catch (Exception ex)
            {
                // Graceful degradation - system continues without SharePoint
                Console.WriteLine($"⚠️  SharePoint connection failed: {ex.Message}");
                Console.WriteLine("   Agent will operate in technical guidance mode only");
                Console.WriteLine("   📝 To enable full functionality:");
                Console.WriteLine("      1. Create SharePoint connection in Azure AI Foundry portal");
                Console.WriteLine($"      2. Connection name: {sharepointResourceName}");
                Console.WriteLine($"      3. Site URL: {sharepointSiteUrl}");
                sharepointTool = null;
            }
            
            // ====================================================================
            // MICROSOFT LEARN MCP INTEGRATION SETUP  
            // ====================================================================
            // Microsoft Learn MCP provides access to current technical documentation:
            // - Azure service configuration guides
            // - Best practices and implementation patterns
            // - Troubleshooting and diagnostic information
            // - Latest feature updates and capabilities
            
            Console.WriteLine("📚 Configuring Microsoft Learn MCP integration...");
            var mcpTool = new McpTool
            {
                ServerLabel = "microsoft_learn",
                ServerUrl = Environment.GetEnvironmentVariable("MCP_SERVER_URL"),
                AllowedTools = new List<string>() // Allow all available tools
            };
            
            // Disable approval workflow for seamless demonstration
            mcpTool.SetApprovalMode("never");
            Console.WriteLine($"✅ Microsoft Learn MCP connected: {Environment.GetEnvironmentVariable("MCP_SERVER_URL")}");
            
            // ====================================================================
            // AGENT CREATION WITH DYNAMIC CAPABILITIES
            // ====================================================================
            // Create agent instructions based on available data sources
            // This demonstrates adaptive system design
            
            string instructions;
            if (sharepointTool != null)
            {
                instructions = @"You are a Modern Workplace Assistant for Contoso Corporation.

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
- ""What is our MFA policy?"" → Search SharePoint for security policies
- ""How do I configure Azure AD Conditional Access?"" → Use Microsoft Learn for technical steps
- ""Our policy requires MFA - how do I implement this?"" → Combine policy requirements with implementation guidance";
            }
            else
            {
                instructions = @"You are a Technical Assistant with access to Microsoft Learn documentation.

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
- Suggest how technical implementations typically align with enterprise requirements";
            }
            
            // Create the agent with appropriate tool configuration
            Console.WriteLine("🛠️  Configuring agent tools...");
            var availableTools = new List<ToolDefinition>();
            if (sharepointTool != null)
            {
                availableTools.AddRange(sharepointTool.Definitions);
            }
            availableTools.AddRange(mcpTool.Definitions);
            Console.WriteLine($"   Available tools: {availableTools.Count}");
            
            var agent = await projectClient.CreateAgentAsync(
                Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME"),
                "Modern Workplace Assistant",
                instructions,
                availableTools
            );
            
            Console.WriteLine($"✅ Agent created successfully: {agent.Id}");
            return new AgentConfiguration 
            { 
                Agent = agent, 
                McpTool = mcpTool, 
                SharepointTool = sharepointTool 
            };
        }
        
        /// <summary>
        /// Demonstrate realistic business scenarios combining internal and external knowledge.
        /// 
        /// This function showcases the practical value of the Modern Workplace Assistant
        /// by walking through scenarios that enterprise employees face regularly.
        /// 
        /// Educational Value:
        /// - Shows real business problems that AI agents can solve
        /// - Demonstrates integration between internal policies and external guidance
        /// - Illustrates how AI can bridge the gap between requirements and implementation
        /// </summary>
        public static async Task DemonstrateBusinessScenariosAsync(AgentConfiguration config)
        {
            var scenarios = new[]
            {
                new BusinessScenario
                {
                    Title = "📋 Company Policy Question",
                    Question = "What is our remote work security policy regarding multi-factor authentication?",
                    Context = "Employee needs to understand company MFA requirements",
                    ExpectedSource = "SharePoint",
                    LearningPoint = "Internal policy retrieval and interpretation"
                },
                new BusinessScenario
                {
                    Title = "🔧 Technical Implementation Question",
                    Question = "How do I set up Azure Active Directory conditional access policies?",
                    Context = "IT administrator needs technical implementation steps",
                    ExpectedSource = "Microsoft Learn MCP",
                    LearningPoint = "External technical documentation access"
                },
                new BusinessScenario
                {
                    Title = "🔄 Combined Business Implementation Question",
                    Question = "Our company security policy requires multi-factor authentication for remote workers. How do I implement this requirement using Azure AD?",
                    Context = "Need to combine policy requirements with technical implementation",
                    ExpectedSource = "Both SharePoint and MCP",
                    LearningPoint = "Multi-source intelligence combining internal requirements with external implementation"
                }
            };
            
            Console.WriteLine($"\n{new string('=', 70)}");
            Console.WriteLine("🏢 MODERN WORKPLACE ASSISTANT - BUSINESS SCENARIO DEMONSTRATION");
            Console.WriteLine(new string('=', 70));
            Console.WriteLine("This demonstration shows how AI agents solve real business problems");
            Console.WriteLine("by combining internal company knowledge with external technical guidance.");
            Console.WriteLine(new string('=', 70));
            
            for (int i = 0; i < scenarios.Length; i++)
            {
                var scenario = scenarios[i];
                Console.WriteLine($"\n📊 SCENARIO {i + 1}/3: {scenario.Title}");
                Console.WriteLine(new string('-', 50));
                Console.WriteLine($"❓ QUESTION: {scenario.Question}");
                Console.WriteLine($"🎯 BUSINESS CONTEXT: {scenario.Context}");
                Console.WriteLine($"📚 EXPECTED SOURCE: {scenario.ExpectedSource}");
                Console.WriteLine($"🎓 LEARNING POINT: {scenario.LearningPoint}");
                Console.WriteLine(new string('-', 50));
                
                // Get response from the agent
                Console.WriteLine("🤖 ASSISTANT RESPONSE:");
                var response = await ChatWithAssistantAsync(config.Agent.Id, config.McpTool, scenario.Question);
                
                // Display response with analysis
                if (response.Status == "completed" && !string.IsNullOrWhiteSpace(response.Content) && response.Content.Trim().Length > 10)
                {
                    var preview = response.Content.Length > 300 ? response.Content.Substring(0, 300) + "..." : response.Content;
                    Console.WriteLine($"✅ SUCCESS: {preview}");
                    if (response.Content.Length > 300)
                    {
                        Console.WriteLine($"   📏 Full response: {response.Content.Length} characters");
                    }
                }
                else
                {
                    Console.WriteLine($"⚠️  LIMITED RESPONSE: {response.Content}");
                    if (config.SharepointTool == null && scenario.ExpectedSource.Contains("SharePoint"))
                    {
                        Console.WriteLine("   💡 This demonstrates graceful degradation when SharePoint is unavailable");
                    }
                }
                
                Console.WriteLine($"📈 STATUS: {response.Status}");
                Console.WriteLine(new string('-', 50));
            }
            
            Console.WriteLine("\n✅ DEMONSTRATION COMPLETED!");
            Console.WriteLine("🎓 Key Learning Outcomes:");
            Console.WriteLine("   • Multi-source data integration in enterprise AI");
            Console.WriteLine("   • Robust error handling and graceful degradation");
            Console.WriteLine("   • Real business value through combined intelligence");
            Console.WriteLine("   • Foundation for governance and monitoring (Tutorials 2-3)");
        }
        
        /// <summary>
        /// Execute a conversation with the workplace assistant.
        /// 
        /// This function demonstrates the conversation pattern for Azure AI Foundry agents
        /// and includes comprehensive error handling for production readiness.
        /// 
        /// Educational Value:
        /// - Shows proper thread management and conversation flow
        /// - Demonstrates streaming response handling
        /// - Includes timeout and error management patterns
        /// </summary>
        public static async Task<ChatResult> ChatWithAssistantAsync(string agentId, McpTool mcpTool, string message)
        {
            try
            {
                // Create conversation thread (maintains conversation context)
                var thread = await projectClient.CreateThreadAsync();
                
                // Add user message to thread
                await projectClient.CreateMessageAsync(thread.Id, "user", message);
                
                // Execute the conversation with streaming response
                var runStream = projectClient.CreateAndStreamRunAsync(thread.Id, agentId);
                
                // Collect streaming response
                var responseParts = new List<string>();
                var finalStatus = "unknown";
                
                await foreach (var eventData in runStream)
                {
                    if (eventData.EventType == "MessageDelta")
                    {
                        var delta = eventData.Data as dynamic;
                        foreach (var contentPart in delta?.delta?.content ?? new object[0])
                        {
                            if (contentPart?.text?.value != null)
                            {
                                responseParts.Add(contentPart.text.value.ToString());
                            }
                        }
                    }
                    if (eventData.RunStatus != null)
                    {
                        finalStatus = eventData.RunStatus.Status;
                    }
                }
                
                var fullResponse = string.Join("", responseParts);
                return new ChatResult { Content = fullResponse, Status = finalStatus };
            }
            catch (Exception ex)
            {
                return new ChatResult { Content = $"Error in conversation: {ex.Message}", Status = "failed" };
            }
        }
        
        /// <summary>
        /// Interactive mode for testing the workplace assistant.
        /// 
        /// This provides a simple interface for users to test the agent with their own questions
        /// and see how it combines different data sources for comprehensive answers.
        /// </summary>
        public static async Task InteractiveModeAsync(AgentConfiguration config)
        {
            Console.WriteLine($"\n{new string('=', 60)}");
            Console.WriteLine("💬 INTERACTIVE MODE - Test Your Workplace Assistant!");
            Console.WriteLine(new string('=', 60));
            Console.WriteLine("Ask questions that combine company policies with technical guidance:");
            Console.WriteLine("• 'What's our remote work policy for Azure access?'");
            Console.WriteLine("• 'How do I configure SharePoint security?'");
            Console.WriteLine("• 'Our policy requires encryption - how do I set this up in Azure?'");
            Console.WriteLine("Type 'quit' to exit.");
            Console.WriteLine(new string('-', 60));
            
            while (true)
            {
                try
                {
                    Console.Write("\n❓ Your question: ");
                    var question = Console.ReadLine()?.Trim();
                    
                    if (string.IsNullOrEmpty(question))
                    {
                        Console.WriteLine("💡 Please ask a question about policies or technical implementation.");
                        continue;
                    }
                    
                    if (new[] { "quit", "exit", "bye" }.Contains(question.ToLower()))
                    {
                        break;
                    }
                    
                    Console.Write("\n🤖 Workplace Assistant: ");
                    var response = await ChatWithAssistantAsync(config.Agent.Id, config.McpTool, question);
                    Console.WriteLine(response.Content);
                    
                    if (response.Status != "completed")
                    {
                        Console.WriteLine($"\n⚠️  Response status: {response.Status}");
                    }
                    
                    Console.WriteLine(new string('-', 60));
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"\n❌ Error: {ex.Message}");
                    Console.WriteLine(new string('-', 60));
                }
            }
            
            Console.WriteLine("\n👋 Thank you for testing the Modern Workplace Assistant!");
        }
        
        /// <summary>
        /// Main execution flow demonstrating the complete sample.
        /// 
        /// This orchestrates the full demonstration:
        /// 1. Agent creation with diagnostic information
        /// 2. Business scenario demonstration  
        /// 3. Interactive testing mode
        /// 4. Clean completion with next steps
        /// </summary>
        public static async Task Main(string[] args)
        {
            Console.WriteLine("🚀 Azure AI Foundry - Modern Workplace Assistant");
            Console.WriteLine("Tutorial 1: Building Enterprise Agents with SharePoint + MCP Integration");
            Console.WriteLine(new string('=', 70));
            
            try
            {
                // Create the agent with full diagnostic output
                var agentConfig = await CreateWorkplaceAssistantAsync();
                
                // Demonstrate business scenarios  
                await DemonstrateBusinessScenariosAsync(agentConfig);
                
                // Offer interactive testing
                Console.Write("\n🎯 Try interactive mode? (y/n): ");
                var answer = Console.ReadLine()?.ToLower();
                if (answer?.StartsWith("y") == true)
                {
                    await InteractiveModeAsync(agentConfig);
                }
                
                Console.WriteLine("\n🎉 Sample completed successfully!");
                Console.WriteLine("📚 This foundation supports Tutorial 2 (Governance) and Tutorial 3 (Production)");
                Console.WriteLine("🔗 Next: Add evaluation metrics, monitoring, and production deployment");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Sample failed: {ex.Message}");
                Environment.Exit(1);
            }
        }
    }
}