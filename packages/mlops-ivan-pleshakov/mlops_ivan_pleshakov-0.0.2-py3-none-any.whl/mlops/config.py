"""Configs."""

from pathlib import Path

from loguru import logger

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")


MODELS_PARAMS_PATH = PROJ_ROOT / "mlops/params/models_params.yaml"
GLOBAL_PARAMS_PATH = PROJ_ROOT / "mlops/params/global_params.yaml"
