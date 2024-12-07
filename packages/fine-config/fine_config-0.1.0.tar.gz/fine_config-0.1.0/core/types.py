from enum import Enum, auto
from typing import Any, Dict, Optional, Union

class Environment(str, Enum):
    """环境枚举"""
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"
    
class ConfigValueType(str, Enum):
    """配置值类型"""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    
class ConfigFormat(str, Enum):
    """配置格式"""
    AUTO = "auto"
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    ENV = "env"
    
class ConfigSource(str, Enum):
    """配置来源"""
    FILE = "file"
    ENV = "env"
    REDIS = "redis"
    VAULT = "vault"
    
class ConfigChangeEvent:
    """配置变更事件"""
    def __init__(
        self,
        key: str,
        old_value: Any,
        new_value: Any,
        source: ConfigSource
    ):
        self.key = key
        self.old_value = old_value
        self.new_value = new_value
        self.source = source
        
class ConfigValidationRule:
    """配置验证规则"""
    def __init__(
        self,
        field: str,
        rule_type: str,
        params: Optional[Dict[str, Any]] = None
    ):
        self.field = field
        self.rule_type = rule_type
        self.params = params or {}
        
ConfigValue = Union[str, int, float, bool, list, dict]