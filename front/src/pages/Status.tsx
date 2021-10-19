import {
    Button,
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

const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
    },
    root: {
        margin: "0 auto",
        maxWidth: theme.breakpoints.width("sm"),
        display: "flex",
        flexDirection: "column",
        padding: theme.spacing(4),
    },
}));

const Status = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [status, setStatus] = useState<StatusType>();
    const {t} = useTranslation();

    // TODO: watch webSocket connection status
    // TODO: reload status when websocket is connected
    useEffect(() => {
        (async () => {
            setIsLoading(true);
            const {data} = await httpApi.get<StatusType>("/status");
            setStatus(data);
            setIsLoading(false);
        })();
    }, []);

    const classes = useStyles();

    const handleRestart = () => {
        (async () => {
            await httpApi.post("/server/restart");
        })();
    };

    return (
        <>
            <AppTopBar title={t("status.title")}/>
            <AppContent>
                <div className={classes.root}>
                    <p>{t("status.websocket")} {webSocket.isConnected() ? t("status.connected") : t("status.not_connected")}</p>
                    {isLoading ? <CircularProgress /> : null}
                    <p>{t("status.debrider")} {status?.debrider_connected ? t("status.connected") : t("status.not_connected")}</p>
                    <p>{t("status.downloader")} {status?.downloader_connected ? t("status.connected") : t("status.not_connected")}</p>
                    <Button variant="contained" color="secondary" onClick={handleRestart}>{t("status.restart")}</Button>
                    <p>{t("status.restart_information")}</p>
                </div>
            </AppContent>
        </>
    );
};

export default Status;
