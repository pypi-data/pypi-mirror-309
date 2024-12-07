from typing import Any, Dict, Optional, Type, TypeVar, Union
from pathlib import Path
import os
from pydantic import BaseModel

from .discovery import ConfigDiscovery
from .types import Environment
from ..exceptions import ConfigError
from typing import Any, Dict, Optional, Type, TypeVar
from pathlib import Path
import os
import boto3
import json
from botocore.exceptions import ClientError
from pydantic import BaseModel
from nice_logger import logger
T = TypeVar('T', bound=BaseModel)

class BaseSettings(BaseModel):
    """配置基类"""

    model_config = {
        "arbitrary_types_allowed": True,
        "extra": "allow",
    }

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._config_dir: Optional[Path] = None
        self._env: Optional[str] = None
        self._loaded = False

        # ASM 相关属性
        self._asm_client = None
        self._region_name = os.getenv("AWS_REGION", "ap-northeast-1")

    def _init_asm_client(self) -> None:
        """初始化 AWS Secrets Manager client"""
        if not self._asm_client:
            session = boto3.session.Session()
            self._asm_client = session.client(
                service_name='secretsmanager',
                region_name=self._region_name
            )

    @classmethod
    def from_config_dir(
        cls,
        config_dir: str | Path,
        env: Optional[str] = None,
        load_env_file: bool = True,
        **kwargs
    ) -> "BaseSettings":
        """从配置目录创建设置实例"""
        instance = cls(**kwargs)
        instance._config_dir = Path(config_dir)
        instance._env = env or os.getenv("ENV", "dev")

        if load_env_file:
            from dotenv import load_dotenv
            load_dotenv()

        instance.load_config()
        return instance

    def update_from_asm(self, secret_name: str = "db") -> None:
        """
        从 AWS Secrets Manager 更新配置

        Args:
            secret_name: ASM中的secret名称，默认为"db"
        """
        aws_config = self.get_config("aws")
        if not aws_config:
            logger.info("AWS configuration not found")
            return

        use_asm = getattr(aws_config, "use_asm", False)
        if not use_asm:
            logger.info("ASM is not enabled in AWS configuration")
            return

        asm_mapping = getattr(aws_config, "asm_mapping", {})
        if not asm_mapping:
            logger.info("ASM mapping is empty in AWS configuration")
            return

        self.load_asm(secret_name, asm_mapping)


    def load_asm(self, secret_name: str, mapping: Optional[Dict[str, str]] = None) -> None:
        """
        从 AWS Secrets Manager 加载配置并更新当前配置

        Args:
            secret_name: ASM中的secret名称
            mapping: ASM key与配置项的映射关系，格式为 {'asm_key': 'module.field'}
                    例如: {'exlink/mysql-pwd': 'database.mysql_password'}
        """
        self._init_asm_client()

        try:
            response = self._asm_client.get_secret_value(SecretId=secret_name)
            secret_data = json.loads(response['SecretString'])
            if mapping:
                for asm_key, config_path in mapping.items():
                    if asm_key not in secret_data:
                        continue

                    # 解析配置路径
                    parts = config_path.split('.')
                    if len(parts) != 2:
                        continue

                    module_name, field_name = parts
                    config = self.get_config(module_name)

                    if config and hasattr(config, field_name):
                        # 获取字段类型并进行类型转换
                        field_info = config.model_fields.get(field_name)
                        if field_info:
                            value = secret_data[asm_key]
                            # 使用现有的类型转换逻辑
                            self._set_config_value(config, field_name, value)

        except ClientError as e:
            logger.error(f"Failed to load secret from ASM: {str(e)}")
            raise

    def load_config(self) -> None:
        """加载配置"""
        if not self._config_dir:
            raise ConfigError("Config directory not set")
        logger.info(f"Loading config from directory: {self._config_dir}")  # 调试信息

        # 使用配置发现器加载配置
        discovery = ConfigDiscovery(self._config_dir)
        configs = discovery.discover_configs(self._env)
        logger.info(f"Discovered configs: {configs}")  # 调试信息

        # 更新配置
        self._update_configs(configs)
        self._loaded = True

    def _update_configs(self, configs: Dict[str, Type[BaseModel]]) -> None:
        """更新配置值"""
        logger.info(f"Updating configs with: {configs}")  # 调试信息

        # 初始化配置实例
        config_instances = {}
        for module_name, config_class in configs.items():
            try:
                logger.debug(f"Processing config for module: {module_name}")  # 调试信息
                # 如果已经存在该属性，使用现有值
                if hasattr(self, module_name):
                    existing = getattr(self, module_name)
                    if isinstance(existing, config_class):
                        config_instances[module_name] = existing
                        logger.debug(f"Using existing config for {module_name}: {existing}")  # 调试信息
                        continue

                # 否则创建新实例
                config_instances[module_name] = config_class()
                logger.info(f"Created new config for {module_name}: {config_instances[module_name]}")  # 调试信息
            except Exception as e:
                logger.error(f"Error creating config for {module_name}: {e}")  # 调试信息
                raise ConfigError(f"Failed to initialize config for {module_name}: {e}")

        # 从环境变量覆盖配置
        self._override_from_env(config_instances)

        # 更新实例
        for field_name, instance in config_instances.items():
            logger.info(f"Setting field {field_name} with value: {instance}")  # 调试信息
            object.__setattr__(self, field_name, instance)

    def _override_from_env(self, configs: Dict[str, BaseModel]) -> None:
        """从环境变量覆盖配置"""
        logger.info(f"Starting environment variable override...")  # 调试日志

        # 遍历所有环境变量
        for env_key, env_value in os.environ.items():
            logger.info(f"Checking environment variable: {env_key}={env_value}")  # 调试日志

            # 检查标准格式 (MODULE_FIELD)
            for module_name, config in configs.items():
                # 1. 检查标准格式 (例如: DATABASE_MYSQL_HOST)
                standard_key = f"{module_name.upper()}_{env_key}"
                if env_key.startswith(f"{module_name.upper()}_"):
                    field_name = env_key[len(module_name) + 1:].lower()
                    if field_name in config.model_fields:
                        self._set_config_value(config, field_name, env_value)
                        continue

                # 2. 检查简化格式 (例如: MYSQL_HOST 映射到 database.mysql_host)
                for field_name in config.model_fields:
                    if env_key.upper() == f"{field_name.upper()}":
                        self._set_config_value(config, field_name, env_value)
                        break

                    # 处理嵌套字段 (例如: MYSQL_HOST 映射到 database.mysql_host)
                    # field_parts = field_name.split('_')
                    # if len(field_parts) > 1:
                    #     if env_key.upper() == f"{field_parts[-1].upper()}":
                    #         self._set_config_value(config, field_name, env_value)
                    #         break

    def _set_config_value(self, config: BaseModel, field_name: str, env_value: str) -> None:
        """设置配置值并进行类型转换"""
        try:
            field_info = config.model_fields[field_name]
            field_type = field_info.annotation

            # 类型转换
            if field_type == bool:
                env_value = env_value.lower() == 'true'
            elif field_type == int:
                env_value = int(env_value)
            elif field_type == float:
                env_value = float(env_value)
            elif field_type == list:
                env_value = env_value.split(',')

            logger.info(f"Setting {field_name} = {env_value} ({type(env_value)})")  # 调试日志
            setattr(config, field_name, env_value)

        except Exception as e:
            logger.error(f"Error setting config value: {e}")  # 调试日志
            raise ConfigError(f"Invalid environment variable value for {field_name}: {e}")

    def reload(self) -> None:
        """重新加载配置"""
        if not self._loaded:
            raise ConfigError("Config not loaded yet")
        self.load_config()

    @property
    def env(self) -> Environment:
        """当前环境"""
        return Environment(self._env or "dev")

    def get_config(self, module: str) -> Optional[BaseModel]:
        """获取指定模块的配置"""
        return getattr(self, module, None)

    def export_config(self) -> Dict[str, Any]:
        """导出配置为字典"""
        return self.model_dump()

    @classmethod
    def load(
        cls,
        config_dir: Optional[Union[str, Path]] = None,
        module: Optional[str] = None,
        env: Optional[str] = None
    ) -> "Settings":
        """
        加载项目配置

        Args:
            config_dir: 配置文件目录路径。如果为None，将按顺序从其他位置查找
            module: Python模块路径，用于从指定模块所在目录查找配置
                    例如: "your_project.src"
            env: 环境名称，如果为None则从环境变量ENV中获取，默认为dev

        Returns:
            Settings: 配置实例

        Raises:
            ConfigError: 当无法找到有效的配置目录时抛出

        Priority:
            1. 显式指定的config_dir
            2. 环境变量 CONFIG_DIR
            3. 指定模块目录（如果提供了module参数）
            4. 调用者代码所在目录
            5. 当前工作目录
            6. 项目根目录递归查找
        """
        searched_paths = []

        if config_dir is None:
            # 1. 首先检查环境变量
            config_dir = os.getenv("CONFIG_DIR")
            if config_dir:
                logger.info(f"Found CONFIG_DIR environment variable: {config_dir}")
            else:
                logger.info("CONFIG_DIR environment variable not set")

            if not config_dir:
                # 2. 如果提供了模块路径，从模块所在目录查找
                if module:
                    try:
                        import importlib
                        module_spec = importlib.util.find_spec(module)
                        if module_spec and module_spec.origin:
                            module_dir = Path(module_spec.origin).parent
                            module_config = module_dir / "config" / "env_config"
                            searched_paths.append(str(module_config))
                            logger.info(f"Checking module directory: {module_config}")
                            if module_config.exists():
                                config_dir = module_config
                                print(f"Found config directory in module: {config_dir}")
                    except Exception as e:
                        logger.info(f"Error finding module {module}: {e}")

                # 3. 从调用者代码所在目录查找
                if not config_dir:
                    import inspect
                    caller_frame = inspect.currentframe().f_back
                    if caller_frame:
                        caller_file = caller_frame.f_code.co_filename
                        caller_dir = Path(caller_file).parent
                        caller_config = caller_dir / "env_config"
                        searched_paths.append(str(caller_config))
                        logger.info(f"Checking caller directory: {caller_config}")
                        if caller_config.exists():
                            config_dir = caller_config
                            logger.info(f"Found config directory in caller location: {config_dir}")

                # 4. 检查当前工作目录
                if not config_dir:
                    cwd_config = Path.cwd() / "config" / "env_config"
                    searched_paths.append(str(cwd_config))
                    logger.info(f"Checking current working directory: {cwd_config}")

                    if cwd_config.exists():
                        config_dir = cwd_config
                        logger.info(f"Found config directory in current working directory: {config_dir}")
                    else:
                        # 5. 尝试查找项目根目录
                        current_dir = Path.cwd()
                        while current_dir.parent != current_dir:
                            config_path = current_dir / "config" / "env_config"
                            searched_paths.append(str(config_path))
                            logger.info(f"Checking directory: {config_path}")

                            if config_path.exists():
                                config_dir = config_path
                                logger.info(f"Found config directory: {config_dir}")
                                break
                            current_dir = current_dir.parent
        else:
            logger.info(f"Using explicitly provided config directory: {config_dir}")

        if not config_dir:
            error_message = ["Cannot find config directory. Please either:"]
            error_message.append("1. Set CONFIG_DIR environment variable")
            error_message.append("2. Create config/env_config directory in your project")
            error_message.append("3. Specify module parameter with your project's module path")
            error_message.append("4. Explicitly specify config_dir when calling load()")
            error_message.append("\nSearched locations:")
            for path in searched_paths:
                error_message.append(f"  - {path}")

            logger.info("\nSearched the following locations:")
            for path in searched_paths:
                print(f"  - {path}")

            raise ConfigError("\n".join(error_message))

        logger.info(f"\nFinal config directory: {config_dir}")
        logger.info(f"Current environment: {env}")

        return cls.from_config_dir(config_dir, env)
