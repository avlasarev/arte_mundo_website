
from app import app, db, bcrypt
from app.models import User

# with app.app_context():
#     db.create_all()  # Creates database tables
#
#     # Check if admin user exists
#     admin_user = User.query.filter_by(email='alexander.vlasarev@abv.bg').first()
#     if not admin_user:
#         hashed_password = bcrypt.generate_password_hash('Kaloqnetup26&').decode('utf-8')
#         admin_user = User(username='admin', email='alexander.vlasarev@abv.bg', password=hashed_password, is_admin=True)
#         db.session.add(admin_user)
#         db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates database tables
    app.run(debug=True)
