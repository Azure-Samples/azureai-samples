### Tracing using Application Insights

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

These samples are broken into asynchronous and synchrounous samples. From there, each sample has two versions, one that traces and displays the results locally in the console, and one that sends the traces to the Azure Monitor in AI Studio. Navigate to the to the 'Tracing' tab in your AI Studio project page to enable the second set of samples.