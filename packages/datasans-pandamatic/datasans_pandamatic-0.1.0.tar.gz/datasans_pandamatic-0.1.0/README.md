# Pandamatic

An AI-powered code generator for dataframe processing. 

## Installation

```bash
pip install datasans-pandamatic
```

## Usage

```python
from datasans_pandamatic import PandaMatic

# Initialize with your key code
generator = PandaMatic(key_code="your-key-code")

# Define your dataframe
df = pd.read_csv("your_data.csv")

# Use the generator
code = generator.gencode(df, "Your prompt here")
code
```

## Features

- AI-powered code generation
- Smart data type handling
- Comprehensive error handling
- Powered by Open AI GPT 4o Mini
