from pathlib import Path
from typing import Dict, Type, Optional
import importlib.util
import sys
from pydantic import BaseModel

from nice_config.exceptions.config_error import ConfigError
from nice_logger import logger
class ConfigDiscovery:
    """配置发现器"""

    def __init__(self, config_dir: Path):
        self.config_dir = config_dir

    def discover_configs(
        self,
        env: Optional[str] = None
    ) -> Dict[str, Type[BaseModel]]:
        """发现配置类

        Args:
            env: 环境名称

        Returns:
            配置类字典 {模块名: 配置类}
        """
        logger.info(f"Discovering configs for env: {env}")  # 调试日志

        # 加载默认配置
        configs = self._load_default_configs()
        logger.info(f"Loaded default configs: {configs}")  # 调试日志

        # 如果指定了环境且不是dev，加载环境特定配置
        if env and env != "dev":
            env_configs = self._load_env_configs(env)
            logger.info(f"Loaded env specific configs: {env_configs}")  # 调试日志

            # 更新配置，环境特定配置会覆盖默认配置
            for module_name, config_class in env_configs.items():
                if module_name in configs:
                    # 如果是继承自默认配置类，则使用环境特定配置类
                    default_class = configs[module_name]
                    if issubclass(config_class, default_class):
                        logger.info(f"Overriding {module_name} with env specific config")  # 调试日志
                        configs[module_name] = config_class
                else:
                    configs[module_name] = config_class

        return configs

    def _load_default_configs(self) -> Dict[str, Type[BaseModel]]:
        """加载默认配置"""
        return self._load_configs_from_dir("default")

    def _load_env_configs(self, env: str) -> Dict[str, Type[BaseModel]]:
        """加载环境特定配置"""
        return self._load_configs_from_dir(env)

    def _load_configs_from_dir(self, subdir: str) -> Dict[str, Type[BaseModel]]:
        """从指定子目录加载配置"""
        config_dir = self.config_dir / subdir
        logger.info(f"Loading configs from directory: {config_dir}")  # 调试日志

        if not config_dir.exists():
            logger.info(f"Config directory does not exist: {config_dir}")  # 调试日志
            return {}

        configs = {}
        for config_file in config_dir.glob("*.py"):
            if config_file.stem == "__init__":
                continue

            try:
                logger.info(f"Processing config file: {config_file}")  # 调试日志

                # 构建正确的模块路径
                rel_path = config_file.relative_to(self.config_dir.parent.parent)
                module_parts = list(rel_path.parent.parts) + [rel_path.stem]
                module_path = ".".join(module_parts)
                logger.info(f"Full module path: {module_path}")  # 调试日志

                # 检查模块是否已经加载
                if module_path in sys.modules:
                    logger.info(f"Module already loaded: {module_path}")  # 调试日志
                    module = sys.modules[module_path]
                else:
                    logger.info(f"Loading module: {module_path}")  # 调试日志
                    spec = importlib.util.spec_from_file_location(module_path, config_file)
                    if spec is None or spec.loader is None:
                        logger.info(f"Failed to get module spec for: {config_file}")  # 调试日志
                        continue

                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_path] = module
                    spec.loader.exec_module(module)

                # 查找所有配置类
                config_class = None
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if (isinstance(item, type) and
                        issubclass(item, BaseModel) and
                        item != BaseModel):
                        logger.info(f"Found config class: {item_name}")  # 调试日志

                        # 如果是环境特定配置，检查是否继承自默认配置
                        if subdir != "default":
                            # 获取基类
                            bases = item.__bases__
                            for base in bases:
                                if base.__module__.endswith("default." + config_file.stem):
                                    logger.info(f"Found environment specific config: {item_name} inherits from {base.__name__}")
                                    config_class = item
                                    break
                        else:
                            # 默认配置直接使用
                            config_class = item
                            break

                if config_class:
                    logger.info(f"Using config class: {config_class.__name__}")  # 调试日志
                    configs[config_file.stem] = config_class
                else:
                    logger.info(f"No suitable config class found in {config_file}")  # 调试日志

            except Exception as e:
                logger.info(f"Error loading config from {config_file}: {e}")  # 调试日志
                raise ConfigError(f"Failed to load config from {config_file}: {e}")

        return configs
