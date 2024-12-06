# Introduction
## Install package
```shell
pip install llm_cat
```
##  Example Usage:
```python
# deepseek
message = "What is the capital of France?"
token ="sk-xxxxxxxxxxxxx"
result = deepseek_chat(message,token)
print(result)


# ollama
message = "What is the capital of France?"
response = ollama_chat(message,model='llama3.1',url = 'http://localhost:11434/api/chat')
print(response)
```



## Template

```python
from jinja2 import Template

prompt_template = "Hello {{ name }}!"
template = Template(prompt_template)
print(template.render(name="John Doe"))
```

