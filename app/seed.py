from app import app, db
from models import Hero, Power, HeroPower

# Flask app context
with app.app_context():
    # Drop existing tables (if any) and create new ones
    db.drop_all()
    db.create_all()

    # Seed Heroes
    hero1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    hero2 = Hero(name="Doreen Green", super_name="Squirrel Girl")
    hero3 = Hero(name="Gwen Stacy", super_name="Spider-Gwen")

    db.session.add_all([hero1, hero2, hero3])
    db.session.commit()

    # Seed Powers
    power1 = Power(name="Super Strength", description="Gives the wielder super-human strengths")
    power2 = Power(name="Flight", description="Gives the wielder the ability to fly through the skies at supersonic speed")

    db.session.add_all([power1, power2])
    db.session.commit()

    # Seed HeroPowers
    heropower1 = HeroPower(strength="Strong", hero=hero1, power=power1)
    heropower2 = HeroPower(strength="Average", hero=hero1, power=power2)
    heropower3 = HeroPower(strength="Weak", hero=hero2, power=power1)
    heropower4 = HeroPower(strength="Strong", hero=hero3, power=power2)

    db.session.add_all([heropower1, heropower2, heropower3, heropower4])
    db.session.commit()

    print("Database seeded successfully!")
