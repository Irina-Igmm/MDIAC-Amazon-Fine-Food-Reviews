from fastapi.testclient import TestClient

from src.api import app as api

client = TestClient(api.app)


class FakeModel:
    def predict_proba(self, X):
        return [[0.1, 0.9] for _ in X]


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_predict(monkeypatch, tmp_path):
    log_path = tmp_path / "predictions.jsonl"
    monkeypatch.setattr(api, "_model", FakeModel())
    monkeypatch.setattr(api, "PREDICTION_LOG", log_path)

    resp = client.post("/predict", json={"text": "Delicious!"})
    assert resp.status_code == 200
    assert resp.json()["sentiment"] == "positif"
    assert log_path.exists()
