### Tracing using Application Insights

Reasoning about your agent executions is important for troubleshooting and debugging. However, it can be difficult for complex agents for a number of reasons:
* There could be a high number of steps, making it hard to keep track of all of them.
* The sequence of steps could vary based on user input.
* The inputs/outputs at each stage may be long and deserve more detailed inspection.
* Each step of an agent might also involve nesting — for example, an agent might invoke a tool, which uses another process, which then invokes another tool. If you notice strange or incorrect output from a top-level agent run, it is difficult to determine exactly where in the execution it was introduced.

Tracing solves this by allowing you to clearly see the inputs and outputs of each primitive involved in a particular agent run, in the order in which they were invoked.

Tracing lets you analyze your agent's performance and behavior by using OpenTelemetry and adding an Application Insights Azure resource to your Azure AI Studio project. See the Tracing tab in your [AI studio](https://ai.azure.com/) project page. If one was enabled, you can get the Application Insights connection string, configure your Agents, and observe the full execution path through Azure Monitor. Typically, you might want to start tracing before you create an Agent.

#### Installation

Make sure to install OpenTelemetry and the Azure SDK tracing plugin:

```bash
pip install opentelemetry
pip install azure-core-tracing-opentelemetry
```

You will also need an exporter to send telemetry to your observability backend. You can print traces to the console or use a local viewer such as [Aspire Dashboard](https://learn.microsoft.com/dotnet/aspire/fundamentals/dashboard/standalone?tabs=bash).

To connect to Aspire Dashboard or another OpenTelemetry compatible backend, install the OTLP exporter:

```bash
pip install opentelemetry-exporter-otlp
```

These samples are broken into asynchronous and synchronous samples. From there, each sample has two versions, one that traces and displays the results locally in the console, and one that sends the traces to the Azure Monitor in AI Studio. Navigate to the to the 'Tracing' tab in your AI Studio project page to enable the second set of samples.

Note: the initial release of Azure AI Projects has a bug in the agents tracing functionality. The bug will cause agent function tool call related info (function names and parameter values, which could contain sensitive information) to be included in the traces even when content recoding is not enabled. We are working to fix this issue.