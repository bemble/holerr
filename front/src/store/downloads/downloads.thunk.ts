import {AppThunk} from "..";
import {Download} from "../../models/downloads.type";
import httpApi from "../../api/http";
import {setAllDownload} from "./downloads.actions";

export const fetchDownloads = (): AppThunk => async (dispatch) => {
    const { data: downloads } = await httpApi.get<Download[]>("/downloads");
    dispatch(setAllDownload(downloads as Download[]));
};

export const deleteDownload = (id: string): AppThunk => async (dispatch) => {
    await httpApi.delete<void>(`/downloads/${id}`);
};

export const cleanUpDownload = (): AppThunk => async (dispatch) => {
    await httpApi.post<void>("/downloads/clean_up");
};
