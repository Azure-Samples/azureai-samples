## Adversarial simulation

Augment and accelerate your red-teaming operation by leveraging Azure AI Studio safety evaluations to generate an adversarial dataset against your application. We provide adversarial tasks and profiles along with access to an Azure Open AI GPT-4 model with safety behaviors turned off to enable the adversarial simulation.

We provide starting samples for Question Answering and Conversation simulation. However the supported scenarios are listed in the table below, simply replace the template names with the template names. [Learn more](
https://aka.ms/advsimulatorhowto
) about how to use the simulator

| Task type                     | Template name                | Use this dataset for evaluating |
|-------------------------------|------------------------------|---------------------------------|
| Question Answering            | `adv_qa`                     | Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Conversation                  | `adv_conversation`           | Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Summarization                 | `adv_summarization`          | Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Search                        | `adv_search`                 | Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Text Rewrite                  | `adv_rewrite`                | Hateful and unfair content, Sexual content, Violent content, Self-harm-related content |
| Ungrounded Content Generation | `adv_content_gen_ungrounded` | Groundedness |
| Grounded Content Generation   | `adv_content_gen_grounded`   | Groundedness |
