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

import com.azure.ai.projects.AIProjectClient;
import com.azure.ai.projects.AIProjectClientBuilder;
import com.azure.ai.agents.models.*;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.AzureCliCredential;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;

public class Main {
    
    // ============================================================================
    // CONFIGURATION AND SETUP
    // ============================================================================
    
    private static final Properties config = new Properties();
    private static AIProjectClient projectClient;
    
    static {
        // Load environment configuration
        try {
            loadEnvironmentConfig();
            setupAuthentication();
        } catch (Exception e) {
            System.err.println("Failed to initialize configuration: " + e.getMessage());
            System.exit(1);
        }
    }
    
    private static void loadEnvironmentConfig() throws IOException {
        // Load .env file if it exists
        if (Files.exists(Paths.get(".env"))) {
            Files.lines(Paths.get(".env"))
                    .filter(line -> !line.trim().isEmpty() && !line.startsWith("#"))
                    .forEach(line -> {
                        String[] parts = line.split("=", 2);
                        if (parts.length == 2) {
                            config.setProperty(parts[0].trim(), parts[1].trim());
                        }
                    });
        }
        
        // Override with system environment variables
        System.getenv().forEach((key, value) -> {
            if (config.containsKey(key) || key.startsWith("AI_FOUNDRY_") || 
                key.startsWith("PROJECT_") || key.startsWith("SHAREPOINT_") || 
                key.startsWith("MCP_") || key.startsWith("MODEL_")) {
                config.setProperty(key, value);
            }
        });
    }
    
    private static void setupAuthentication() {
        // Support both default Azure credentials and specific tenant authentication
        String tenantId = config.getProperty("AI_FOUNDRY_TENANT_ID");
        
        if (tenantId != null && !tenantId.isEmpty()) {
            System.out.println("🔐 Using AI Foundry tenant: " + tenantId);
            projectClient = new AIProjectClientBuilder()
                    .endpoint(config.getProperty("PROJECT_ENDPOINT"))
                    .credential(new AzureCliCredential())
                    .buildClient();
        } else {
            projectClient = new AIProjectClientBuilder()
                    .endpoint(config.getProperty("PROJECT_ENDPOINT"))
                    .credential(new DefaultAzureCredential())
                    .buildClient();
        }
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
     * @return AgentConfiguration containing agent and tool information
     */
    public static AgentConfiguration createWorkplaceAssistant() {
        System.out.println("🤖 Creating Modern Workplace Assistant...");
        
        // ========================================================================
        // SHAREPOINT INTEGRATION SETUP
        // ========================================================================
        // SharePoint provides access to internal company knowledge:
        // - Company policies and procedures
        // - Security guidelines and requirements  
        // - Governance and compliance documentation
        // - Internal process documentation
        
        String sharepointResourceName = config.getProperty("SHAREPOINT_RESOURCE_NAME");
        String sharepointSiteUrl = config.getProperty("SHAREPOINT_SITE_URL");
        
        System.out.println("📁 Configuring SharePoint integration...");
        System.out.println("   Connection: " + sharepointResourceName);
        System.out.println("   Site URL: " + sharepointSiteUrl);
        
        SharepointTool sharepointTool = null;
        try {
            // Attempt to retrieve pre-configured SharePoint connection
            var sharepointConnection = projectClient.getConnections().get(sharepointResourceName);
            String currentTarget = sharepointConnection.getTarget();
            
            // Validate connection configuration (common preview issue)
            if ("_".equals(currentTarget) || currentTarget == null || "N/A".equals(currentTarget)) {
                System.out.println("⚠️  SharePoint connection has invalid target: '" + currentTarget + "'");
                System.out.println("   Expected: " + sharepointSiteUrl);
                System.out.println("   🔧 SOLUTION: Update connection target in Azure AI Foundry portal");
                System.out.println("      1. Go to Management Center > Connected Resources");
                System.out.println("      2. Edit '" + sharepointResourceName + "' connection");
                System.out.println("      3. Set target URL to: " + sharepointSiteUrl);
                sharepointTool = null;
            } else {
                sharepointTool = new SharepointTool(sharepointConnection.getId());
                System.out.println("✅ SharePoint successfully connected");
                System.out.println("   Active target: " + currentTarget);
            }
            
        } catch (Exception e) {
            // Graceful degradation - system continues without SharePoint
            System.out.println("⚠️  SharePoint connection failed: " + e.getMessage());
            System.out.println("   Agent will operate in technical guidance mode only");
            System.out.println("   📝 To enable full functionality:");
            System.out.println("      1. Create SharePoint connection in Azure AI Foundry portal");
            System.out.println("      2. Connection name: " + sharepointResourceName);
            System.out.println("      3. Site URL: " + sharepointSiteUrl);
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
        
        System.out.println("📚 Configuring Microsoft Learn MCP integration...");
        McpTool mcpTool = new McpTool()
                .setServerLabel("microsoft_learn")
                .setServerUrl(config.getProperty("MCP_SERVER_URL"))
                .setAllowedTools(Collections.emptyList()); // Allow all available tools
        
        // Disable approval workflow for seamless demonstration
        mcpTool.setApprovalMode("never");
        System.out.println("✅ Microsoft Learn MCP connected: " + config.getProperty("MCP_SERVER_URL"));
        
        // ========================================================================
        // AGENT CREATION WITH DYNAMIC CAPABILITIES
        // ========================================================================
        // Create agent instructions based on available data sources
        // This demonstrates adaptive system design
        
        String instructions;
        if (sharepointTool != null) {
            instructions = """
                You are a Modern Workplace Assistant for Contoso Corporation.
                
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
                - "Our policy requires MFA - how do I implement this?" → Combine policy requirements with implementation guidance
                """;
        } else {
            instructions = """
                You are a Technical Assistant with access to Microsoft Learn documentation.
                
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
                - Suggest how technical implementations typically align with enterprise requirements
                """;
        }
        
        // Create the agent with appropriate tool configuration
        System.out.println("🛠️  Configuring agent tools...");
        List<ToolDefinition> availableTools = new ArrayList<>();
        if (sharepointTool != null) {
            availableTools.addAll(sharepointTool.getDefinitions());
        }
        availableTools.addAll(mcpTool.getDefinitions());
        System.out.println("   Available tools: " + availableTools.size());
        
        Agent agent = projectClient.getAgents().createAgent(
                config.getProperty("MODEL_DEPLOYMENT_NAME"),
                "Modern Workplace Assistant",
                instructions,
                availableTools
        );
        
        System.out.println("✅ Agent created successfully: " + agent.getId());
        return new AgentConfiguration(agent, mcpTool, sharepointTool);
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
    public static void demonstrateBusinessScenarios(AgentConfiguration config) {
        BusinessScenario[] scenarios = {
            new BusinessScenario(
                "📋 Company Policy Question",
                "What is our remote work security policy regarding multi-factor authentication?",
                "Employee needs to understand company MFA requirements",
                "SharePoint",
                "Internal policy retrieval and interpretation"
            ),
            new BusinessScenario(
                "🔧 Technical Implementation Question", 
                "How do I set up Azure Active Directory conditional access policies?",
                "IT administrator needs technical implementation steps",
                "Microsoft Learn MCP",
                "External technical documentation access"
            ),
            new BusinessScenario(
                "🔄 Combined Business Implementation Question",
                "Our company security policy requires multi-factor authentication for remote workers. How do I implement this requirement using Azure AD?",
                "Need to combine policy requirements with technical implementation",
                "Both SharePoint and MCP",
                "Multi-source intelligence combining internal requirements with external implementation"
            )
        };
        
        System.out.println("\n" + "=".repeat(70));
        System.out.println("🏢 MODERN WORKPLACE ASSISTANT - BUSINESS SCENARIO DEMONSTRATION");  
        System.out.println("=".repeat(70));
        System.out.println("This demonstration shows how AI agents solve real business problems");
        System.out.println("by combining internal company knowledge with external technical guidance.");
        System.out.println("=".repeat(70));
        
        for (int i = 0; i < scenarios.length; i++) {
            BusinessScenario scenario = scenarios[i];
            System.out.println(String.format("\n📊 SCENARIO %d/3: %s", i + 1, scenario.title));
            System.out.println("-".repeat(50));
            System.out.println("❓ QUESTION: " + scenario.question);
            System.out.println("🎯 BUSINESS CONTEXT: " + scenario.context);
            System.out.println("📚 EXPECTED SOURCE: " + scenario.expectedSource);
            System.out.println("🎓 LEARNING POINT: " + scenario.learningPoint);
            System.out.println("-".repeat(50));
            
            // Get response from the agent
            System.out.println("🤖 ASSISTANT RESPONSE:");
            ChatResult response = chatWithAssistant(config.agent.getId(), config.mcpTool, scenario.question);
            
            // Display response with analysis
            if ("completed".equals(response.status) && response.content != null && response.content.trim().length() > 10) {
                String preview = response.content.length() > 300 ? 
                    response.content.substring(0, 300) + "..." : response.content;
                System.out.println("✅ SUCCESS: " + preview);
                if (response.content.length() > 300) {
                    System.out.println("   📏 Full response: " + response.content.length() + " characters");
                }
            } else {
                System.out.println("⚠️  LIMITED RESPONSE: " + response.content);
                if (config.sharepointTool == null && (scenario.expectedSource.contains("SharePoint"))) {
                    System.out.println("   💡 This demonstrates graceful degradation when SharePoint is unavailable");
                }
            }
            
            System.out.println("📈 STATUS: " + response.status);
            System.out.println("-".repeat(50));
        }
        
        System.out.println("\n✅ DEMONSTRATION COMPLETED!");
        System.out.println("🎓 Key Learning Outcomes:");
        System.out.println("   • Multi-source data integration in enterprise AI");
        System.out.println("   • Robust error handling and graceful degradation");  
        System.out.println("   • Real business value through combined intelligence");
        System.out.println("   • Foundation for governance and monitoring (Tutorials 2-3)");
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
    public static ChatResult chatWithAssistant(String agentId, McpTool mcpTool, String message) {
        try {
            // Create conversation thread (maintains conversation context)
            Thread thread = projectClient.getAgents().getThreads().create();
            
            // Add user message to thread
            projectClient.getAgents().getMessages().create(
                thread.getId(), 
                "user", 
                message
            );
            
            // Execute the conversation with streaming response
            RunStream runStream = projectClient.getAgents().getRuns().createAndStream(
                thread.getId(),
                agentId
            );
            
            // Collect streaming response
            List<String> responseParts = new ArrayList<>();
            String finalStatus = "unknown";
            
            for (RunEvent event : runStream) {
                if (event.getEventType().equals("MessageDelta")) {
                    MessageDelta delta = (MessageDelta) event.getData();
                    for (ContentPart contentPart : delta.getDelta().getContent()) {
                        if (contentPart.getText() != null && contentPart.getText().getValue() != null) {
                            responseParts.add(contentPart.getText().getValue());
                        }
                    }
                }
                if (event.getRunStatus() != null) {
                    finalStatus = event.getRunStatus().getStatus();
                }
            }
            
            String fullResponse = String.join("", responseParts);
            return new ChatResult(fullResponse, finalStatus);
            
        } catch (Exception e) {
            return new ChatResult("Error in conversation: " + e.getMessage(), "failed");
        }
    }
    
    /**
     * Interactive mode for testing the workplace assistant.
     * 
     * This provides a simple interface for users to test the agent with their own questions
     * and see how it combines different data sources for comprehensive answers.
     */
    public static void interactiveMode(AgentConfiguration config) {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("💬 INTERACTIVE MODE - Test Your Workplace Assistant!");
        System.out.println("=".repeat(60));
        System.out.println("Ask questions that combine company policies with technical guidance:");
        System.out.println("• 'What's our remote work policy for Azure access?'");
        System.out.println("• 'How do I configure SharePoint security?'"); 
        System.out.println("• 'Our policy requires encryption - how do I set this up in Azure?'");
        System.out.println("Type 'quit' to exit.");
        System.out.println("-".repeat(60));
        
        Scanner scanner = new Scanner(System.in);
        
        while (true) {
            try {
                System.out.print("\n❓ Your question: ");
                String question = scanner.nextLine().trim();
                
                if (question.toLowerCase().matches("quit|exit|bye")) {
                    break;
                }
                
                if (question.isEmpty()) {
                    System.out.println("💡 Please ask a question about policies or technical implementation.");
                    continue;
                }
                
                System.out.print("\n🤖 Workplace Assistant: ");
                ChatResult response = chatWithAssistant(config.agent.getId(), config.mcpTool, question);
                System.out.println(response.content);
                
                if (!"completed".equals(response.status)) {
                    System.out.println("\n⚠️  Response status: " + response.status);
                }
                
                System.out.println("-".repeat(60));
                
            } catch (Exception e) {
                System.out.println("\n❌ Error: " + e.getMessage());
                System.out.println("-".repeat(60));
            }
        }
        
        System.out.println("\n👋 Thank you for testing the Modern Workplace Assistant!");
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
    public static void main(String[] args) {
        System.out.println("🚀 Azure AI Foundry - Modern Workplace Assistant");
        System.out.println("Tutorial 1: Building Enterprise Agents with SharePoint + MCP Integration");
        System.out.println("=".repeat(70));
        
        // Create the agent with full diagnostic output
        AgentConfiguration agentConfig = createWorkplaceAssistant();
        
        // Demonstrate business scenarios  
        demonstrateBusinessScenarios(agentConfig);
        
        // Offer interactive testing
        Scanner scanner = new Scanner(System.in);
        System.out.print("\n🎯 Try interactive mode? (y/n): ");
        if (scanner.nextLine().toLowerCase().startsWith("y")) {
            interactiveMode(agentConfig);
        }
        
        System.out.println("\n🎉 Sample completed successfully!");
        System.out.println("📚 This foundation supports Tutorial 2 (Governance) and Tutorial 3 (Production)");
        System.out.println("🔗 Next: Add evaluation metrics, monitoring, and production deployment");
        
        scanner.close();
    }
    
    // ============================================================================
    // HELPER CLASSES
    // ============================================================================
    
    public static class AgentConfiguration {
        public final Agent agent;
        public final McpTool mcpTool;
        public final SharepointTool sharepointTool;
        
        public AgentConfiguration(Agent agent, McpTool mcpTool, SharepointTool sharepointTool) {
            this.agent = agent;
            this.mcpTool = mcpTool;
            this.sharepointTool = sharepointTool;
        }
    }
    
    public static class BusinessScenario {
        public final String title;
        public final String question;
        public final String context;
        public final String expectedSource;
        public final String learningPoint;
        
        public BusinessScenario(String title, String question, String context, String expectedSource, String learningPoint) {
            this.title = title;
            this.question = question;
            this.context = context;
            this.expectedSource = expectedSource;
            this.learningPoint = learningPoint;
        }
    }
    
    public static class ChatResult {
        public final String content;
        public final String status;
        
        public ChatResult(String content, String status) {
            this.content = content;
            this.status = status;
        }
    }
}