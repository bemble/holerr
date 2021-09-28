import { RootState } from "..";
import { downloadsAdapter } from "./downloads.slice";

export const downloadsSelector = downloadsAdapter.getSelectors<RootState>(
  (state) => state.downloads
);
