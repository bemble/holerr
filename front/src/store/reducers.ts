import { combineReducers } from "@reduxjs/toolkit";
import downloads from "./downloads/downloads.slice";
import presets from "./presets/presets.slice";

const reducers = combineReducers({
  downloads: downloads.reducer,
  presets: presets.reducer,
});

export default reducers;
