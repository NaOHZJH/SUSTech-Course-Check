import os
from re import DEBUG
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    """Configuration class to hold environment variables."""
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    XN = os.getenv("XN")
    XQ = os.getenv("XQ")

    DEBUG = os.getenv("DEBUG", "False").lower() == 'true'

    CAS_LOGIN_URL = "https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas"
    TIS_BASE = "https://tis.sustech.edu.cn"
    QUERY_YXKC_URL = TIS_BASE + "/Xsxk/queryYxkc"