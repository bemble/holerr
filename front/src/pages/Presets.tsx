import {Card, CardContent, CardHeader, Checkbox, IconButton, InputLabel, makeStyles,} from "@material-ui/core";
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
        margin: theme.spacing(2) + "px auto",
        minWidth: `min(calc(100% - ${theme.spacing(4)}px), ${theme.breakpoints.values.sm}px)`,
        maxWidth: `min(calc(100% - ${theme.spacing(4)}px), ${theme.breakpoints.values.md}px)`,
        display: "flex",
        flexDirection: "column",
        padding: theme.spacing(2),
    }
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
                    {allPresets.map(p => <Card key={p.name} className={classes.root}>
                        <CardHeader
                            title={p.name}
                            action={<IconButton aria-label="Delete" onClick={() => handleDelete(p.name)}>
                                <DeleteIcon />
                            </IconButton>}
                        >
                        </CardHeader>
                        <CardContent>
                            <div>{t("presets.watch_dir")} {p.watch_dir}</div>
                            <div>{t("presets.output_dir")} {p.output_dir}</div>
                            <div>{t("presets.file_extensions")} {p.file_extensions?.join(',') || t("presets.all")}</div>
                            <div>{t("presets.min_file_size")} {p.min_file_size}</div>
                            <InputLabel><Checkbox checked={p.create_sub_dir}
                                                    readOnly={true}/> {t("presets.create_sub_dir")}</InputLabel>
                        </CardContent>
                    </Card>)}
                </div>
            </AppContent>
        </>
    );
};

export default Presets;
