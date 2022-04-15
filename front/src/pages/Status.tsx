import {
    Button,
    Card,
    CircularProgress,
    makeStyles,
} from "@material-ui/core";
import {useTranslation} from "react-i18next";
import AppContent from "../layouts/AppContent";
import AppTopBar from "../layouts/AppTopBar";
import {useEffect, useState} from "react";
import httpApi from "../api/http";
import {Status as StatusType} from "../models/status.type";
import webSocket from "../api/websocket";
import { Configuration } from "../models/configuration.type";

const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
    },
    root: {
        margin: theme.spacing(2) + "px auto",
        minWidth: `min(calc(100% - ${theme.spacing(4)}px), ${theme.breakpoints.values.sm}px)`,
        maxWidth: `min(calc(100% - ${theme.spacing(4)}px), ${theme.breakpoints.values.md}px)`,
        display: "flex",
        flexDirection: "column",
        padding: theme.spacing(4),
    },
}));

const Status = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [isInDocker, setIsInDocker] = useState(false);
    const [status, setStatus] = useState<StatusType>();
    const {t} = useTranslation();

    // TODO: watch webSocket connection status
    // TODO: reload status when websocket is connected
    useEffect(() => {
        (async () => {
            setIsLoading(true);
            const {data} = await httpApi.get<StatusType>("/status");
            const {data: {is_in_docker}} = await httpApi.get<Configuration>("/configuration");
            setIsInDocker(is_in_docker);
            setStatus(data);
            setIsLoading(false);
        })();
    }, []);

    const classes = useStyles();

    const handleRestart = () => {
        void httpApi.post("/server/restart");
    };

    return <>
        <AppTopBar title={t("status.title")} isLoading={isLoading} />
        <AppContent>
            <Card className={classes.root}>
                <div>{t("status.websocket")} {webSocket.isConnected() ? t("status.connected") : t("status.not_connected")}</div>
                {isLoading ? <p>{t("loading")}</p> : null}
                {!isLoading ? <div>{t("status.debrider")} {status?.debrider_connected ? t("status.connected") : t("status.not_connected")}</div> : null}
                {!isLoading ? <div>{t("status.downloader")} {status?.downloader_connected ? t("status.connected") : t("status.not_connected")}</div> : null}
                {isInDocker ? <>
                    <br />
                    <Button variant="contained" color="secondary" onClick={handleRestart}>{t("status.restart")}</Button>
                    <p>{t("status.restart_information")}</p>
                </> : null}
            </Card>
        </AppContent>
    </>;
};

export default Status;
