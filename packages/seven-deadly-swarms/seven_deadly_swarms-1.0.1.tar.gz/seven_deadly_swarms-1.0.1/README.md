# Seven Deadly Swarms

**Seven Deadly Swarms** is a Python library that allows you to dynamically modify text by either adding or removing elements inspired by the **seven deadly sins**: Pride, Greed, Wrath, Envy, Lust, Gluttony, and Sloth.


With this library, you can:
- **Add elements** to embellish and amplify text in the style of the seven sins.
- **Remove elements** to cleanse the text of any references or traits associated with the seven sins.

The library leverages OpenAI's GPT models and provides seamless integration using the `OPENAI_API_KEY` environment variable.

---

### Key Features
- **Add or Remove**: Transform your text by sequentially applying or removing traits inspired by the seven deadly sins.
- **Simple API**: Easy-to-use functions for integrating into any Python project.
- **Environment-Based Configuration**: Securely manage your OpenAI API key with environment variables.
- **Customizable and Modular**: Use the individual sins or the entire sequence depending on your needs.

---

### Example Usage

```python
from seven_deadly_swarms import SevenDeadlySwarms

# Initialize the swarms
swarms = SevenDeadlySwarms()

content = "The product launch was a massive success with grand ambition and meticulous details."

# Add elements of the seven deadly sins
modified_content = swarms.add_elements(content)
print("Added Elements:\n\n==============================================", modified_content)

# Remove elements of the seven deadly sins
cleaned_content = swarms.remove_elements(content)
print("Removed Elements:\n\n==============================================", cleaned_content)
```

---

### Installation

```bash
pip install seven-deadly-swarms
```

### Requirements
- Python 3.7+
- OpenAI Python SDK (`pip install openai`)

