import classes from "./Status.module.scss";
import { Card, CardContent, Grid } from "@material-ui/core";
import { useTranslation } from "react-i18next";
import AppContent from "../../layouts/AppContent";
import AppTopBar from "../../layouts/AppTopBar";
import { useEffect, useState } from "react";
import httpApi from "../../api/http";
import { Status as StatusType } from "../../models/status.type";
import webSocket from "../../api/websocket";
import { StatusDot } from "../../components";
import { Status as StatusDotType } from "../../components/StatusDot";
import classNames from "classnames";

const Status = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<StatusType>();
  const { t } = useTranslation();

  // TODO: watch webSocket connection status
  // TODO: reload status when websocket is connected
  useEffect(() => {
    (async () => {
      setIsLoading(true);
      const { data } = await httpApi.get<StatusType>("/status");
      setStatus(data);
      setIsLoading(false);
    })();
  }, []);

  let debriderStatus: StatusDotType = "pending";
  let downloaderStatus: StatusDotType = "pending";
  if (!isLoading) {
    debriderStatus = status?.debrider.connected ? "success" : "error";
    downloaderStatus = status?.downloader.connected ? "success" : "error";
  }

  return (
    <>
      <AppTopBar title={t("status.title")} isLoading={isLoading} />
      <AppContent>
        <Grid container className={classes.root} justifyContent="center">
          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <div>
                  {t("status.app_version")}{" "}
                  <code
                    className={classNames(classes.code, {
                      [classes.pending]: isLoading,
                    })}
                  >
                    {isLoading ? t("loading") : status?.app.version}
                  </code>
                </div>
                <div>
                  {t("status.worker_last_run")}{" "}
                  <code
                    className={classNames(classes.code, {
                      [classes.pending]: isLoading,
                    })}
                  >
                    {isLoading
                      ? t("loading")
                      : new Date(
                          status?.app.worker.last_run as any
                        ).toLocaleString()}
                  </code>
                </div>
                <div className={classes.spacer} />
                <hr className={classes.separator} />
                <div className={classes.spacer} />
                <Grid container>
                  <Grid
                    item
                    container
                    xs={4}
                    direction="column"
                    alignItems="center"
                  >
                    <StatusDot
                      status={webSocket.isConnected() ? "success" : "error"}
                    />{" "}
                    {t("status.websocket")}
                  </Grid>
                  <Grid
                    item
                    container
                    xs={4}
                    direction="column"
                    alignItems="center"
                  >
                    <StatusDot status={debriderStatus} />
                    <span>{t("status.debrider")}</span>
                    {status?.debrider ? (
                      <span>({status?.debrider.name})</span>
                    ) : null}
                  </Grid>
                  <Grid
                    item
                    container
                    xs={4}
                    direction="column"
                    alignItems="center"
                  >
                    <StatusDot status={downloaderStatus} />
                    <span>{t("status.downloader")}</span>
                    {status?.downloader ? (
                      <span>({status?.downloader.name})</span>
                    ) : null}
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </AppContent>
    </>
  );
};

export default Status;
