# LSP Types Required

A demonstration repository which shows [ZubanLS](https://zubanls.com/) requires types to be installed to return code suggestions / highlights / autocompletion for packages installed in a virtualenv.

The `lsp_client` will send the LSP server a `textDocument/hover` event for line 0, character 11 of `main.py` which simply contains:
```python
import requests
```
With Jedi server, you'll get a nice response of the module:
```
DEBUG:pygls.protocol.json_rpc:Received result for message "64e3f112-9203-4055-8b57-33996dfa8176": Hover(contents=MarkupContent(kind=<MarkupKind.PlainText: 'plaintext'>, value='module requests\n---\nRequests HTTP Library\n~~~~~~~~~~~~~~~~~~~~~\n\nRequests is an HTTP library, written in Python, for human beings.
...
```

With Zuban you'll get `null` (or `None`):
```
DEBUG:pygls.protocol.json_rpc:Received result for message "6969d192-7f1f-48b6-87d2-786266511623": None
```

But when you install the `types-request` package, Zuban is able to return some info:
```
DEBUG:pygls.protocol.json_rpc:Received result for message "3e37ce6f-4d59-4cb6-9af9-47dc62420e57": Hover(contents=MarkupContent(kind=<MarkupKind.Markdown: 'markdown'>, value='(module) requests: ModuleType\n---\nRequests HTTP Library\n~~~~~~~~~~~~~~~~~~~~~\n\nRequests is an HTTP library, written in Python, for human beings.\n
...
```

How to do it yourself:

```shell
uv sync

uv run lsp_client jedi
uv run lsp_client zuban

uv run pip install types-request

uv run lsp_client jedi
uv run lsp_client zuban
```
