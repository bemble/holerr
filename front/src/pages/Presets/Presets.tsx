import classes from "./Presets.module.scss";

import {Grid} from "@material-ui/core";
import {useTranslation} from "react-i18next";
import AppContent from "../../layouts/AppContent";
import AppTopBar from "../../layouts/AppTopBar";
import {useAppSelector} from "../../store";
import {presetsSelector} from "../../store/presets/presets.selectors";
import Preset from "./Preset";
import { useDispatch } from "react-redux";
import { fetchPresets } from "../../store/presets/presets.thunk";

// TODO: add new preset
const Presets = () => {
    const {t} = useTranslation();
    const allPresets = useAppSelector(presetsSelector.selectAll);

    const dispatch = useDispatch();

    const handleDelete = () => {
        dispatch(fetchPresets());
    };

    return <>
            <AppTopBar title={t("presets.title")}/>
            <AppContent>
                <Grid container className={classes.root} spacing={2}>
                    {allPresets.map(p => <Grid item key={p.name} xs={12} sm={6}><Preset preset={p} onDelete={handleDelete} /></Grid>)}
                </Grid>
            </AppContent>
        </>;
};

export default Presets;
