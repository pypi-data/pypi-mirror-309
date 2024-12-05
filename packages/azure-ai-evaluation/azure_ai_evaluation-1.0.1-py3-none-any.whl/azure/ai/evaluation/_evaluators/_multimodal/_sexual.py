# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from promptflow._utils.async_utils import async_run_allowing_running_loop
from azure.ai.evaluation._common.constants import EvaluationMetrics
from azure.ai.evaluation._common._experimental import experimental
from ._content_safety_multimodal_base import ContentSafetyMultimodalEvaluatorBase


@experimental
class SexualMultimodalEvaluator:
    """
    Initialize a sexual multimodal evaluator for sexual score.

    :param credential: The credential for connecting to the Azure AI project. This is required.
    :type credential: ~azure.core.credentials.TokenCredential
    :param azure_ai_project: The scope of the Azure AI project,
        which includes subscription ID, resource group name, and project name.
    :type azure_ai_project: ~azure.ai.evaluation.AzureAIProject

    **Usage Example**

    .. code-block:: python

        azure_ai_project = {
            "subscription_id": "<subscription_id>",
            "resource_group_name": "<resource_group_name>",
            "project_name": "<project_name>",
        }
        eval_fn = SexualMultimodalEvaluator(azure_ai_project)
        result = eval_fn(conversation=
            {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What's in this image?"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "<image url or base64 encoded image>"
                                }
                            }
                        ]
                    },
                    {
                        "role": "assistant",
                        "content": "This picture shows an astronaut standing in the desert."
                    }
                ]
            }
        )

    **Output Format**

    .. code-block:: json

        {
            "sexual": "High",
            "sexual_score": 6.5,
            "sexual_reason": "Some reason"
        }

    """

    id = "sexual_multimodal"
    """Evaluator identifier, experimental and to be used only with evaluation in cloud."""

    def __init__(self, credential, azure_ai_project):
        self._async_evaluator = _AsyncSexualMultimodalEvaluator(credential, azure_ai_project)

    def __call__(self, *, conversation, **kwargs):
        """
        Evaluates sexual content.

        :keyword conversation: The conversation contains list of messages to be evaluated.
            Each message should have "role" and "content" keys. It supports single turn only.
        :paramtype conversation: ~azure.ai.evaluation.Conversation
        :return: The sexual score.
        :rtype: Dict[str, Union[float, str]]
        """
        return async_run_allowing_running_loop(self._async_evaluator, conversation=conversation, **kwargs)

    def _to_async(self):
        return self._async_evaluator


class _AsyncSexualMultimodalEvaluator(ContentSafetyMultimodalEvaluatorBase):
    def __init__(self, credential, azure_ai_project):
        super().__init__(
            metric=EvaluationMetrics.SEXUAL,
            credential=credential,
            azure_ai_project=azure_ai_project,
        )

    async def __call__(self, *, conversation, **kwargs):
        return await super().__call__(conversation=conversation, **kwargs)
