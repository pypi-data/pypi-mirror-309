`pip install prlps_text_replacer`


```python
from prlps_text_replacer import text_replace_by_dict

text = "Гуманоидный робот и Соединенное Королевство - это разные вещи. А безпанцирные улитки - это просто слизни. РОБОТ рОбОт робот"
replacements = {
    "гуманоидный робот": "андроид",
    "Соединенное Королевство": "Великобритания",
    "безпанцирные улитки": "слизни",
    "робот": "машина",
    "РОБОТ": "АВТОМАТ",
}

result = text_replace_by_dict(text, replacements)
print(result)
```
