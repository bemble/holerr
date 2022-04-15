import {Card, CardContent, CardHeader, Checkbox, Chip, FormControl, IconButton, Input, InputLabel, makeStyles, TextField,} from "@material-ui/core";
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
    },
    cardContent: {
        "& > *:not(:first-child)": {
            marginTop: theme.spacing(4)
        }
    },
    chipsContainer: {
        padding: theme.spacing(1)+"px 0",
        "& > *:not(:first-child)": {
            marginLeft: theme.spacing(2)
        }
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

    const handleDeleteExtension = () => {};

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
                        <CardContent className={classes.cardContent}>
                            <TextField
                                label={t("presets.watch_dir")}
                                defaultValue={p.watch_dir}
                                fullWidth={true}
                                InputProps={{
                                    readOnly: true,
                                }} />
                            <TextField
                                label={t("presets.output_dir")}
                                defaultValue={p.output_dir}
                                fullWidth={true}
                                InputProps={{
                                    readOnly: true,
                                }} />
                            <div className="MuiFormControl-root MuiTextField-root MuiFormControl-fullWidth">
                                <label className="MuiFormLabel-root MuiInputLabel-root MuiInputLabel-formControl MuiInputLabel-animated MuiInputLabel-shrink MuiFormLabel-filled" data-shrink="true">
                                    {t("presets.file_extensions")}
                                </label>
                                <div className={"MuiInputBase-root MuiInput-root MuiInput-underline MuiInputBase-fullWidth MuiInput-fullWidth MuiInputBase-formControl MuiInput-formControl " + classes.chipsContainer}>
                                    {(p.file_extensions || [t("presets.all")]).map(e => <Chip key={e} label={e} onDelete={handleDeleteExtension} size="small" />)}
                                </div>
                            </div>
                            <TextField
                                label={t("presets.min_file_size")}
                                defaultValue={p.min_file_size}
                                fullWidth={true}
                                InputProps={{
                                    readOnly: true,
                                }} />
                            <InputLabel>
                                <Checkbox checked={p.create_sub_dir} readOnly={true}/> {t("presets.create_sub_dir")}
                            </InputLabel>
                        </CardContent>
                    </Card>)}
                </div>
            </AppContent>
        </>
    );
};

export default Presets;
