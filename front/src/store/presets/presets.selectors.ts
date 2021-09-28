import { RootState } from "..";
import { presetsAdapter } from "./presets.slice";

export const presetsSelector = presetsAdapter.getSelectors<RootState>(
  (state) => state.presets
);
