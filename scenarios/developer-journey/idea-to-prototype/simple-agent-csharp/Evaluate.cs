/**
 * Azure AI Foundry Agent Evaluation - Tutorial 1: Modern Workplace Assistant
 * 
 * This evaluation system demonstrates enterprise AI quality assurance patterns:
 * - Business-focused evaluation scenarios
 * - Multi-source knowledge validation (SharePoint + MCP)
 * - Response quality assessment
 * - Source attribution verification
 * - Performance and reliability measurement
 * 
 * Educational Focus:
 * - Shows how to evaluate enterprise AI systems
 * - Demonstrates quality metrics for business scenarios
 * - Provides foundation for governance and monitoring
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

namespace ModernWorkplaceAssistant.Evaluation
{
    public class EvaluationResult
    {
        public string Question { get; set; }
        public string Answer { get; set; }
        public string Status { get; set; }
        public List<string> Sources { get; set; } = new List<string>();
        public DateTime Timestamp { get; set; }
        public double ResponseTimeMs { get; set; }
        public string ExpectedSource { get; set; }
        public bool SourceMatch { get; set; }
    }
    
    public class TestQuestion
    {
        public string question { get; set; }
        public string expected_source { get; set; }
        public string category { get; set; }
    }
    
    public class AgentEvaluator
    {
        private readonly AIProjectClient projectClient;
        
        public AgentEvaluator()
        {
            // Load environment variables
            LoadEnvironmentVariables();
            
            var credential = new DefaultAzureCredential();
            projectClient = new AIProjectClient(
                new Uri(Environment.GetEnvironmentVariable("PROJECT_ENDPOINT")),
                credential
            );
        }
        
        private static void LoadEnvironmentVariables()
        {
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
        
        public async Task<List<EvaluationResult>> RunEvaluationAsync()
        {
            Console.WriteLine("🧪 Starting Modern Workplace Assistant Evaluation");
            Console.WriteLine("==================================================");
            
            // Load test questions
            var questions = await LoadTestQuestionsAsync();
            Console.WriteLine($"📝 Loaded {questions.Count} test questions");
            
            // Create agent for evaluation
            Console.WriteLine("🤖 Creating evaluation agent...");
            var agentConfig = await CreateWorkplaceAssistantAsync();
            
            var results = new List<EvaluationResult>();
            
            // Run evaluation for each question
            for (int i = 0; i < questions.Count; i++)
            {
                var question = questions[i];
                Console.WriteLine($"\n[{i + 1}/{questions.Count}] Testing: {question.category}");
                Console.WriteLine($"❓ Question: {question.question}");
                
                var result = await EvaluateQuestionAsync(agentConfig.Agent, question);
                results.Add(result);
                
                // Display result
                Console.WriteLine($"✅ Status: {result.Status}");
                Console.WriteLine($"⏱️  Response time: {result.ResponseTimeMs:F0}ms");
                Console.WriteLine($"📚 Sources found: {result.Sources.Count}");
                Console.WriteLine($"🎯 Expected source match: {(result.SourceMatch ? "✅" : "⚠️")}");
                
                if (result.Sources.Any())
                {
                    Console.WriteLine("   Sources:");
                    foreach (var source in result.Sources.Take(3))
                    {
                        Console.WriteLine($"   - {source}");
                    }
                }
            }
            
            // Display summary
            DisplayEvaluationSummary(results);
            
            // Cleanup
            await CleanupAgentAsync(agentConfig.Agent);
            
            return results;
        }
        
        private async Task<List<TestQuestion>> LoadTestQuestionsAsync()
        {
            var questionsFile = "questions.jsonl";
            if (!File.Exists(questionsFile))
            {
                throw new FileNotFoundException($"Test questions file not found: {questionsFile}");
            }
            
            var questions = new List<TestQuestion>();
            var lines = await File.ReadAllLinesAsync(questionsFile);
            
            foreach (var line in lines)
            {
                if (string.IsNullOrWhiteSpace(line))
                    continue;
                    
                try
                {
                    var question = JsonSerializer.Deserialize<TestQuestion>(line);
                    questions.Add(question);
                }
                catch (JsonException ex)
                {
                    Console.WriteLine($"⚠️  Failed to parse question: {line} - {ex.Message}");
                }
            }
            
            return questions;
        }
        
        private async Task<(Agent Agent, McpTool McpTool, SharepointTool SharepointTool)> CreateWorkplaceAssistantAsync()
        {
            // Create agent using the same logic as the main program
            var sharePointResourceName = Environment.GetEnvironmentVariable("SHAREPOINT_RESOURCE_NAME");
            SharepointTool sharePointTool = null;
            
            try
            {
                var sharePointConn = await projectClient.Connections.GetConnectionAsync(sharePointResourceName);
                sharePointTool = new SharepointTool(sharePointConn.Id);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"⚠️  SharePoint connection failed: {ex.Message}");
            }
            
            var mcpTool = new McpTool("microsoft_learn", Environment.GetEnvironmentVariable("MCP_SERVER_URL"));
            
            var instructions = sharePointTool != null
                ? "You are a Modern Workplace Assistant. Use SharePoint for company policies and Microsoft Learn for technical guidance. Always cite your sources."
                : "You are a Technical Assistant with Microsoft Learn access. Provide technical guidance and cite sources.";
            
            var tools = new List<ToolDefinition>();
            if (sharePointTool != null)
                tools.AddRange(sharePointTool.Definitions);
            tools.AddRange(mcpTool.Definitions);
            
            var agent = await projectClient.Agents.CreateAgentAsync(
                Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME"),
                name: "Evaluation Agent",
                instructions: instructions,
                tools: tools
            );
            
            return (agent, mcpTool, sharePointTool);
        }
        
        private async Task<EvaluationResult> EvaluateQuestionAsync(Agent agent, TestQuestion question)
        {
            var startTime = DateTime.UtcNow;
            var result = new EvaluationResult
            {
                Question = question.question,
                ExpectedSource = question.expected_source,
                Timestamp = startTime
            };
            
            try
            {
                // Create thread and run conversation
                var thread = await projectClient.Agents.CreateThreadAsync();
                
                await projectClient.Agents.CreateMessageAsync(thread.Id, MessageRole.User, question.question);
                var run = await projectClient.Agents.CreateRunAsync(thread.Id, agent.Id);
                
                // Wait for completion
                while (run.Status == RunStatus.InProgress || run.Status == RunStatus.Queued)
                {
                    await Task.Delay(1000);
                    run = await projectClient.Agents.GetRunAsync(thread.Id, run.Id);
                }
                
                var endTime = DateTime.UtcNow;
                result.ResponseTimeMs = (endTime - startTime).TotalMilliseconds;
                
                if (run.Status == RunStatus.Completed)
                {
                    var messages = await projectClient.Agents.GetMessagesAsync(thread.Id);
                    var assistantMessage = messages.Value
                        .Where(m => m.Role == MessageRole.Assistant)
                        .OrderByDescending(m => m.CreatedAt)
                        .FirstOrDefault();
                    
                    if (assistantMessage != null)
                    {
                        result.Answer = assistantMessage.Content.FirstOrDefault()?.Text ?? "";
                        result.Status = "Completed";
                        
                        // Extract sources from response
                        result.Sources = ExtractSourcesFromResponse(result.Answer);
                        result.SourceMatch = CheckSourceMatch(result.Sources, question.expected_source);
                    }
                    else
                    {
                        result.Status = "No response";
                    }
                }
                else
                {
                    result.Status = $"Failed: {run.Status}";
                }
                
                // Cleanup thread
                await projectClient.Agents.DeleteThreadAsync(thread.Id);
            }
            catch (Exception ex)
            {
                result.Status = $"Error: {ex.Message}";
            }
            
            return result;
        }
        
        private List<string> ExtractSourcesFromResponse(string response)
        {
            var sources = new List<string>();
            
            // Look for common source indicators
            var sourceIndicators = new[] { "SharePoint", "Microsoft Learn", "learn.microsoft.com", "documentation" };
            
            foreach (var indicator in sourceIndicators)
            {
                if (response.Contains(indicator, StringComparison.OrdinalIgnoreCase))
                {
                    sources.Add(indicator);
                }
            }
            
            return sources.Distinct().ToList();
        }
        
        private bool CheckSourceMatch(List<string> foundSources, string expectedSource)
        {
            if (string.IsNullOrEmpty(expectedSource))
                return true;
                
            return foundSources.Any(source => 
                source.Contains(expectedSource, StringComparison.OrdinalIgnoreCase) ||
                expectedSource.Contains(source, StringComparison.OrdinalIgnoreCase));
        }
        
        private void DisplayEvaluationSummary(List<EvaluationResult> results)
        {
            Console.WriteLine("\n📊 EVALUATION SUMMARY");
            Console.WriteLine("=====================");
            
            var successful = results.Count(r => r.Status == "Completed");
            var avgResponseTime = results.Where(r => r.Status == "Completed")
                .Average(r => r.ResponseTimeMs);
            var sourceMatches = results.Count(r => r.SourceMatch);
            
            Console.WriteLine($"✅ Successful responses: {successful}/{results.Count} ({100.0 * successful / results.Count:F1}%)");
            Console.WriteLine($"⏱️  Average response time: {avgResponseTime:F0}ms");
            Console.WriteLine($"🎯 Source attribution accuracy: {sourceMatches}/{results.Count} ({100.0 * sourceMatches / results.Count:F1}%)");
            
            // Show failed cases
            var failed = results.Where(r => r.Status != "Completed").ToList();
            if (failed.Any())
            {
                Console.WriteLine("\n⚠️ Failed Cases:");
                foreach (var fail in failed)
                {
                    Console.WriteLine($"   - {fail.Question}: {fail.Status}");
                }
            }
        }
        
        private async Task CleanupAgentAsync(Agent agent)
        {
            try
            {
                await projectClient.Agents.DeleteAgentAsync(agent.Id);
                Console.WriteLine("🧹 Cleanup completed");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"⚠️ Cleanup warning: {ex.Message}");
            }
        }
    }
    
    // Entry point for evaluation
    public class EvaluationProgram
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine("Azure AI Foundry - Modern Workplace Assistant Evaluation");
            Console.WriteLine("========================================================");
            
            try
            {
                var evaluator = new AgentEvaluator();
                var results = await evaluator.RunEvaluationAsync();
                
                Console.WriteLine($"\n🎉 Evaluation completed with {results.Count} test cases");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Evaluation failed: {ex.Message}");
                Environment.Exit(1);
            }
        }
    }
}