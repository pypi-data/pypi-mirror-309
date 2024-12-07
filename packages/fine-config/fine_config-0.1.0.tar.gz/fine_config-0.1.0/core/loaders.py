from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path
import os
import json
import yaml
from dotenv import load_dotenv

from .types import ConfigSource, ConfigFormat
from ..exceptions import ConfigLoadError

class ConfigLoader(ABC):
    """配置加载器基类"""
    
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """加载配置"""
        pass

class EnvConfigLoader(ConfigLoader):
    """环境变量配置加载器"""
    
    def __init__(self, prefix: str = "", load_dotenv_file: bool = True):
        self.prefix = prefix
        if load_dotenv_file:
            load_dotenv()
    
    def load(self) -> Dict[str, Any]:
        """从环境变量加载配置"""
        configs = {}
        for key, value in os.environ.items():
            if self.prefix and not key.startswith(self.prefix):
                continue
            
            # 移除前缀
            if self.prefix:
                key = key[len(self.prefix):]
                
            # 处理嵌套键 (例如: DATABASE_MYSQL_HOST -> database.mysql.host)
            parts = key.lower().split('_')
            current = configs
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = value
            
        return configs

class FileConfigLoader(ConfigLoader):
    """文件配置加载器"""
    
    def __init__(
        self, 
        file_path: str | Path,
        format: ConfigFormat = ConfigFormat.AUTO
    ):
        self.file_path = Path(file_path)
        self.format = format if format != ConfigFormat.AUTO else self._detect_format()
        
    def _detect_format(self) -> ConfigFormat:
        """根据文件扩展名检测格式"""
        suffix = self.file_path.suffix.lower()
        format_map = {
            '.json': ConfigFormat.JSON,
            '.yaml': ConfigFormat.YAML,
            '.yml': ConfigFormat.YAML,
            '.toml': ConfigFormat.TOML,
            '.env': ConfigFormat.ENV,
        }
        return format_map.get(suffix, ConfigFormat.JSON)
    
    def load(self) -> Dict[str, Any]:
        """从文件加载配置"""
        if not self.file_path.exists():
            raise ConfigLoadError(f"Config file not found: {self.file_path}")
            
        try:
            content = self.file_path.read_text(encoding='utf-8')
            
            if self.format == ConfigFormat.JSON:
                return json.loads(content)
            elif self.format == ConfigFormat.YAML:
                import yaml
                return yaml.safe_load(content)
            elif self.format == ConfigFormat.TOML:
                import tomli
                return tomli.loads(content)
            elif self.format == ConfigFormat.ENV:
                # 解析 .env 文件
                configs = {}
                for line in content.splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        configs[key.strip()] = value.strip().strip('"\'')
                return configs
            else:
                raise ConfigLoadError(f"Unsupported format: {self.format}")
                
        except Exception as e:
            raise ConfigLoadError(f"Failed to load config file: {e}")

class RedisConfigLoader(ConfigLoader):
    """Redis配置加载器"""
    
    def __init__(
        self,
        redis_url: str,
        prefix: str = "config:",
        format: ConfigFormat = ConfigFormat.JSON
    ):
        self.redis_url = redis_url
        self.prefix = prefix
        self.format = format
        
    def load(self) -> Dict[str, Any]:
        """从Redis加载配置"""
        try:
            import redis
            client = redis.from_url(self.redis_url)
            
            configs = {}
            for key in client.scan_iter(f"{self.prefix}*"):
                value = client.get(key)
                if value:
                    # 移除前缀
                    key = key[len(self.prefix):].decode('utf-8')
                    
                    # 解析值
                    if self.format == ConfigFormat.JSON:
                        value = json.loads(value)
                    elif self.format == ConfigFormat.YAML:
                        import yaml
                        value = yaml.safe_load(value)
                        
                    # 处理嵌套键
                    parts = key.split('.')
                    current = configs
                    for part in parts[:-1]:
                        current = current.setdefault(part, {})
                    current[parts[-1]] = value
                    
            return configs
            
        except Exception as e:
            raise ConfigLoadError(f"Failed to load config from Redis: {e}")

class VaultConfigLoader(ConfigLoader):
    """Vault配置加载器"""
    
    def __init__(
        self,
        url: str,
        token: str,
        path: str,
        mount_point: str = "secret"
    ):
        self.url = url
        self.token = token
        self.path = path
        self.mount_point = mount_point
        
    def load(self) -> Dict[str, Any]:
        """从Vault加载配置"""
        try:
            import hvac
            client = hvac.Client(url=self.url, token=self.token)
            
            # 读取密钥
            result = client.secrets.kv.v2.read_secret_version(
                path=self.path,
                mount_point=self.mount_point
            )
            
            return result['data']['data'] if result and 'data' in result else {}
            
        except Exception as e:
            raise ConfigLoadError(f"Failed to load config from Vault: {e}")

class CompositeConfigLoader(ConfigLoader):
    """组合配置加载器"""
    
    def __init__(self, loaders: list[ConfigLoader], merge_strategy: str = "deep"):
        self.loaders = loaders
        self.merge_strategy = merge_strategy
        
    def load(self) -> Dict[str, Any]:
        """按顺序加载所有配置并合并"""
        from .utils import deep_merge, shallow_merge
        
        merged_config = {}
        for loader in self.loaders:
            config = loader.load()
            if self.merge_strategy == "deep":
                merged_config = deep_merge(merged_config, config)
            else:
                merged_config = shallow_merge(merged_config, config)
                
        return merged_config 