import { FormControl, InputLabel, makeStyles, Select } from "@material-ui/core";
import { useTranslation } from "react-i18next";
import AppContent from "../layouts/AppContent";
import AppTopBar from "../layouts/AppTopBar";

type Language = {
  label: string;
  value: string;
};
const LANGUAGES: Language[] = [
  { label: "Français", value: "fr" },
  { label: "English", value: "en" },
];

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

const Settings = () => {
  const { t, i18n } = useTranslation();

  const classes = useStyles();

  return (
    <>
      <AppTopBar title={t("settings_title")} />
      <AppContent>
        <div className={classes.root}>
          <FormControl variant="outlined" className={classes.formControl}>
            <InputLabel htmlFor="language">{t("settings_language")}</InputLabel>
            <Select
              native
              value={i18n.language}
              label={t("settings_language")}
              onChange={(e) => i18n.changeLanguage(e.target.value as string)}
              inputProps={{
                name: "language",
                id: "language",
              }}
            >
              {LANGUAGES.map((l) => (
                <option key={l.value} value={l.value}>
                  {l.label}
                </option>
              ))}
            </Select>
          </FormControl>
        </div>
      </AppContent>
    </>
  );
};

export default Settings;
