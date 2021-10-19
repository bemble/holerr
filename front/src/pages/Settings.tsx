import {
    Button,
    Checkbox,
    CircularProgress,
    FormControl,
    InputLabel,
    makeStyles,
    Select,
    TextField
} from "@material-ui/core";
import {useTranslation} from "react-i18next";
import AppContent from "../layouts/AppContent";
import AppTopBar from "../layouts/AppTopBar";
import {ChangeEvent, useEffect, useState} from "react";
import httpApi from "../api/http";
import {Configuration} from "../models/configuration.type";

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
    spacer : {
        height: theme.spacing(4),
        width: "1px"
    }
}));

const Settings = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [config, setConfig] = useState<Configuration>();
    // Needed to not override api key and password if no change
    const [newConfig, setNewConfig] = useState<any>({});
    const [hasChange, setHasChange] = useState(false);
    const [restartRequired, setRestartRequired] = useState(false);
    const {t, i18n} = useTranslation();
    const languages = (i18n.options.supportedLngs || []).filter(l => l !== "cimode");

    useEffect(() => {
        (async () => {
            setIsLoading(true);
            const {data} = await httpApi.get<Configuration>("/configuration");
            setConfig(data);
            setIsLoading(false);
        })();
    }, []);

    useEffect(() => {
        if (newConfig && Object.keys(newConfig).length) {
            setHasChange(true);
        }
    }, [newConfig]);

    const handleChangeDebug = ({target}: ChangeEvent<HTMLInputElement>) => {
        if (config) {
            const tmpConf = Object.assign({}, config);
            tmpConf.debug = target.checked;

            const tmpNewConfig = Object.assign({}, newConfig);
            tmpNewConfig.debug = tmpConf.debug;

            setRestartRequired(true);
            setConfig(tmpConf);
            setNewConfig(tmpNewConfig);
        }
    };

    const handleChangeBasePath = ({target}: ChangeEvent<HTMLInputElement>) => {
        if (config) {
            const tmpConf = Object.assign({}, config);
            tmpConf.base_path = target.value;

            const tmpNewConfig = Object.assign({}, newConfig);
            tmpNewConfig.base_path = tmpConf.base_path;

            setRestartRequired(true);
            setConfig(tmpConf);
            setNewConfig(tmpNewConfig);
        }
    };

    const handleChangeRealDebridApiKey = ({target}: ChangeEvent<HTMLInputElement>) => {
        if (config) {
            const tmpConf = Object.assign({}, config);
            if (!tmpConf.debriders) {
                tmpConf.debriders = {real_debrid: {api_key: ""}};
            }
            tmpConf.debriders.real_debrid.api_key = target.value;

            const tmpNewConfig = Object.assign({}, newConfig);
            tmpNewConfig.debriders = tmpConf.debriders;

            setConfig(tmpConf);
            setNewConfig(tmpNewConfig);
        }
    };

    const handleChangeSynoEndpoint = ({target}: ChangeEvent<HTMLInputElement>) => {
        if (config) {
            const tmpConf = Object.assign({}, config);
            if (!tmpConf.downloaders) {
                tmpConf.downloaders = {synology_download_station: {endpoint: "", username: "", password: ""}};
            }
            tmpConf.downloaders.synology_download_station.endpoint = target.value;

            const tmpNewConfig = Object.assign({}, newConfig);
            if (!tmpNewConfig.downloaders) {
                tmpNewConfig.downloaders = {synology_download_station: {}};
            }
            tmpNewConfig.downloaders.synology_download_station.endpoint = tmpConf.downloaders.synology_download_station.endpoint;

            setConfig(tmpConf);
            setNewConfig(tmpNewConfig);
        }
    };

    const handleChangeSynoUsername = ({target}: ChangeEvent<HTMLInputElement>) => {
        if (config) {
            const tmpConf = Object.assign({}, config);
            if (!tmpConf.downloaders) {
                tmpConf.downloaders = {synology_download_station: {endpoint: "", username: "", password: ""}};
            }
            tmpConf.downloaders.synology_download_station.username = target.value;

            const tmpNewConfig = Object.assign({}, newConfig);
            if (!tmpNewConfig.downloaders) {
                tmpNewConfig.downloaders = {synology_download_station: {}};
            }
            tmpNewConfig.downloaders.synology_download_station.username = tmpConf.downloaders.synology_download_station.username;

            setConfig(tmpConf);
            setNewConfig(tmpNewConfig);
        }
    };

    const handleChangeSynoPassword = ({target}: ChangeEvent<HTMLInputElement>) => {
        if (config) {
            const tmpConf = Object.assign({}, config);
            if (!tmpConf.downloaders) {
                tmpConf.downloaders = {synology_download_station: {endpoint: "", username: "", password: ""}};
            }
            tmpConf.downloaders.synology_download_station.password = target.value;

            const tmpNewConfig = Object.assign({}, newConfig);
            if (!tmpNewConfig.downloaders) {
                tmpNewConfig.downloaders = {synology_download_station: {}};
            }
            tmpNewConfig.downloaders.synology_download_station.password = tmpConf.downloaders.synology_download_station.password;

            setConfig(tmpConf);
            setNewConfig(tmpNewConfig);
        }
    };

    const handleSave = () => {
        (async () => {
            setIsLoading(true);
            const {data} = await httpApi.patch<Configuration>(`/configuration`, newConfig);
            setConfig(data);
            setIsLoading(false);
        })();
    };

    const classes = useStyles();

    return (
        <>
            <AppTopBar title={t("settings.title")}/>
            <AppContent>
                <div className={classes.root}>
                    <FormControl variant="outlined" className={classes.formControl}>
                        <InputLabel htmlFor="language">{t("settings.language")}</InputLabel>
                        <Select
                            native
                            value={i18n.language}
                            label={t("settings.language")}
                            onChange={(e) => i18n.changeLanguage(e.target.value as string)}
                            inputProps={{
                                name: "language",
                                id: "language",
                            }}
                        >
                            {languages.map(l => <option value={l} key={l}>
                                {t(`languages.${l}`)}
                            </option>)}
                        </Select>
                    </FormControl>
                    <h2>{t("settings.configuration_subtitle")} {isLoading ? <CircularProgress/> : null}</h2>
                    {config ? <>
                        <InputLabel><Checkbox checked={config.debug} disabled={isLoading}
                                              onChange={handleChangeDebug}/> {t("settings.configuration_debug")}
                        </InputLabel>
                        <TextField value={config.base_path} label={t("settings.configuration_base_path")}
                                   onChange={handleChangeBasePath}/>
                        <h3>Real-Debrid</h3>
                        <TextField value={config.debriders?.real_debrid.api_key} onChange={handleChangeRealDebridApiKey}
                                   label={t("settings.configuration_api_key")}/>
                        Retrieve your API key here: <a href="https://real-debrid.com/apitoken"
                                                       title="Real-Debrid APi Key link">Real-debrid website</a>
                        <h3>Synology Download Station</h3>
                        <TextField value={config.downloaders?.synology_download_station.endpoint}
                                   onChange={handleChangeSynoEndpoint}
                                   label={t("settings.configuration_endpoint")}/>
                        <TextField value={config.downloaders?.synology_download_station.username}
                                   onChange={handleChangeSynoUsername}
                                   label={t("settings.configuration_username")}/>
                        <TextField value={config.downloaders?.synology_download_station.password}
                                   onChange={handleChangeSynoPassword}
                                   label={t("settings.configuration_password")}/>
                        <div className={classes.spacer} />
                        <Button variant="contained" color="primary" disabled={!hasChange || isLoading}
                                onClick={handleSave}>{t("settings.configuration_save")}</Button>
                        {restartRequired ? <p>{t("settings.configuration_restart_required")}</p> : null}
                    </> : null}
                </div>
            </AppContent>
        </>
    );
};

export default Settings;
