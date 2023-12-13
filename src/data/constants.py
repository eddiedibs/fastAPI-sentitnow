from dotenv import load_dotenv
load_dotenv()

import os

DATABASE_URL=os.getenv("DATABASE_URL")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
GRANT_TYPE="password"