# jsonicdict

## 概要

jsonicdictは、PythonのListやDict等をJSONと全く同じ表記で記述できるようにするためのライブラリです。

## インストール

```bash
pip install jsonicdict
```

## 使い方

```python
from jsonicdict import true, false, null
```

## サンプル

```python
from jsonicdict import true, false, null

objnull = null
objfalse = false
objtrue = true
objnum = 200
objstr = "string"
objarray = [1, "string", true, false, null, {"key": "value"}]
objdict = {"null": null, "array": [1, 2, 3], "string": "string", "number": 1, "boolean": true, "false": false, "object": {"key": "value"}}

print(objnull)    # -> None
print(objfalse)   # -> False
print(objtrue)    # -> True
print(objnum)     # -> 200
print(objstr)     # -> string
print(objarray)   # -> [1, 'string', True, False, None, {'key': 'value'}]
print(objdict)    # -> {'null': None, 'array': [1, 2, 3], 'string': 'string', 'number': 1, 'boolean': True, 'false': False, 'object': {'key': 'value'}}

import json

jsonnull = json.loads('null')
jsonfalse = json.loads('false')
jsontrue = json.loads('true')
jsonnum = json.loads('200')
jsonstr = json.loads('"string"')
jsonarray = json.loads('[1, "string", true, false, null, {"key": "value"}]')
jsondict = json.loads('{"null": null, "array": [1, 2, 3], "string": "string", "number": 1, "boolean": true, "false": false, "object": {"key": "value"}}')

print(jsonnull)    # -> None
print(jsonfalse)   # -> False
print(jsontrue)    # -> True
print(jsonnum)     # -> 200
print(jsonstr)     # -> string
print(jsonarray)   # -> [1, 'string', True, False, None, {'key': 'value'}]
print(jsondict)    # -> {'null': None, 'array': [1, 2, 3], 'string': 'string', 'number': 1, 'boolean': True, 'false': False, 'object': {'key': 'value'}}

```
