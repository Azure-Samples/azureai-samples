namespace ApprovalWithHumanInteraction.Functions
{
    /// <summary>
    /// All Azure Functions that participate in the Agents framework must accept a json serializable input object that contains an opaque string named CorrelationId.
    /// </summary>
    /// <remarks>This is a REQUIRED class structure</remarks>
    public abstract class Input
    {
        /// <summary>
        /// An opaque internal identifier that is used to correlate the response with the request.
        /// </summary>
        public string CorrelationId { get; set; }
    }
}