import os
import torch
import glob
import json
from .gpt_model import GPTModel
from .tokenizer import AstraTokenizer


# torch.serialization.add_safe_globals([GPTModel])

class Model:
    def __init__(self, model_dir: str, map_location='cpu', weights_only=False):
        self.map_location = map_location
        self.config = self.load_config(model_dir)
        model_path = self.find_model_path(model_dir)
        self.model = self.load_model(model_path, weights_only)
        
    
    def find_model_path(self, model_dir: str):
        model_files = glob.glob(os.path.join(model_dir, '*.pth'))
        if not model_files:
            raise FileNotFoundError("No model file found in the specified directory.")
        return model_files[0]  # Assuming there's only one matching file
    
    def load_model(self, model_path: str, weights_only):
        model = GPTModel(self.config)
        state_dict = torch.load(model_path, map_location=self.map_location, weights_only=weights_only)
        model.load_state_dict(state_dict)
        model.to(self.map_location)
        model.eval()  
        return model
    
    def load_config(self, model_dir: str):
        config_path = glob.glob(os.path.join(model_dir, '*config.json'))
        if not config_path:
            raise FileNotFoundError("Configuration file not found.")
        with open(config_path[0], 'r') as f:
            config = json.load(f)
        return config


    def generate(self, messages , max_new_tokens=255, context_size=None, temperature=0.0, top_k=None, eos_id=None):
        
        tokenizer = AstraTokenizer()
        idx = tokenizer.encoder(messages, True)
        idx = idx.to(self.map_location)
        
        if context_size == None:
            context_size = self.config['context_length']
        
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -context_size:]
            with torch.no_grad():
                logits = self.model(idx_cond)
            logits = logits[:, -1, :]
            if top_k is not None:
                top_logits, _ = torch.topk(logits, top_k)
                min_val = top_logits[:, -1]
                logits = torch.where(
                    logits < min_val,
                    torch.tensor(float('-inf')).to(logits.device),
                    logits
                )
            if temperature > 0.0:
                logits = logits / temperature
                probs = torch.softmax(logits, dim=-1)
                idx_next = torch.multinomial(probs, num_samples=1)
            else:
                idx_next = torch.argmax(logits, dim=-1, keepdim=True)
            if idx_next == eos_id:
                break
            idx = torch.cat((idx, idx_next), dim=1)
        return tokenizer.decoder(idx)