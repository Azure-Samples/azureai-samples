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

import { AIProjectClient } from '@azure/ai-projects';
import { DefaultAzureCredential } from '@azure/identity';
import { Agent, SharepointTool, McpTool } from '@azure/ai-agents';
import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

interface TestQuestion {
    question: string;
    expected_source: string;
    category: string;
}

interface EvaluationResult {
    question: string;
    answer: string;
    status: string;
    sources: string[];
    timestamp: Date;
    responseTimeMs: number;
    expectedSource: string;
    sourceMatch: boolean;
}

interface AgentConfiguration {
    agent: Agent;
    mcpTool: McpTool;
    sharepointTool: SharepointTool | null;
}

class AgentEvaluator {
    private projectClient: AIProjectClient;
    
    constructor() {
        // Setup authentication
        const credential = new DefaultAzureCredential();
        this.projectClient = new AIProjectClient(
            process.env.PROJECT_ENDPOINT!,
            credential
        );
    }
    
    async runEvaluation(): Promise<EvaluationResult[]> {
        console.log('🧪 Starting Modern Workplace Assistant Evaluation');
        console.log('==================================================');
        
        // Load test questions
        const questions = await this.loadTestQuestions();
        console.log(`📝 Loaded ${questions.length} test questions`);
        
        // Create agent for evaluation
        console.log('🤖 Creating evaluation agent...');
        const agentConfig = await this.createWorkplaceAssistant();
        
        const results: EvaluationResult[] = [];
        
        // Run evaluation for each question
        for (let i = 0; i < questions.length; i++) {
            const question = questions[i];
            console.log(`\n[${i + 1}/${questions.length}] Testing: ${question.category}`);
            console.log(`❓ Question: ${question.question}`);
            
            const result = await this.evaluateQuestion(agentConfig.agent, question);
            results.push(result);
            
            // Display result
            console.log(`✅ Status: ${result.status}`);
            console.log(`⏱️  Response time: ${result.responseTimeMs.toFixed(0)}ms`);
            console.log(`📚 Sources found: ${result.sources.length}`);
            console.log(`🎯 Expected source match: ${result.sourceMatch ? '✅' : '⚠️'}`);
            
            if (result.sources.length > 0) {
                console.log('   Sources:');
                result.sources.slice(0, 3).forEach(source => {
                    console.log(`   - ${source}`);
                });
            }
        }
        
        // Display summary
        this.displayEvaluationSummary(results);
        
        // Cleanup
        await this.cleanupAgent(agentConfig.agent);
        
        return results;
    }
    
    private async loadTestQuestions(): Promise<TestQuestion[]> {
        const questionsFile = 'questions.jsonl';
        if (!fs.existsSync(questionsFile)) {
            throw new Error(`Test questions file not found: ${questionsFile}`);
        }
        
        const questions: TestQuestion[] = [];
        const content = fs.readFileSync(questionsFile, 'utf-8');
        const lines = content.split('\n').filter(line => line.trim());
        
        for (const line of lines) {
            try {
                const question = JSON.parse(line) as TestQuestion;
                questions.push(question);
            } catch (error) {
                console.log(`⚠️  Failed to parse question: ${line} - ${error}`);
            }
        }
        
        return questions;
    }
    
    private async createWorkplaceAssistant(): Promise<AgentConfiguration> {
        // Create agent using the same logic as the main program
        const sharePointResourceName = process.env.SHAREPOINT_RESOURCE_NAME!;
        let sharePointTool: SharepointTool | null = null;
        
        try {
            const sharePointConn = await this.projectClient.connections.get(sharePointResourceName);
            sharePointTool = new SharepointTool(sharePointConn.id);
            console.log('✅ SharePoint tool configured');
        } catch (error) {
            console.log(`⚠️  SharePoint connection failed: ${error}`);
        }
        
        const mcpTool = new McpTool({
            serverLabel: 'microsoft_learn',
            serverUrl: process.env.MCP_SERVER_URL!,
            allowedTools: []
        });
        
        const instructions = sharePointTool 
            ? 'You are a Modern Workplace Assistant. Use SharePoint for company policies and Microsoft Learn for technical guidance. Always cite your sources.'
            : 'You are a Technical Assistant with Microsoft Learn access. Provide technical guidance and cite sources.';
        
        const tools = [];
        if (sharePointTool) {
            tools.push(...sharePointTool.definitions);
        }
        tools.push(...mcpTool.definitions);
        
        const agent = await this.projectClient.agents.createAgent({
            model: process.env.MODEL_DEPLOYMENT_NAME!,
            name: 'Evaluation Agent',
            instructions,
            tools
        });
        
        return { agent, mcpTool, sharepointTool: sharePointTool };
    }
    
    private async evaluateQuestion(agent: Agent, question: TestQuestion): Promise<EvaluationResult> {
        const startTime = Date.now();
        const result: EvaluationResult = {
            question: question.question,
            answer: '',
            status: '',
            sources: [],
            timestamp: new Date(),
            responseTimeMs: 0,
            expectedSource: question.expected_source,
            sourceMatch: false
        };
        
        try {
            // Create thread and run conversation
            const thread = await this.projectClient.agents.createThread();
            
            await this.projectClient.agents.createMessage(thread.id, {
                role: 'user',
                content: question.question
            });
            
            let run = await this.projectClient.agents.createRun(thread.id, {
                assistantId: agent.id
            });
            
            // Wait for completion
            while (run.status === 'in_progress' || run.status === 'queued') {
                await new Promise(resolve => setTimeout(resolve, 1000));
                run = await this.projectClient.agents.getRun(thread.id, run.id);
            }
            
            const endTime = Date.now();
            result.responseTimeMs = endTime - startTime;
            
            if (run.status === 'completed') {
                const messages = await this.projectClient.agents.getMessages(thread.id);
                const assistantMessage = messages.data
                    .filter(m => m.role === 'assistant')
                    .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())[0];
                
                if (assistantMessage && assistantMessage.content[0]?.text) {
                    result.answer = assistantMessage.content[0].text.value;
                    result.status = 'Completed';
                    
                    // Extract sources from response
                    result.sources = this.extractSourcesFromResponse(result.answer);
                    result.sourceMatch = this.checkSourceMatch(result.sources, question.expected_source);
                } else {
                    result.status = 'No response';
                }
            } else {
                result.status = `Failed: ${run.status}`;
            }
            
            // Cleanup thread
            await this.projectClient.agents.deleteThread(thread.id);
        } catch (error) {
            result.status = `Error: ${error}`;
        }
        
        return result;
    }
    
    private extractSourcesFromResponse(response: string): string[] {
        const sources: string[] = [];
        
        // Look for common source indicators
        const sourceIndicators = ['SharePoint', 'Microsoft Learn', 'learn.microsoft.com', 'documentation'];
        
        for (const indicator of sourceIndicators) {
            if (response.toLowerCase().includes(indicator.toLowerCase())) {
                sources.push(indicator);
            }
        }
        
        return Array.from(new Set(sources));
    }
    
    private checkSourceMatch(foundSources: string[], expectedSource: string): boolean {
        if (!expectedSource) return true;
        
        return foundSources.some(source => 
            source.toLowerCase().includes(expectedSource.toLowerCase()) ||
            expectedSource.toLowerCase().includes(source.toLowerCase())
        );
    }
    
    private displayEvaluationSummary(results: EvaluationResult[]): void {
        console.log('\n📊 EVALUATION SUMMARY');
        console.log('=====================');
        
        const successful = results.filter(r => r.status === 'Completed').length;
        const avgResponseTime = results
            .filter(r => r.status === 'Completed')
            .reduce((sum, r) => sum + r.responseTimeMs, 0) / successful || 0;
        const sourceMatches = results.filter(r => r.sourceMatch).length;
        
        console.log(`✅ Successful responses: ${successful}/${results.length} (${(100.0 * successful / results.length).toFixed(1)}%)`);
        console.log(`⏱️  Average response time: ${avgResponseTime.toFixed(0)}ms`);
        console.log(`🎯 Source attribution accuracy: ${sourceMatches}/${results.length} (${(100.0 * sourceMatches / results.length).toFixed(1)}%)`);
        
        // Show failed cases
        const failed = results.filter(r => r.status !== 'Completed');
        if (failed.length > 0) {
            console.log('\n⚠️ Failed Cases:');
            failed.forEach(fail => {
                console.log(`   - ${fail.question}: ${fail.status}`);
            });
        }
    }
    
    private async cleanupAgent(agent: Agent): Promise<void> {
        try {
            await this.projectClient.agents.deleteAgent(agent.id);
            console.log('🧹 Cleanup completed');
        } catch (error) {
            console.log(`⚠️ Cleanup warning: ${error}`);
        }
    }
}

// Entry point for evaluation
async function main(): Promise<void> {
    console.log('Azure AI Foundry - Modern Workplace Assistant Evaluation');
    console.log('========================================================');
    
    try {
        const evaluator = new AgentEvaluator();
        const results = await evaluator.runEvaluation();
        
        console.log(`\n🎉 Evaluation completed with ${results.length} test cases`);
    } catch (error) {
        console.log(`❌ Evaluation failed: ${error}`);
        process.exit(1);
    }
}

// Run if this file is executed directly
if (require.main === module) {
    main().catch(console.error);
}