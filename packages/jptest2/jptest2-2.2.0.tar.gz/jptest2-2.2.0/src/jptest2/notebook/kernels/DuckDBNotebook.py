from asyncio import Lock
from os import PathLike
from typing import Union

from nbclient import NotebookClient

from .. import Notebook
from ..NotebookCell import NotebookCell


class DuckDBNotebook(Notebook):
    def __init__(self, notebook: Union[str, PathLike], execute: bool = False, timeout: int = 120):
        super().__init__(notebook, self.__execute_cell, execute)

        self._nc: NotebookClient = NotebookClient(self._nb, kernel_name='duckdb_kernel', timeout=timeout)
        self._lock: Lock = Lock()

    async def __aenter__(self) -> "Notebook":
        await self._nc.async_setup_kernel(cleanup_kc=False).__aenter__()
        await super().__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self._nc._async_cleanup_kernel()

    async def __execute_cell(self, cell: NotebookCell):
        async with self._lock:
            await self._nc.async_execute_cell(cell.raw_cell, cell_index=cell.idx)
