## Adversarial simulation

Augment and accelerate your red-teaming operation by leveraging Azure AI Studio safety evaluations to generate an adversarial dataset against your application. We provide adversarial tasks and profiles along with access to an Azure Open AI GPT-4 model with safety behaviors turned off to enable the adversarial simulation.

The simulator uses a set of adversarial prompt templates, hosted in the service, to simulate against your target application or endpoint for the following scenarios with the maximum number of simulations we provide:

| Task type                     | Template name                | Maximum number of simulations | Use this dataset for evaluating |
|-------------------------------|------------------------------|---------|---------------------|
| Question Answering            | `adv_qa`                     |1384 | Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Conversation                  | `adv_conversation`           |1018 |Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Summarization                 | `adv_summarization`          |525 |Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Search                        | `adv_search`                 |1000 |Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Text Rewrite                  | `adv_rewrite`                |1000 |Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Ungrounded Content Generation | `adv_content_gen_ungrounded` |496 | Groundedness |
| Grounded Content Generation   | `adv_content_gen_grounded`   |475 |Groundedness |
