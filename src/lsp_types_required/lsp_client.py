import asyncio
import logging
import os
import sys
from pathlib import Path

from lsprotocol import types
from pygls.lsp.client import BaseLanguageClient

logging.basicConfig()
logging.getLogger("pygls.protocol.json_rpc").setLevel(logging.DEBUG)

logger: logging.Logger = logging.getLogger(__name__)

current_dir: Path = Path(__file__).parent.absolute()


def initialize(pid: int, current_dir: Path) -> types.InitializeParams:
    """
    See an example here: https://github.com/microsoft/monitors4codegen/blob/main/src/monitors4codegen/multilspy/language_servers/jedi_language_server/initialize_params.json
    """
    return types.InitializeParams(
        capabilities=types.ClientCapabilities(
            text_document=types.TextDocumentClientCapabilities(
                hover=types.HoverClientCapabilities(
                    dynamic_registration=False,
                    content_format=[
                        types.MarkupKind.Markdown,
                        types.MarkupKind.PlainText,
                    ],
                )
            )
        ),
        process_id=pid,
        client_info=types.InitializeParamsClientInfoType(
            name="PyGLS client", version="0.0.1"
        ),
        root_path=str(current_dir),
        trace=types.TraceValues.Verbose,
        workspace_folders=[
            types.WorkspaceFolder(uri=f"file://{current_dir}", name="workspace")
        ],
    )


class LanguageClient(BaseLanguageClient):
    async def server_exit(self, server: asyncio.subprocess.Process):
        """Called when the server process exits."""
        error: bytes = b"Server process exited"
        if server.stderr and not server.stderr.at_eof():
            # Log stderr
            error = await server.stderr.read()
            logger.error(error)

        # Notify pending futures of the server being stopped
        for future in self.protocol._request_futures.values():
            future.set_exception(RuntimeError(error))


async def lsp_send_hover(lsp: str):
    client: LanguageClient = LanguageClient(name="My PyGLS Client", version="0.0.1")

    match lsp:
        case "jedi":
            await client.start_io(".venv/bin/jedi-language-server")
        case "zuban":
            await client.start_io(".venv/bin/zuban", "server")

    await client.initialize_async(
        params=initialize(pid=os.getpid(), current_dir=current_dir)
    )

    client.initialized(params=types.InitializedParams())

    await client.text_document_hover_async(
        params=types.HoverParams(
            text_document=types.TextDocumentIdentifier(
                uri=f"file://{current_dir / 'main.py'}",
            ),
            position=types.Position(line=0, character=11),
        )
    )


def main():
    lsp: str = sys.argv[1] if len(sys.argv) > 1 else "jedi"

    asyncio.run(lsp_send_hover(lsp))


if __name__ == "__main__":
    main()
