from __future__ import annotations

from contract import ActorStep, Observation


class FixtureDriver:
    name = "fixture"

    def __init__(self) -> None:
        self.started = False
        self.steps: list[str] = []

    def start(self) -> None:
        self.started = True

    def act(self, step: ActorStep) -> None:
        self.steps.append(f"{step.actor}:{step.text}")

    def observe(self, assertion: str) -> Observation:
        return Observation(
            name=assertion,
            ok=self.started and bool(self.steps),
            evidence={"driver": self.name, "steps": self.steps, "assertion": assertion},
        )

    def stop(self) -> None:
        self.started = False


def run(features: list[dict]) -> dict:
    driver = FixtureDriver()
    driver.start()
    for feature in features:
        driver.act(ActorStep(actor="pm-steward", text=f"execute {feature['feature']}"))
    observations = [
        driver.observe("human reviewer sees the next safe action"),
        driver.observe("operational record contains trigger mode context blockers and checks"),
        driver.observe("operator workbench status links decisions evidence and handoffs"),
    ]
    driver.stop()
    return {
        "ok": all(item.ok for item in observations),
        "driver": driver.name,
        "features": [feature["path"] for feature in features],
        "observations": [
            {"name": item.name, "ok": item.ok, "evidence": item.evidence}
            for item in observations
        ],
    }
