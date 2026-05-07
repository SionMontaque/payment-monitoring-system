from app.api.routes import app
from app.database.db import engine, Base
from app.database.models import Transaction

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(debug=True)