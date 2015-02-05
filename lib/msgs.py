class MsgTemplates:
    COMPLETION_ERROR_MSG = "[SYCM][Completion] Error {}"
    COMPLETION_NOT_AVAILABLE_MSG = "[SYCM] No completion available"
    ERROR_MESSAGE_TEMPLATE = "[{kind}] {text}"
    GET_PATH_ERROR_MSG = "[SYCM][Path] Failed to replace '{}' -> '{}'"
    NO_HMAC_MESSAGE = "[SYCM] You should generate HMAC throug the menu before using plugin"
    NOTIFY_ERROR_MSG = "[SYCM][Notify] Error {}"
    PRINT_ERROR_MESSAGE_TEMPLATE = "[SYCM] > {} ({},{})\n"
    LOAD_EXTRA_CONF_FINISHED = '[SYCM] Finished loading extra configuration.'
    LOAD_SERVER_FINISHED = '[SYCM] Ycmd server registered, location: {}'
    SERVER_NOT_LOADED = '[SYCM] Ycmd server is not loaded.'