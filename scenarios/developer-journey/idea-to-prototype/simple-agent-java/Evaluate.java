/**
 * Azure AI Foundry Evaluation Sample - Tutorial 1
 * 
 * This sample demonstrates comprehensive evaluation of AI agents in business contexts.
 * It evaluates both technical accuracy and business value alignment, providing
 * metrics that matter for enterprise AI deployments.
 * 
 * Educational Focus:
 * - Business-focused evaluation metrics beyond technical accuracy
 * - Comprehensive response quality assessment
 * - Foundation for Tutorial 2 (governance) evaluation frameworks
 * - Real-world quality assurance patterns
 * 
 * Business Context:
 * Evaluates the Modern Workplace Assistant's ability to:
 * 1. Retrieve accurate company policy information
 * 2. Provide current technical implementation guidance
 * 3. Combine internal requirements with external best practices
 * 4. Deliver actionable guidance for business scenarios
 */

import com.azure.ai.projects.AIProjectClient;
import com.azure.ai.projects.AIProjectClientBuilder;
import com.azure.ai.agents.models.*;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.AzureCliCredential;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;

public class Evaluate {
    
    // ============================================================================
    // EVALUATION CONFIGURATION
    // ============================================================================
    
    private static final Properties config = new Properties();
    private static AIProjectClient projectClient;
    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    // Business-focused evaluation criteria
    private static final String[] POLICY_KEYWORDS = {
        "security", "authentication", "authorization", "compliance", 
        "governance", "remote work", "access control", "MFA", "multi-factor"
    };
    
    private static final String[] TECHNICAL_KEYWORDS = {
        "Azure", "configuration", "implementation", "setup", "deployment",
        "Active Directory", "Conditional Access", "PowerShell", "portal"
    };
    
    static {
        try {
            loadEnvironmentConfig();
            setupAuthentication();
        } catch (Exception e) {
            System.err.println("Failed to initialize evaluation configuration: " + e.getMessage());
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
        String tenantId = config.getProperty("AI_FOUNDRY_TENANT_ID");
        
        if (tenantId != null && !tenantId.isEmpty()) {
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
     * Load test questions from JSONL file.
     * 
     * Educational Value:
     * - Shows standardized evaluation data format
     * - Demonstrates systematic testing approach
     * - Provides reproducible evaluation scenarios
     */
    public static List<TestQuestion> loadTestQuestions() throws IOException {
        List<TestQuestion> questions = new ArrayList<>();
        
        if (!Files.exists(Paths.get("questions.jsonl"))) {
            System.out.println("⚠️  questions.jsonl not found, using default test questions");
            return getDefaultTestQuestions();
        }
        
        List<String> lines = Files.readAllLines(Paths.get("questions.jsonl"));
        for (String line : lines) {
            if (!line.trim().isEmpty()) {
                try {
                    JsonNode node = objectMapper.readTree(line);
                    questions.add(new TestQuestion(
                        node.get("question").asText(),
                        node.get("category").asText(),
                        node.get("expected_sources").asText(),
                        node.get("context").asText()
                    ));
                } catch (Exception e) {
                    System.out.println("⚠️  Failed to parse question: " + line);
                }
            }
        }
        
        return questions;
    }
    
    private static List<TestQuestion> getDefaultTestQuestions() {
        return Arrays.asList(
            new TestQuestion(
                "What is our company policy on remote work security requirements?",
                "policy",
                "sharepoint",
                "Employee needs to understand security requirements for remote work"
            ),
            new TestQuestion(
                "How do I configure Azure AD multi-factor authentication?",
                "technical",
                "mcp",  
                "IT administrator needs step-by-step MFA setup instructions"
            ),
            new TestQuestion(
                "Our security policy requires MFA for all remote access. How do I implement this in Azure AD?",
                "implementation",
                "both",
                "Combining company policy requirements with technical implementation steps"
            ),
            new TestQuestion(
                "What are the latest Azure Conditional Access best practices?",
                "technical",
                "mcp",
                "IT team needs current best practices for security configuration"
            )
        );
    }
    
    /**
     * Evaluate response quality using comprehensive business metrics.
     * 
     * This evaluation goes beyond simple accuracy to assess business value,
     * practical applicability, and enterprise readiness.
     * 
     * Educational Value:
     * - Shows multi-dimensional evaluation approach
     * - Demonstrates business-relevant quality metrics
     * - Provides foundation for governance and monitoring
     */
    public static EvaluationResult evaluateResponse(TestQuestion question, String response, long responseTimeMs) {
        EvaluationResult result = new EvaluationResult();
        result.question = question.question;
        result.category = question.category;
        result.response = response;
        result.responseTimeMs = responseTimeMs;
        
        // ====================================================================
        // BUSINESS VALUE ASSESSMENT
        // ====================================================================
        
        // 1. Completeness: Does the response address all aspects of the question?
        result.completenessScore = evaluateCompleteness(question, response);
        
        // 2. Accuracy: Is the information technically correct and current?
        result.accuracyScore = evaluateAccuracy(question, response);
        
        // 3. Actionability: Can the user take concrete next steps?
        result.actionabilityScore = evaluateActionability(response);
        
        // 4. Source Integration: Does it properly combine internal/external sources?
        result.sourceIntegrationScore = evaluateSourceIntegration(question, response);
        
        // 5. Business Context: Does it understand enterprise requirements?
        result.businessContextScore = evaluateBusinessContext(question, response);
        
        // ====================================================================
        // PERFORMANCE METRICS
        // ====================================================================
        
        // Response time evaluation (important for user experience)
        if (responseTimeMs < 5000) {
            result.performanceScore = 1.0;
        } else if (responseTimeMs < 10000) {
            result.performanceScore = 0.8;
        } else if (responseTimeMs < 20000) {
            result.performanceScore = 0.6;
        } else {
            result.performanceScore = 0.3;
        }
        
        // ====================================================================
        // OVERALL QUALITY SCORE
        // ====================================================================
        
        // Weighted average emphasizing business value
        result.overallScore = (
            result.completenessScore * 0.25 +      // Must answer the full question
            result.accuracyScore * 0.20 +          // Must be technically correct
            result.actionabilityScore * 0.20 +     // Must provide actionable guidance
            result.sourceIntegrationScore * 0.15 + // Must combine sources appropriately
            result.businessContextScore * 0.15 +   // Must understand business context
            result.performanceScore * 0.05         // Must perform reasonably
        );
        
        // Grade assignment for easy interpretation
        if (result.overallScore >= 0.9) {
            result.grade = "A";
        } else if (result.overallScore >= 0.8) {
            result.grade = "B";
        } else if (result.overallScore >= 0.7) {
            result.grade = "C";
        } else if (result.overallScore >= 0.6) {
            result.grade = "D";
        } else {
            result.grade = "F";
        }
        
        return result;
    }
    
    private static double evaluateCompleteness(TestQuestion question, String response) {
        if (response == null || response.trim().isEmpty()) return 0.0;
        
        // Check if response addresses key aspects based on question category
        double score = 0.5; // Base score for any response
        
        if (question.category.equals("policy") && 
            Arrays.stream(POLICY_KEYWORDS).anyMatch(kw -> 
                response.toLowerCase().contains(kw.toLowerCase()))) {
            score += 0.3;
        }
        
        if (question.category.equals("technical") && 
            Arrays.stream(TECHNICAL_KEYWORDS).anyMatch(kw -> 
                response.toLowerCase().contains(kw.toLowerCase()))) {
            score += 0.3;
        }
        
        if (question.category.equals("implementation") && 
            Arrays.stream(POLICY_KEYWORDS).anyMatch(kw -> 
                response.toLowerCase().contains(kw.toLowerCase())) &&
            Arrays.stream(TECHNICAL_KEYWORDS).anyMatch(kw -> 
                response.toLowerCase().contains(kw.toLowerCase()))) {
            score += 0.4;
        }
        
        // Length-based completeness (reasonable explanations should be substantial)
        if (response.length() > 200) score += 0.2;
        
        return Math.min(1.0, score);
    }
    
    private static double evaluateAccuracy(TestQuestion question, String response) {
        if (response == null || response.trim().isEmpty()) return 0.0;
        
        // Base accuracy assessment (would be enhanced with domain-specific validation)
        double score = 0.6; // Assume reasonable accuracy for non-empty responses
        
        // Check for structured information (lists, steps, examples)
        if (response.contains("1.") || response.contains("•") || response.contains("-")) {
            score += 0.2;
        }
        
        // Check for specific technical terms that indicate detailed knowledge
        if (question.category.equals("technical") || question.category.equals("implementation")) {
            if (response.toLowerCase().contains("azure") && 
                response.toLowerCase().contains("active directory")) {
                score += 0.2;
            }
        }
        
        return Math.min(1.0, score);
    }
    
    private static double evaluateActionability(String response) {
        if (response == null || response.trim().isEmpty()) return 0.0;
        
        double score = 0.0;
        
        // Check for actionable elements
        if (response.contains("step") || response.contains("Step")) score += 0.3;
        if (response.contains("1.") || response.contains("2.")) score += 0.3;
        if (response.contains("configure") || response.contains("set up") || 
            response.contains("implement")) score += 0.2;
        if (response.contains("portal") || response.contains("PowerShell") || 
            response.contains("command")) score += 0.2;
        
        return Math.min(1.0, score);
    }
    
    private static double evaluateSourceIntegration(TestQuestion question, String response) {
        if (response == null || response.trim().isEmpty()) return 0.0;
        
        double score = 0.5; // Base score
        
        // Check if response appropriately uses expected sources
        if (question.expectedSources.contains("sharepoint") && 
            (response.toLowerCase().contains("policy") || 
             response.toLowerCase().contains("company") ||
             response.toLowerCase().contains("internal"))) {
            score += 0.25;
        }
        
        if (question.expectedSources.contains("mcp") && 
            (response.toLowerCase().contains("microsoft") || 
             response.toLowerCase().contains("azure") ||
             response.toLowerCase().contains("documentation"))) {
            score += 0.25;
        }
        
        return Math.min(1.0, score);
    }
    
    private static double evaluateBusinessContext(TestQuestion question, String response) {
        if (response == null || response.trim().isEmpty()) return 0.0;
        
        double score = 0.4; // Base score
        
        // Check for business awareness
        if (response.toLowerCase().contains("enterprise") || 
            response.toLowerCase().contains("organization") ||
            response.toLowerCase().contains("company")) {
            score += 0.2;
        }
        
        // Check for security/compliance awareness
        if (response.toLowerCase().contains("security") || 
            response.toLowerCase().contains("compliance") ||
            response.toLowerCase().contains("governance")) {
            score += 0.2;
        }
        
        // Check for practical considerations
        if (response.toLowerCase().contains("user") || 
            response.toLowerCase().contains("administrator") ||
            response.toLowerCase().contains("deployment")) {
            score += 0.2;
        }
        
        return Math.min(1.0, score);
    }
    
    /**
     * Execute evaluation against the workplace assistant.
     * 
     * This runs the complete evaluation suite and provides comprehensive
     * business-focused metrics for the AI agent's performance.
     */
    public static void runEvaluation() {
        System.out.println("🔬 Azure AI Foundry - Agent Evaluation");
        System.out.println("Tutorial 1: Comprehensive Business-Focused Evaluation");
        System.out.println("=".repeat(60));
        
        try {
            // Create the agent (reusing Main class logic)
            Main.AgentConfiguration agentConfig = Main.createWorkplaceAssistant();
            
            // Load test questions
            List<TestQuestion> questions = loadTestQuestions();
            System.out.println("📋 Loaded " + questions.size() + " test questions");
            
            // Run evaluation
            List<EvaluationResult> results = new ArrayList<>();
            
            for (int i = 0; i < questions.size(); i++) {
                TestQuestion question = questions.get(i);
                System.out.println(String.format("\n🧪 Test %d/%d: %s", 
                    i + 1, questions.size(), question.category.toUpperCase()));
                System.out.println("❓ " + question.question);
                
                // Measure response time
                long startTime = System.currentTimeMillis();
                Main.ChatResult response = Main.chatWithAssistant(
                    agentConfig.agent.getId(), 
                    agentConfig.mcpTool, 
                    question.question
                );
                long responseTime = System.currentTimeMillis() - startTime;
                
                // Evaluate response
                EvaluationResult result = evaluateResponse(question, response.content, responseTime);
                results.add(result);
                
                // Display immediate results
                System.out.println(String.format("📊 Grade: %s (%.2f) | Time: %dms", 
                    result.grade, result.overallScore, result.responseTimeMs));
                System.out.println("-".repeat(50));
            }
            
            // Generate comprehensive report
            generateEvaluationReport(results);
            
        } catch (Exception e) {
            System.err.println("❌ Evaluation failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Generate comprehensive evaluation report with business insights.
     * 
     * Educational Value:
     * - Shows how to present evaluation results for business stakeholders
     * - Demonstrates actionable insights from evaluation data
     * - Provides foundation for continuous improvement processes
     */
    private static void generateEvaluationReport(List<EvaluationResult> results) {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("📈 COMPREHENSIVE EVALUATION REPORT");
        System.out.println("=".repeat(60));
        
        // Overall statistics
        double avgScore = results.stream().mapToDouble(r -> r.overallScore).average().orElse(0.0);
        long avgResponseTime = (long) results.stream().mapToLong(r -> r.responseTimeMs).average().orElse(0.0);
        
        Map<String, Long> gradeDistribution = results.stream()
            .collect(Collectors.groupingBy(r -> r.grade, Collectors.counting()));
        
        System.out.println("🎯 OVERALL PERFORMANCE:");
        System.out.println(String.format("   Average Score: %.2f", avgScore));
        System.out.println(String.format("   Average Response Time: %dms", avgResponseTime));
        System.out.println("   Grade Distribution: " + gradeDistribution);
        
        // Category-specific analysis
        Map<String, List<EvaluationResult>> byCategory = results.stream()
            .collect(Collectors.groupingBy(r -> r.category));
        
        System.out.println("\n📊 CATEGORY ANALYSIS:");
        for (Map.Entry<String, List<EvaluationResult>> entry : byCategory.entrySet()) {
            String category = entry.getKey();
            List<EvaluationResult> categoryResults = entry.getValue();
            double categoryAvg = categoryResults.stream().mapToDouble(r -> r.overallScore).average().orElse(0.0);
            
            System.out.println(String.format("   %s: %.2f average (%d questions)", 
                category.toUpperCase(), categoryAvg, categoryResults.size()));
        }
        
        // Detailed metrics breakdown
        System.out.println("\n🔍 DETAILED METRICS:");
        double avgCompleteness = results.stream().mapToDouble(r -> r.completenessScore).average().orElse(0.0);
        double avgAccuracy = results.stream().mapToDouble(r -> r.accuracyScore).average().orElse(0.0);
        double avgActionability = results.stream().mapToDouble(r -> r.actionabilityScore).average().orElse(0.0);
        double avgSourceIntegration = results.stream().mapToDouble(r -> r.sourceIntegrationScore).average().orElse(0.0);
        double avgBusinessContext = results.stream().mapToDouble(r -> r.businessContextScore).average().orElse(0.0);
        double avgPerformance = results.stream().mapToDouble(r -> r.performanceScore).average().orElse(0.0);
        
        System.out.println(String.format("   Completeness: %.2f", avgCompleteness));
        System.out.println(String.format("   Accuracy: %.2f", avgAccuracy));
        System.out.println(String.format("   Actionability: %.2f", avgActionability));
        System.out.println(String.format("   Source Integration: %.2f", avgSourceIntegration));
        System.out.println(String.format("   Business Context: %.2f", avgBusinessContext));
        System.out.println(String.format("   Performance: %.2f", avgPerformance));
        
        // Business insights and recommendations
        System.out.println("\n💡 BUSINESS INSIGHTS:");
        if (avgScore >= 0.8) {
            System.out.println("   ✅ Agent demonstrates strong enterprise readiness");
            System.out.println("   ✅ Suitable for pilot deployment with monitoring");
        } else if (avgScore >= 0.7) {
            System.out.println("   ⚠️  Agent shows promise but needs improvement");
            System.out.println("   ⚠️  Recommend additional training before deployment");
        } else {
            System.out.println("   ❌ Agent requires significant improvement");
            System.out.println("   ❌ Not ready for production deployment");
        }
        
        if (avgResponseTime > 10000) {
            System.out.println("   ⚠️  Response times may impact user experience");
            System.out.println("   💡 Recommend performance optimization");
        }
        
        System.out.println("\n🚀 NEXT STEPS:");
        System.out.println("   📚 Tutorial 2: Implement governance and monitoring");
        System.out.println("   🔄 Tutorial 3: Production deployment and scaling");
        System.out.println("   📊 Use these metrics to track improvement over time");
        
        System.out.println("\n" + "=".repeat(60));
    }
    
    public static void main(String[] args) {
        runEvaluation();
    }
    
    // ============================================================================
    // HELPER CLASSES
    // ============================================================================
    
    public static class TestQuestion {
        public final String question;
        public final String category;
        public final String expectedSources;
        public final String context;
        
        public TestQuestion(String question, String category, String expectedSources, String context) {
            this.question = question;
            this.category = category;
            this.expectedSources = expectedSources;
            this.context = context;
        }
    }
    
    public static class EvaluationResult {
        public String question;
        public String category;
        public String response;
        public long responseTimeMs;
        
        // Quality metrics
        public double completenessScore;
        public double accuracyScore;
        public double actionabilityScore;
        public double sourceIntegrationScore;
        public double businessContextScore;
        public double performanceScore;
        
        // Overall assessment
        public double overallScore;
        public String grade;
    }
}