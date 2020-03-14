import os
import environ

env = environ.Env(
    DEBUG=(bool, False),
    SUIT_LIST_PER_PAGE=(int, 20),
)

if os.path.exists('.env'):
    environ.Env.read_env()
