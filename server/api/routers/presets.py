from server.core import config
from server.core.config_models import Preset
from server.core.config_repositories import PresetRepository
from server.core.exceptions import NotFoundException
from .routers_models import PartialPreset

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
        return PresetRepository.add_preset(preset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{preset_name}", response_model=Preset, tags=["Presets"])
async def update_preset(preset_name: str, preset: PartialPreset):
    try:
        update_data = preset.model_dump(exclude_unset=True)
        return PresetRepository.update_preset(preset_name, update_data)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{preset_name}", tags=["Presets"], status_code=status.HTTP_204_NO_CONTENT
)
async def delete_preset(preset_name):
    try:
        PresetRepository.delete_preset(preset_name)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Preset {preset_name} not found",
        )
