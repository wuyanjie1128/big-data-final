import os

# Optional cloud vision (not required for this app to work)
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
DASHSCOPE_BASE_URL = os.getenv(
    "DASHSCOPE_BASE_URL",
    "https://dashscope.aliyuncs.com/compatible-mode/v1"
)
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen3-vl-plus")

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "temp_uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
