import torch
from transformers import AutoTokenizer, AutoModel


class TransformerEncoder:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()

    def encode(self, text: str):
        if not text:
            text = ""

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        # Mean pooling
        embeddings = outputs.last_hidden_state
        attention_mask = inputs["attention_mask"]

        mask = attention_mask.unsqueeze(-1).expand(
            embeddings.size()
        ).float()

        summed = torch.sum(embeddings * mask, dim=1)

        counts = torch.clamp(
            mask.sum(dim=1),
            min=1e-9
        )

        return (summed / counts).squeeze(0).numpy()


class CodeBERTEncoder(TransformerEncoder):
    def __init__(self):
        super().__init__(
            "microsoft/codebert-base"
        )


class SciBERTEncoder(TransformerEncoder):
    def __init__(self):
        super().__init__(
            "allenai/scibert_scivocab_uncased"
        )
