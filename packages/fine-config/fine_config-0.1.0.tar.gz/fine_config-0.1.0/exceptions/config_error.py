class ConfigError(Exception):
    """配置相关异常基类"""
    pass

class ConfigNotFoundError(ConfigError):
    """配置未找到异常"""
    pass

class ConfigValidationError(ConfigError):
    """配置验证异常"""
    pass

class ConfigLoadError(ConfigError):
    """配置加载异常"""
    pass 