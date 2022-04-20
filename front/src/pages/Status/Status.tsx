import classes from "./Status.module.scss";
import {
    Button,
    Card,
    CardContent,
    Grid,
} from "@material-ui/core";
import {useTranslation} from "react-i18next";
import AppContent from "../../layouts/AppContent";
import AppTopBar from "../../layouts/AppTopBar";
import {useEffect, useState} from "react";
import httpApi from "../../api/http";
import {Status as StatusType} from "../../models/status.type";
import webSocket from "../../api/websocket";
import { Configuration } from "../../models/configuration.type";
import {StatusDot} from "../../components";
import {Status as StatusDotType} from "../../components/StatusDot";
import classNames from "classnames";

const Status = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [isInDocker, setIsInDocker] = useState(false);
    const [appVersion, setAppVersion] = useState("");
    const [status, setStatus] = useState<StatusType>();
    const {t} = useTranslation();

    // TODO: watch webSocket connection status
    // TODO: reload status when websocket is connected
    useEffect(() => {
        (async () => {
            setIsLoading(true);
            const {data} = await httpApi.get<StatusType>("/status");
            const {data: {is_in_docker, app_version}} = await httpApi.get<Configuration>("/configuration");
            setIsInDocker(is_in_docker);
            setAppVersion(app_version);
            setStatus(data);
            setIsLoading(false);
        })();
    }, []);

    const handleRestart = () => {
        void httpApi.post("/server/restart");
    };

    let debriderStatus:StatusDotType = "pending";
    let downloaderStatus:StatusDotType = "pending";
    if(!isLoading) {
        debriderStatus = status?.debrider_connected ? "success" : "error";
        downloaderStatus = status?.downloader_connected ? "success" : "error";
    }

    return <>
        <AppTopBar title={t("status.title")} isLoading={isLoading} />
        <AppContent>
            <Grid container className={classes.root} justifyContent="center">
                <Grid item xs={12} sm={6}>
                    <Card>
                        <CardContent>
                            <div>{t("status.app_version")} <code className={classNames(classes.code, {[classes.pending]: isLoading})}>{isLoading ? t("loading") : appVersion}</code></div>
                            <div className={classes.spacer} />
                            <hr className={classes.separator} />
                            <div className={classes.spacer} />
                            <Grid container>
                                <Grid item container xs={4} direction="column" alignItems="center">
                                    <StatusDot status={webSocket.isConnected() ? "success" : "error"} /> {t("status.websocket")}
                                </Grid>
                                <Grid item container xs={4} direction="column" alignItems="center">
                                    <StatusDot status={debriderStatus} /> {t("status.debrider")}
                                </Grid>
                                <Grid item container xs={4} direction="column" alignItems="center">
                                    <StatusDot status={downloaderStatus} /> {t("status.downloader")}
                                </Grid>
                            </Grid>
                            {isInDocker ? <>
                                <div className={classes.spacer} />
                                <hr className={classes.separator} />
                                <div className={classes.spacer} />
                                <Grid container justifyContent="center">
                                    <Grid item><Button variant="contained" color="secondary" onClick={handleRestart}>{t("status.restart")}</Button></Grid>
                                    <div className={classes.spacer} />
                                    <Grid item>{t("status.restart_information")}</Grid>
                                </Grid>
                            </> : null}
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </AppContent>
    </>;
};

export default Status;
