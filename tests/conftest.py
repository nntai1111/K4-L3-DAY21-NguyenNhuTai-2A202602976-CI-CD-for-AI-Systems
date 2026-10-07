import mlflow
import pytest


@pytest.fixture(autouse=True)
def isolated_workdir(tmp_path, monkeypatch):
    """
    Chay moi test trong thu muc tam rieng.

    - outputs/report.json va models/model.joblib duoc ghi vao tmp_path,
      khong ghi de len ket qua huan luyen that cua du an.
    - MLflow ghi vao mlruns/ trong tmp_path, khong lan vao mlflow.db
      hay xung dot voi thu muc mlruns/ cua cac lan chay that.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MLFLOW_TRACKING_URI", raising=False)
    mlflow.set_tracking_uri((tmp_path / "mlruns").as_uri())
    yield
    mlflow.set_tracking_uri(None)
