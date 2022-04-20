import { makeStyles } from "@material-ui/core";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
} from "react-router-dom";
import { Download } from "./models/downloads.type";
import webSocket from "./api/websocket";
import useSocketMessage from "./hooks/useSocketMessage";
import AppBottomBar from "./layouts/AppBottomBar";
import {Downloads, Presets, Settings, Status} from "./pages";

import {
  addDownload,
  removeDownload,
  updateDownload,
} from "./store/downloads/downloads.actions";
import { fetchPresets } from "./store/presets/presets.thunk";

export const useAppStyles = makeStyles((theme) => ({
  layout: {
    height: "100%",
    display: "flex",
    flexDirection: "column",
  },
}));

// TODO: create onboarding when no configuration
const Main = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    webSocket.connect();
    dispatch(fetchPresets());
  }, []);

  useSocketMessage<Download>("downloads/update", (data) => {
    const { id, ...content } = data;
    dispatch(updateDownload({ id, changes: content }));
  });

  useSocketMessage<Download>("downloads/new", (data) => {
    dispatch(addDownload(data));
  });

  useSocketMessage<Download>("downloads/delete", (data) => {
    dispatch(removeDownload(data.id));
  });

  const classes = useAppStyles();

  return (
    <div className={classes.layout}>
      <Router basename={process.env.PUBLIC_URL}>
        <Switch>
          <Route path="/downloads" component={Downloads} />
          <Route path="/presets" component={Presets} />
          <Route path="/settings" component={Settings} />
          <Route path="/status" component={Status} />
          <Redirect to="/downloads" />
        </Switch>
        <AppBottomBar />
      </Router>
    </div>
  );
};

export default Main;
