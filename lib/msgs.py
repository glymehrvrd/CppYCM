class MsgTemplates:
    COMPLETION_ERROR_MSG = "[CppYCM][Completion] Error {}"
    COMPLETION_NOT_AVAILABLE_MSG = "[CppYCM] No completion available"
    ERROR_MESSAGE_TEMPLATE = "[{kind}] {text}"
    GET_PATH_ERROR_MSG = "[CppYCM][Path] Failed to replace '{}' -> '{}'"
    NO_HMAC_MESSAGE = "[CppYCM] You should generate HMAC throug the menu before using plugin"
    NOTIFY_ERROR_MSG = "[CppYCM][Notify] Error {}"
    PRINT_ERROR_MESSAGE_TEMPLATE = "[CppYCM] > {} ({},{})\n"
    LOAD_EXTRA_CONF_FINISHED = '[CppYCM] Finished loading extra configuration.'
    LOAD_SERVER_FINISHED = '[CppYCM] Ycmd server registered, location: {}'
    SERVER_NOT_LOADED = '[CppYCM] Ycmd server is not loaded.'