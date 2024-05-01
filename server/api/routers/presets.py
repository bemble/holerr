from server.core import config
from server.core.config_models import Preset
from server.core.config_repositories import PresetRepository

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/presets")


@router.get("/", response_model=list[Preset], tags=["Presets"])
async def list_presets():
    return config.presets


@router.post(
    "/", response_model=Preset, tags=["Presets"], status_code=status.HTTP_201_CREATED
)
async def add_preset(preset: Preset):
    try:
        added_preset = PresetRepository.add_preset(preset)
        return added_preset
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{preset_name}", tags=["Presets"], status_code=status.HTTP_204_NO_CONTENT
)
async def delete_preset(preset_name):
    deleted = PresetRepository.delete_preset(preset_name)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preset {preset_name} not found",
        )
