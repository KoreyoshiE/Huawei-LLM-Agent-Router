import re
import json
import importlib
from abc import ABC, abstractmethod
from transformers import AutoModelForCausalLM, AutoTokenizer

# Detect available accelerators: NPU (vendor-specific), CUDA (NVIDIA), and MPS (Apple)
# Set flags and a `device_map` used later when loading models.
IS_NPU = False
IS_CUDA = False
IS_MPS = False
device_map = "auto"  # default fallback

# 1) Try NPU (vendor-specific extension, e.g., torch_npu)
try:
    torch_npu = importlib.import_module("torch_npu")

    npu_module = getattr(torch_npu, "npu", None)
    is_avail = getattr(npu_module, "is_available", None)
    if callable(is_avail) and is_avail():
        IS_NPU = True
        device_map = {"": "npu"}
except Exception:
    # keep IS_NPU False on any failure
    IS_NPU = False

# 2) Try standard PyTorch CUDA / MPS detection
try:
    torch = importlib.import_module("torch")

    if getattr(torch, "cuda", None) is not None and torch.cuda.is_available():
        IS_CUDA = True
        # Map whole model to CUDA device (transformers accepts 'cuda' or 'cuda:0')
        device_map = {"": "cuda"}
    elif getattr(getattr(torch, "backends", None), "mps", None) is not None and torch.backends.mps.is_available():
        IS_MPS = True
        device_map = {"": "mps"}
except Exception:
    # If torch isn't installed or detection fails, fall back to defaults
    IS_CUDA = False
    IS_MPS = False


class BaseLLM(ABC):
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map="auto" if not IS_NPU else {"": "npu"},
        )

    def generate(self, messages, max_new_tokens=1024, **kwargs):
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **model_inputs, max_new_tokens=max_new_tokens, **kwargs
        )
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]) :].tolist()
        content = self.tokenizer.decode(output_ids, skip_special_tokens=True)
        return content


class CustomAgent:
    def __init__(self):
        # TODO: Initialize your Agent here
        raise NotImplementedError("CustomAgent is not implemented yet.")

    def run(self, input_messages) -> str:
        # TODO: Implement your Agent logic here
        raise NotImplementedError("CustomAgent run method is not implemented yet.")
        return "[Your Agent response]"
