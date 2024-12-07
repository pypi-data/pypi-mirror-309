from ..model_registry import register_model
from ..types import ModelInputOutput
from .vision2seq import Vision2SeqModel


@register_model(
    "Salesforce/blip2-opt-2.7b", "transformers", ModelInputOutput.IMAGE_TEXT_TO_TEXT
)
@register_model(
    "Salesforce/blip2-opt-6.7b", "transformers", ModelInputOutput.IMAGE_TEXT_TO_TEXT
)
@register_model(
    "Salesforce/blip2-flan-t5-xxl", "transformers", ModelInputOutput.IMAGE_TEXT_TO_TEXT
)
@register_model(
    "Salesforce/blip2-opt-6.7b-coco",
    "transformers",
    ModelInputOutput.IMAGE_TEXT_TO_TEXT,
)
@register_model(
    "Salesforce/blip2-flan-t5-xl",
    "transformers",
    ModelInputOutput.IMAGE_TEXT_TO_TEXT,
)
@register_model(
    "Salesforce/blip2-flan-t5-xl-coco",
    "transformers",
    ModelInputOutput.IMAGE_TEXT_TO_TEXT,
)
@register_model(
    "Salesforce/blip2-opt-2.7b-coco",
    "transformers",
    ModelInputOutput.IMAGE_TEXT_TO_TEXT,
)
@register_model(
    "Gregor/mblip-mt0-xl",
    "transformers",
    ModelInputOutput.IMAGE_TEXT_TO_TEXT,
)
@register_model(
    "Gregor/mblip-bloomz-7b",
    "transformers",
    ModelInputOutput.IMAGE_TEXT_TO_TEXT,
)
class BLIP2(Vision2SeqModel):
    def __init__(self, model_id: str, **kwargs):
        super().__init__(model_id, **kwargs)
