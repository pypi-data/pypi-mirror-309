# Check Python version
**N.B: python version must be required up to 3.10.0**

`!python --version`


# Install dependencies of Astra LLM
`pip install astra-llm==0.1.19`

# Load Model

### Selection of device for load model
```
import torch

# Set device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

```

### Load model
```
from astra.model import Model

model = Model('/kaggle/input/astra/pytorch/1.4b/2', map_location=device)
```

# Generate text

```
response = model.generate(
    messages="hello",
    max_new_tokens=50,
    top_k=25,
    temperature=1.4
)
```