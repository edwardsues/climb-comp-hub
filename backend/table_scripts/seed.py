import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app, db
from models import Gym, Competition, Climb
from datetime import datetime

with app.app_context():
    gym = Gym(name="Test Gym", address="123 Boulder St")
    db.session.add(gym)
    db.session.flush()  # get gym.id before committing

    comp1 = Competition(
        gym_id=gym.id,
        name="Spring Bouldering Open",
        start_time=datetime(2026, 4, 1, 9, 0),
        end_time=datetime(2026, 4, 1, 17, 0),
    )
    comp2 = Competition(
        gym_id=gym.id,
        name="Spring Lead Qualifier",
        start_time=datetime(2026, 4, 1, 13, 0),  # overlaps with comp1
        end_time=datetime(2026, 4, 1, 20, 0),
    )

    db.session.add_all([comp1, comp2])
    db.session.flush()

    climb1 = Climb(competition_id=comp1.id, grade="V3", points=100)
    climb2 = Climb(competition_id=comp1.id, grade="V6", points=200)
    db.session.add_all([climb1, climb2])

    db.session.commit()
    print(f"Created gym: {gym.name} (id={gym.id})")
    print(f"Created comp: {comp1.name} (id={comp1.id})")
    print(f"Created comp: {comp2.name} (id={comp2.id})")
    print(f"Created climb: {climb1.name} grade={climb1.grade} (id={climb1.id})")
    print(f"Created climb: {climb2.name} grade={climb2.grade} (id={climb2.id})")
