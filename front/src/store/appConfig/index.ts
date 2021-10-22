import {createAction, createReducer} from "@reduxjs/toolkit";

type AppConfigState = {
    apiKey: string
}

const initialState: AppConfigState = {
    apiKey: process.env.REACT_APP_API_KEY || "%holerr-api-key-placeholder%"
};

const set = createAction<Partial<AppConfigState>>("appConfig/set");

export default createReducer(initialState, (builder) => {
    builder.addCase(set, (state, {payload}) => {
        Object.assign(state, payload);
    });
});