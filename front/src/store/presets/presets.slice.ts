import { createEntityAdapter, createSlice } from "@reduxjs/toolkit";
import { Preset } from "../../models/presets.type";

export const presetsAdapter = createEntityAdapter<Preset>({
  selectId: (preset) => preset.name,
  sortComparer: (a, b) => a.name.localeCompare(b.name),
});

const slice = createSlice({
  name: "downloads",
  initialState: presetsAdapter.getInitialState(),
  reducers: {
    setAllPresets: presetsAdapter.setAll,
  },
});

export default slice;
