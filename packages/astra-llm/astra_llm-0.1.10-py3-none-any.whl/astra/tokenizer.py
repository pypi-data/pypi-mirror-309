import tiktoken
import torch

class AstraTokenizer:
    
    def __init__(self):
        # Initialize tokenizer once in the constructor to avoid repeated calls
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def encoder(self, text: str, if_flat: bool=False) -> torch.Tensor:
        # Encode text to token IDs and convert to tensor
        token_ids = self.tokenizer.encode(text, allowed_special={"<|endoftext|>"})
        encoded_tensor = torch.tensor(token_ids)  
        if if_flat:
            encoded_tensor = encoded_tensor.unsqueeze(0) # add batch dimension
        return encoded_tensor
    
    def decoder(self, token_ids: torch.Tensor) -> str:
        # Decode token IDs back to text
        flat_ids = token_ids.squeeze(0)  # remove batch dimension if present
        decoded_text = self.tokenizer.decode(flat_ids.tolist())
        return decoded_text