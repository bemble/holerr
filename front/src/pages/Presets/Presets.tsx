import classes from "./Presets.module.scss";

import {Fab, Grid} from "@material-ui/core";
import {useTranslation} from "react-i18next";
import AppContent from "../../layouts/AppContent";
import AppTopBar from "../../layouts/AppTopBar";
import {useAppSelector} from "../../store";
import {presetsSelector} from "../../store/presets/presets.selectors";
import { useDispatch } from "react-redux";
import { fetchPresets } from "../../store/presets/presets.thunk";
import { useState } from "react";
import {Add as AddIcon} from "@material-ui/icons";
import AddPresetDialog from "./AddPresetDialog";
import EditPresetCard from "./EditPresetCard";

// TODO: add new preset
const Presets = () => {
    const {t} = useTranslation();
    const [addModalOpen, setAddModalOpen] = useState<boolean>(false);

    const allPresets = useAppSelector(presetsSelector.selectAll);

    const dispatch = useDispatch();

    const handlePresetListChanged = () => {
        dispatch(fetchPresets());
    };

    const handleAddPreset = () => {
        setAddModalOpen(false);
        handlePresetListChanged();
    }

    return <>
            <AppTopBar title={t("presets.title")}/>
            <AppContent>
                <Grid container className={classes.root} spacing={2}>
                    {allPresets.map(p => <Grid item key={p.name} xs={12} sm={6}><EditPresetCard preset={p} onDelete={handlePresetListChanged} /></Grid>)}
                </Grid>
                <Fab
                    variant="extended"
                    className={classes.floatingButton}
                    color="primary"
                    onClick={() => setAddModalOpen(true)}
                    >
                    <AddIcon />
                    {t("presets.add_preset")}
                </Fab>
                <AddPresetDialog open={addModalOpen} onCancel={() => setAddModalOpen(false)} onConfirm={handleAddPreset} />
            </AppContent>
        </>;
};

export default Presets;
