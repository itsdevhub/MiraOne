from pathlib import Path


class asset_factory:
    ASSETS_PATH = Path(__file__).resolve().parent / 'model_assets'

    @classmethod
    def hand_landmarker(cls) -> Path:
        return cls.ASSETS_PATH / "hand_landmarker.task"
