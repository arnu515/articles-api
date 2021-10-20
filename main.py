from src import app
from os import getenv

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    app.run(debug=bool(getenv("DEBUG")), port=int(getenv("PORT", "5000")), host="0.0.0.0" if bool(getenv("HOST")) else None)
