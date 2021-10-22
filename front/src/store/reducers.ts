import { combineReducers } from "@reduxjs/toolkit";
import downloads from "./downloads/downloads.slice";
import presets from "./presets/presets.slice";
import appConfig from "./appConfig";

const reducers = combineReducers({
  downloads: downloads.reducer,
  presets: presets.reducer,
  appConfig
});

export default reducers;
