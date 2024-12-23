---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Evaluate.
---

## Simulate Evaluation (Test) Data 



Relevant, robust evaluation data is essential for effective evaluations. This data can be generated manually, can include production data, or can be assembled with the help of AI. There are two main types of evaluation data: 

- Bring Your Own Data: You can create and update a “golden dataset” with realistic customer questions or inputs paired with expert answers, ensuring quality for generative AI experiences. This dataset can also include samples from production data, offering a realistic evaluation dataset derived from actual queries your AI application has encountered. 
* Simulators: If evaluation data is not available, simulators can play a crucial role in generating evaluation data by creating both topic-related and adversarial queries.  
    - Context-related simulators test the AI system’s ability to handle relevant interactions within a specific context, ensuring it performs well under typical use scenarios.  

    - Adversarial simulators, on the other hand, generate queries designed to challenge the AI system, mimicking potential security threats or attempting to provoke undesirable behaviors. This approach helps identify the model's limitations and prepares it to perform well in unexpected or hostile conditions.  

Azure AI Studio provides tools for both topic-related and adversarial simulations, enabling comprehensive evaluation and enhancing confidence in deployment. For topic-related simulations, Azure AI enables you to simulate relevant conversations using [your data](Simulate_Context-Relevant_Data/Simulate_From_Input_Text/Simulate_From_Input_Text.ipynb), [your Azure Search Index](Simulate_Context-Relevant_Data/Simulate_From_Azure_Search_Index/Simulate_From_Azure_Search_Index.ipynb), or [your pre-defined conversation starters](Simulate_Context-Relevant_Data/Simulate_From_Conversation_Starter/Simulate_From_Conversation_Starter.ipynb).

