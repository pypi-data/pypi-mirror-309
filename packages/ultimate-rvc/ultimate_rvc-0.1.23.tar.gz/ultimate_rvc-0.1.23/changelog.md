# CHANGELOG

This pr fixes the excessive logging that is coming from third party packages (libraries). It does not by manually configuring `logging.BasicConfig` in `__init__.py` of the root of the ultimate-rvc package. The logging has been made configurable via environment variables. The environment variables are:

* `URVC_CONSOLE_LOG_LEVEL`: The log level for console logging. If not set, defaults to `ERROR`.
* `URVC_FILE_LOG_LEVEL`: The log level for file logging. If not set, defaults to `INFO`.
* `URVC_LOGS_DIR`: The directory in which log files will be stored. If not set, logs will be stored in a `logs` directory in the current working directory.
* `URVC_NO_LOGGING`: If set to `1`, logging will be disabled.