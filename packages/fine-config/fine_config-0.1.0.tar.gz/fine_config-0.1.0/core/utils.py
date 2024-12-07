from typing import Any, Dict, Optional
import copy
import json
from pathlib import Path

def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """深度合并两个字典
    
    Args:
        base: 基础字典
        override: 覆盖字典
        
    Returns:
        合并后的字典
    """
    result = copy.deepcopy(base)
    
    for key, value in override.items():
        if (
            key in result and 
            isinstance(result[key], dict) and 
            isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
            
    return result

def shallow_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """浅合并两个字典"""
    result = copy.deepcopy(base)
    result.update(override)
    return result

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """将嵌套字典展平为单层字典
    
    Example:
        >>> flatten_dict({'a': {'b': 1, 'c': 2}})
        {'a.b': 1, 'a.c': 2}
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def unflatten_dict(d: Dict[str, Any], sep: str = '.') -> Dict[str, Any]:
    """将单层字典还原为嵌套字典
    
    Example:
        >>> unflatten_dict({'a.b': 1, 'a.c': 2})
        {'a': {'b': 1, 'c': 2}}
    """
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        target = result
        for part in parts[:-1]:
            target = target.setdefault(part, {})
        target[parts[-1]] = value
    return result

def interpolate_env_vars(value: str) -> str:
    """替换字符串中的环境变量
    
    Example:
        >>> os.environ['USER'] = 'john'
        >>> interpolate_env_vars('Hello ${USER}!')
        'Hello john!'
    """
    import os
    import re
    
    pattern = r'\$\{([^}]+)\}'
    
    def replace(match):
        env_var = match.group(1)
        return os.environ.get(env_var, match.group(0))
        
    return re.sub(pattern, replace, value)

def load_json_file(file_path: str | Path) -> Dict[str, Any]:
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
        
def save_json_file(data: Dict[str, Any], file_path: str | Path) -> None:
    """保存JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
def parse_bool(value: Any) -> bool:
    """解析布尔值
    
    支持多种格式：true/false, yes/no, 1/0, on/off
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        value = value.lower().strip()
        if value in ('true', 'yes', '1', 'on'):
            return True
        if value in ('false', 'no', '0', 'off'):
            return False
    raise ValueError(f"Cannot parse boolean value: {value}")

def mask_sensitive_value(value: str) -> str:
    """掩码敏感信息
    
    Example:
        >>> mask_sensitive_value("my-secret-key")
        'my-***-key'
    """
    if not value or len(value) < 8:
        return "***"
    return f"{value[:3]}***{value[-3:]}" 