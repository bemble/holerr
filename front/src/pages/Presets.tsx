import {Checkbox, InputLabel, makeStyles,} from "@material-ui/core";
import {useTranslation} from "react-i18next";
import AppContent from "../layouts/AppContent";
import AppTopBar from "../layouts/AppTopBar";
import {useAppSelector} from "../store";
import {presetsSelector} from "../store/presets/presets.selectors";
import {Delete as DeleteIcon} from "@material-ui/icons";
import httpApi from "../api/http";

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

const Presets = () => {
    const {t} = useTranslation();
    const allPresets = useAppSelector(presetsSelector.selectAll);

    // TODO: Add/Edit presets

    const classes = useStyles();

    const handleDelete = (name: string) => {
        void httpApi.delete(`/presets/${name}`);
        // TODO: reload preset list
    };

    // TODO: Better display
    return (
        <>
            <AppTopBar title={t("presets.title")}/>
            <AppContent>
                <div className={classes.root}>
                    {allPresets.map(p => <div key={p.name}>
                        <h4>{p.name} <DeleteIcon onClick={() => handleDelete(p.name)}/></h4>
                        <ul>
                            <li>{t("presets.watch_dir")} {p.watch_dir}</li>
                            <li>{t("presets.output_dir")} {p.output_dir}</li>
                            <li>{t("presets.file_extensions")} {p.file_extensions?.join(',') || t("presets.all")}</li>
                            <li>{t("presets.min_file_size")} {p.min_file_size}</li>
                            <li><InputLabel><Checkbox checked={p.create_sub_dir}
                                                      readOnly={true}/> {t("presets.create_sub_dir")}</InputLabel></li>
                        </ul>
                    </div>)}
                </div>
            </AppContent>
        </>
    );
};

export default Presets;
