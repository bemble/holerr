import { createEntityAdapter, createSlice } from "@reduxjs/toolkit";
import { Download } from "../../models/downloads.type";

export const downloadsAdapter = createEntityAdapter<Download>({
  selectId: (downlaod) => downlaod.id,
  sortComparer: (a, b) => new Date(a.created_at).getTime() < new Date(b.created_at).getTime() ? 1 : -1,
});

const slice = createSlice({
  name: "downloads",
  initialState: downloadsAdapter.getInitialState(),
  reducers: {
    setAllDownload: downloadsAdapter.setAll,
    removeDownload: downloadsAdapter.removeOne,
    updateDownload: downloadsAdapter.updateOne,
    addDownload: downloadsAdapter.addOne,
  },
});

export default slice;
