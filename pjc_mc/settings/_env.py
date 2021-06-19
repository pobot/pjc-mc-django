import environ
from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False),
    SUIT_LIST_PER_PAGE=(int, 20),
)

__HERE__ = Path(__file__).resolve().parent.parent
dot_env_path = __HERE__ / '.env'

if dot_env_path.exists():
    print(f"Loading {dot_env_path} file...")
    environ.Env.read_env()
