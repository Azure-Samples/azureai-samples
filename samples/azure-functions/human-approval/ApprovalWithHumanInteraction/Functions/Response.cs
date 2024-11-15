namespace ApprovalWithHumanInteraction.Functions
{
    /// <summary>
    /// All Azure Functions that participate in the Agents framework must return a json serializable response object that contains these values.
    /// </summary>
    /// <remarks>This is a REQUIRED class structure</remarks>
    public class Response
    {
        /// <summary>
        /// This value is fed back to the model as the tool's response.
        /// </summary>
        public string Value { get; set; }

        /// <summary>
        /// An opaque internal identifier that is used to correlate the response with the request.
        /// </summary>
        public string CorrelationId { get; set; }
    }
}