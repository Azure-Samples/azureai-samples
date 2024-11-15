namespace ApprovalWithHumanInteraction.Functions
{
    using System;
    using System.Threading.Tasks;
    using Azure.Communication.Email;
    using Azure.Identity;
    using Azure;
    using Microsoft.AspNetCore.Http;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.Azure.WebJobs;
    using Microsoft.Azure.WebJobs.Extensions.DurableTask;
    using Microsoft.Azure.WebJobs.Extensions.Http;
    using Microsoft.Extensions.Logging;
    using Azure.Core;
    using System.Text.Json;

    public class WorkflowInput : Input
    {
        public string Approver { get; set; }
    }

    public class ApprovalCompleteArgs
    {
        public bool Approved { get; set; }
        public string CorrelationId { get; set; }
    }

    public class ApprovalWithHumanInteraction
    {
        const string INPUT_QUEUE = "agents-sample-approval-input";
        const string OUTPUT_QUEUE = "agents-sample-approval-output";
        static readonly string AZURE_COMMUNICATION_SERVICE_URI = Environment.GetEnvironmentVariable("AZURE_COMMUNICATION_SERVICE_URI");
        static readonly string APPROVAL_HTTP_TRIGGER_FUNCTION_URL = Environment.GetEnvironmentVariable("APPROVAL_HTTP_TRIGGER_FUNCTION_URL");

        [FunctionName(nameof(TriggerOrchestrator))]
        public static async Task TriggerOrchestrator(
            [QueueTrigger(INPUT_QUEUE, Connection = "QUEUECONNECTION")] WorkflowInput input,
            [DurableClient] IDurableOrchestrationClient durableOrchestrationClient,
            ILogger log)
        {
            // initiate the overall workflow by starting the orchestrator.
            var instanceId = await durableOrchestrationClient.StartNewAsync(nameof(WorklowOrchestrator), input);
            log.LogInformation($"Started orchestration instanceId: {instanceId}");
        }

        /// <summary>
        /// Orchestration function to start approval process
        /// </summary>
        [FunctionName(nameof(WorklowOrchestrator))]
        public static async Task WorklowOrchestrator(
            [OrchestrationTrigger] IDurableOrchestrationContext context,
            ILogger log)
        {
            log.LogInformation($"{nameof(WorklowOrchestrator)} triggered, orchestration instanceId: {context.InstanceId}");
            var workflowInput = context.GetInput<WorkflowInput>();

            // call activity function(s) to perform actual work
            await context.CallActivityAsync(nameof(StartApprovalAsync), workflowInput);

            // wait for the approval response
            var response = await context.WaitForExternalEvent<bool>("ApprovalResponse");

            log.LogInformation($"{nameof(WorklowOrchestrator)} ApprovalResponse received: {response}, orchestration instanceId: {context.InstanceId}");

            // complete the approval process
            await context.CallActivityAsync(
                nameof(CompleteApprovalAsync),
                new ApprovalCompleteArgs
                {
                    Approved = response,
                    CorrelationId = workflowInput.CorrelationId,
                });
        }

        /// <summary>
        /// Activity function to start approval process
        /// </summary>
        [FunctionName(nameof(StartApprovalAsync))]
        public static async Task StartApprovalAsync(
            [ActivityTrigger] IDurableActivityContext context,
            string instanceId,
            ILogger log)
        {
            log.LogInformation($"{nameof(StartApprovalAsync)} triggered, orchestration instanceId:{instanceId}");
            var workflowInput = context.GetInput<WorkflowInput>();

            // Send an email notification to the approver with a link to trigger the approval via the http trigger function.
            var credential = new DefaultAzureCredential();
            var emailClient = new EmailClient(new Uri(AZURE_COMMUNICATION_SERVICE_URI), credential);
            var baseApprovalUrl = $"{APPROVAL_HTTP_TRIGGER_FUNCTION_URL}";
            var approveCurlCommand = $@"curl -X POST {baseApprovalUrl} \
     -H ""Content-Type: application/json"" \
     -d '{{""instanceId"": ""{instanceId}"", ""approved"": true}}'";

            var denyCurlCommand = $@"curl -X POST {baseApprovalUrl} \
     -H ""Content-Type: application/json"" \
     -d '{{""instanceId"": ""{instanceId}"", ""approved"": false}}'";


            var emailMessage = new EmailMessage(
                senderAddress: "DoNotReply@b5ec5bee-db41-4759-8bbc-31594a5c909c.azurecomm.net",
                content: new EmailContent("Approval Request")
                {
                    Html = $@"
    <html>
    <body>
        <h2>Agents Approval Requested</h2>
        <p>We request your approval for the agent application.</p>
        <p>To approve, run the following command in your terminal:</p>
        <pre><code>{approveCurlCommand}</code></pre>

        <p>To deny, run the following command in your terminal:</p>
        <pre><code>{denyCurlCommand}</code></pre>

        <p>Thank you,</p>
        <p>Your Team</p>
    </body>
    </html>"
                },
                recipients: new EmailRecipients([new EmailAddress("pwiese@microsoft.com")]));


            await emailClient.SendAsync(
                WaitUntil.Completed,
                emailMessage);
        }

        [FunctionName(nameof(TriggerApproval))]
        public static async Task<IActionResult> TriggerApproval(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)] HttpRequest req,
            [DurableClient] IDurableOrchestrationClient durableOrchestrationClient,
            ILogger log)
        {
            // Ensure the request content is JSON
            if (req.ContentType == "application/json")
            {
                // Read the request body as a JSON document
                using var stream = req.Body;
                using var jsonDoc = await JsonDocument.ParseAsync(stream);

                // Access the top-level fields
                var root = jsonDoc.RootElement;
                if (root.TryGetProperty("instanceId", out var instanceIdElement) &&
                    root.TryGetProperty("approved", out var approvedElement))
                {
                    var  instanceId = instanceIdElement.GetString();
                    bool approved = approvedElement.GetBoolean();

                    log.LogInformation($"{nameof(TriggerApproval)} triggered, target orchestration instanceId:{instanceId}");
                    await durableOrchestrationClient.RaiseEventAsync(instanceId, "ApprovalResponse", approved);
                    return new OkObjectResult(new { Approved = approved });
                }
            }

            return new BadRequestResult();
        }

        /// <summary>
        /// Activity function to complete the approval process. This function writes the result to the output queue configured on the assistant.
        /// </summary>
        [FunctionName(nameof(CompleteApprovalAsync))]
        [return: Queue(OUTPUT_QUEUE, Connection = "QUEUECONNECTION")]
        public static Task<Response> CompleteApprovalAsync(
            [ActivityTrigger] IDurableActivityContext context,
            string instanceId,
            ILogger log)
        {
            log.LogInformation($"{nameof(CompleteApprovalAsync)} triggered, orchestration instanceId:{instanceId}");
            var approvalCompleteArgs = context.GetInput<ApprovalCompleteArgs>();

            // return the result to the output queue using the standard Response POCO.
            return Task.FromResult(new Response
            {
                Value = approvalCompleteArgs.Approved ? "APPROVED" : "DENIED",
                CorrelationId = approvalCompleteArgs.CorrelationId
            });
        }
    }
}