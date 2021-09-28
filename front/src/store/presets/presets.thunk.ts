import { AppThunk } from "..";
import httpApi from "../../api/http";
import { Preset } from "../../models/presets.type";
import { setAllPresets } from "./presets.actions";

export const fetchPresets = (): AppThunk => async (dispatch) => {
  const { data: presets } = await httpApi.get<Preset[]>("/presets");
  dispatch(setAllPresets(presets));
};
