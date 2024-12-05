from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import cast

from poetry.core.poetry import Poetry as BasePoetry

from poetry.__version__ import __version__

# from openfund.config.source import Source
from openfund.pyproject.toml import PyProjectTOML

""
if TYPE_CHECKING:
    from pathlib import Path

    from poetry.core.packages.project_package import ProjectPackage

    from openfund.packages.locker import Locker
    from openfund.config.config import Config
    from openfund.plugins.plugin_manager import PluginManager
    from openfund.repositories.repository_pool import RepositoryPool
    from openfund.toml import TOMLFile


class Openfund(BasePoetry):
    VERSION = __version__

    def __init__(
        self,
        file: Path,
        local_config: dict[str, Any],
        package: ProjectPackage,
        locker: Locker,
        config: Config,
        disable_cache: bool = False,
    ) -> None:
        from openfund.repositories.repository_pool import RepositoryPool

        super().__init__(file, local_config, package, pyproject_type=PyProjectTOML)

        self._locker = locker
        self._config = config
        self._pool = RepositoryPool(config=config)
        self._plugin_manager: PluginManager | None = None
        self._disable_cache = disable_cache

    @property
    def pyproject(self) -> PyProjectTOML:
        pyproject = super().pyproject
        return cast("PyProjectTOML", pyproject)

    @property
    def file(self) -> TOMLFile:
        return self.pyproject.file

    @property
    def locker(self) -> Locker:
        return self._locker

    @property
    def pool(self) -> RepositoryPool:
        return self._pool

    @property
    def config(self) -> Config:
        return self._config

    @property
    def disable_cache(self) -> bool:
        return self._disable_cache

    def set_locker(self, locker: Locker) -> Openfund:
        self._locker = locker

        return self

    def set_pool(self, pool: RepositoryPool) -> Openfund:
        self._pool = pool

        return self

    def set_config(self, config: Config) -> Openfund:
        self._config = config

        return self

    def set_plugin_manager(self, plugin_manager: PluginManager) -> Openfund:
        self._plugin_manager = plugin_manager

        return self

    # def get_sources(self) -> list[Source]:
    #     return [
    #         Source(**source)
    #         for source in self.pyproject.poetry_config.get("source", [])
    #     ]
