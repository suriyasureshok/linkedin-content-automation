import json
from datetime import datetime
from pathlib import Path
from typing import Optional


STATE_FILE = Path(__file__).parent / "sprint.json"


class SprintStateManager:
    VALID_STATUSES = {"WAITING", "PROCESSING", "COMPLETED", "EXPIRED"}

    @classmethod
    def _read(cls) -> dict:
        if not STATE_FILE.exists():
            cls._initialize()

        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    @classmethod
    def _write(cls, data: dict) -> None:
        with open(STATE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @classmethod
    def _initialize(cls) -> None:
        initial_state = {
            "status": "COMPLETED",
            "sprint_id": None,
            "created_at": None,
            "topic": None,
        }

        cls._write(initial_state)

    @classmethod
    def get_state(cls) -> dict:
        return cls._read()

    @classmethod
    def create_sprint(cls) -> dict:
        current_state = cls._read()

        if current_state["status"] == "WAITING":
            current_state["status"] = "EXPIRED"

        sprint_id = datetime.now().strftime("%Y-%m-%d")

        new_state = {
            "status": "WAITING",
            "sprint_id": sprint_id,
            "created_at": datetime.now().isoformat(),
            "topic": None,
        }

        cls._write(new_state)

        return new_state

    @classmethod
    def save_topic(cls, category: str, subject: str, topic: str) -> dict:

        state = cls._read()

        state["topic"] = {
            "category": category.strip(),
            "subject": subject.strip(),
            "topic": topic.strip(),
        }

        cls._write(state)

        return state

    @classmethod
    def start_processing(cls) -> dict:
        state = cls._read()

        state["status"] = "PROCESSING"

        cls._write(state)

        return state

    @classmethod
    def complete_sprint(cls) -> dict:
        state = cls._read()

        state["status"] = "COMPLETED"

        cls._write(state)

        return state

    @classmethod
    def expire_sprint(cls) -> dict:
        state = cls._read()

        state["status"] = "EXPIRED"

        cls._write(state)

        return state

    @classmethod
    def is_waiting_for_topic(cls) -> bool:
        state = cls._read()

        return state["status"] == "WAITING"

    @classmethod
    def has_active_sprint(cls) -> bool:
        state = cls._read()

        return state["status"] in {"WAITING", "PROCESSING"}

    @classmethod
    def reset(cls) -> dict:
        cls._initialize()
        return cls._read()


if __name__ == "__main__":

    print("\n=== CREATE SPRINT ===")
    print(SprintStateManager.create_sprint())

    print("\n=== SAVE TOPIC ===")
    print(
        SprintStateManager.save_topic(
            category="Backend Engineering", subject="Redis", topic="Memory Management"
        )
    )

    print("\n=== START PROCESSING ===")
    print(SprintStateManager.start_processing())

    print("\n=== COMPLETE ===")
    print(SprintStateManager.complete_sprint())

    print("\n=== FINAL STATE ===")
    print(SprintStateManager.get_state())
