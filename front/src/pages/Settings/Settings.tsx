import classes from "./Settings.module.scss";

import {
  Button,
  Card,
  CardContent,
  FormControl,
  Grid,
  InputLabel,
  Select,
  TextField,
} from "@material-ui/core";
import { useTranslation } from "react-i18next";
import AppContent from "../../layouts/AppContent";
import AppTopBar from "../../layouts/AppTopBar";
import { ChangeEvent, useEffect, useState } from "react";
import httpApi from "../../api/http";
import { Configuration } from "../../models/configuration.type";

const Settings = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [config, setConfig] = useState<Configuration>();
  // Needed to not override api key and password if no change
  const [newConfig, setNewConfig] = useState<any>({});
  const [hasChange, setHasChange] = useState(false);
  const [restartRequired, setRestartRequired] = useState(false);
  const { t, i18n } = useTranslation();
  const languages = (i18n.options.supportedLngs || []).filter(
    (l) => l !== "cimode"
  );

  useEffect(() => {
    (async () => {
      setIsLoading(true);
      const { data } = await httpApi.get<Configuration>("/configuration");
      setConfig(data);
      setIsLoading(false);
    })();
  }, []);

  useEffect(() => {
    if (newConfig && Object.keys(newConfig).length) {
      setHasChange(true);
    }
  }, [newConfig]);

  const handleChangeBasePath = ({ target }: ChangeEvent<HTMLInputElement>) => {
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

  const handleChangeRealDebridApiKey = ({
    target,
  }: ChangeEvent<HTMLInputElement>) => {
    if (config) {
      const tmpConf = Object.assign({}, config);
      if (!tmpConf.debrider) {
        tmpConf.debrider = { real_debrid: { api_key: "" } };
      }
      tmpConf.debrider.real_debrid.api_key = target.value;

      const tmpNewConfig = Object.assign({}, newConfig);
      tmpNewConfig.debrider = tmpConf.debrider;

      setConfig(tmpConf);
      setNewConfig(tmpNewConfig);
    }
  };

  const handleChangeSynoEndpoint = ({
    target,
  }: ChangeEvent<HTMLInputElement>) => {
    if (config) {
      const tmpConf = Object.assign({}, config);
      if (!tmpConf.downloader) {
        tmpConf.downloader = {
          synology_download_station: {
            endpoint: "",
            username: "",
            password: "",
          },
        };
      }
      tmpConf.downloader.synology_download_station.endpoint = target.value;

      const tmpNewConfig = Object.assign({}, newConfig);
      if (!tmpNewConfig.downloader) {
        tmpNewConfig.downloader = { synology_download_station: {} };
      }
      tmpNewConfig.downloader.synology_download_station.endpoint =
        tmpConf.downloader.synology_download_station.endpoint;

      setConfig(tmpConf);
      setNewConfig(tmpNewConfig);
    }
  };

  const handleChangeSynoUsername = ({
    target,
  }: ChangeEvent<HTMLInputElement>) => {
    if (config) {
      const tmpConf = Object.assign({}, config);
      if (!tmpConf.downloader) {
        tmpConf.downloader = {
          synology_download_station: {
            endpoint: "",
            username: "",
            password: "",
          },
        };
      }
      tmpConf.downloader.synology_download_station.username = target.value;

      const tmpNewConfig = Object.assign({}, newConfig);
      if (!tmpNewConfig.downloader) {
        tmpNewConfig.downloader = { synology_download_station: {} };
      }
      tmpNewConfig.downloader.synology_download_station.username =
        tmpConf.downloader.synology_download_station.username;

      setConfig(tmpConf);
      setNewConfig(tmpNewConfig);
    }
  };

  const handleChangeSynoPassword = ({
    target,
  }: ChangeEvent<HTMLInputElement>) => {
    if (config) {
      const tmpConf = Object.assign({}, config);
      if (!tmpConf.downloader) {
        tmpConf.downloader = {
          synology_download_station: {
            endpoint: "",
            username: "",
            password: "",
          },
        };
      }
      tmpConf.downloader.synology_download_station.password = target.value;

      const tmpNewConfig = Object.assign({}, newConfig);
      if (!tmpNewConfig.downloader) {
        tmpNewConfig.downloader = { synology_download_station: {} };
      }
      tmpNewConfig.downloader.synology_download_station.password =
        tmpConf.downloader.synology_download_station.password;

      setConfig(tmpConf);
      setNewConfig(tmpNewConfig);
    }
  };

  const handleSave = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setIsLoading(true);
    const { data } = await httpApi.patch<Configuration>(
      `/configuration`,
      newConfig
    );
    setConfig(data);
    setIsLoading(false);
  };

  return (
    <>
      <AppTopBar title={t("settings.title")} isLoading={isLoading} />
      <AppContent>
        <Grid container className={classes.root} justifyContent="center">
          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <form onSubmit={handleSave}>
                  <Grid container direction="column">
                    <FormControl
                      variant="outlined"
                      className={classes.formControl}
                      fullWidth
                    >
                      <InputLabel htmlFor="language">
                        {t("settings.language")}
                      </InputLabel>
                      <Select
                        native
                        value={i18n.language}
                        label={t("settings.language")}
                        onChange={(e) =>
                          i18n.changeLanguage(e.target.value as string)
                        }
                        inputProps={{
                          name: "language",
                          id: "language",
                        }}
                      >
                        {languages.map((l) => (
                          <option value={l} key={l}>
                            {t(`languages.${l}`)}
                          </option>
                        ))}
                      </Select>
                    </FormControl>
                    <h2>{t("settings.configuration_subtitle")}</h2>
                    {config ? (
                      <>
                        <TextField
                          value={config.base_path}
                          label={t("settings.configuration_base_path")}
                          onChange={handleChangeBasePath}
                        />
                        <h3>Real-Debrid</h3>
                        <TextField
                          value={config.debrider?.real_debrid.api_key}
                          onChange={handleChangeRealDebridApiKey}
                          label={t("settings.configuration_api_key")}
                        />
                        <div>
                          {t("settings.retrieve_real_debrid_token")}{" "}
                          <a
                            href="https://real-debrid.com/apitoken"
                            className={classes.link}
                            title="Real-Debrid APi Key link"
                          >
                            {t("settings.real_debrid_website")}
                          </a>
                        </div>
                        <h3>Synology Download Station</h3>
                        <TextField
                          value={
                            config.downloader?.synology_download_station
                              .endpoint
                          }
                          onChange={handleChangeSynoEndpoint}
                          label={t("settings.configuration_endpoint")}
                        />
                        <TextField
                          value={
                            config.downloader?.synology_download_station
                              .username
                          }
                          onChange={handleChangeSynoUsername}
                          label={t("settings.configuration_username")}
                        />
                        <TextField
                          value={
                            config.downloader?.synology_download_station
                              .password
                          }
                          onChange={handleChangeSynoPassword}
                          label={t("settings.configuration_password")}
                        />
                        <div className={classes.spacer} />
                        <Button
                          type="submit"
                          variant="contained"
                          color="primary"
                          disabled={!hasChange || isLoading}
                        >
                          {t("settings.configuration_save")}
                        </Button>
                        {restartRequired ? (
                          <p>{t("settings.configuration_restart_required")}</p>
                        ) : null}
                      </>
                    ) : null}
                  </Grid>
                </form>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </AppContent>
    </>
  );
};

export default Settings;
