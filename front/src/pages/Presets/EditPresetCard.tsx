import classes from "./Preset.module.scss";
import {  useState } from "react";
import { Card, CardContent, CardHeader, IconButton } from "@material-ui/core";
import httpApi from "../../api/http";
import {Delete as DeleteIcon, Save as SaveIcon} from "@material-ui/icons";
import { Preset } from "../../models/presets.type";
import DeletePresetDialog from "./DeletePresetDialog";
import PresetForm from "./PresetForm";

type EditPresetCardProps = {
    preset: Preset,
    onDelete: () => void
};

const EditPresetCard:React.FC<EditPresetCardProps>= ({preset, onDelete}) => {
    const [displayName, setDisplayName] = useState(preset.name);
    const [currentPreset, setCurrentPreset] = useState(preset);
    const [changed, setChanged] = useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);

    const handlePresetUpdate = (p:Preset) => {
        setCurrentPreset(p);
        setChanged(true);
    };

    const handleDelete = async () => {
        setShowDeleteDialog(false);
        await httpApi.delete(`/presets/${displayName.replace("/", "%2F")}`);
        onDelete();
    };

    const handleUpdate = async (e:React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        await httpApi.patch(`/presets/${displayName.replace("/", "%2F")}`, currentPreset);
        setDisplayName(currentPreset.name);
        setChanged(false);
    };

    return <Card>
        <form onSubmit={handleUpdate}>
            <CardHeader
                title={displayName}
                action={<div>
                    {changed ? <IconButton aria-label="Save" color="secondary" size="small" type="submit">
                        <SaveIcon />
                    </IconButton> : null}
                    <IconButton aria-label="Delete" onClick={() => setShowDeleteDialog(true)} size="small">
                        <DeleteIcon />
                    </IconButton>
                </div>}
            >
            </CardHeader>
            <CardContent className={classes.cardContent}>
                    <PresetForm preset={preset} onUpdate={handlePresetUpdate} />
            </CardContent>
            <DeletePresetDialog open={showDeleteDialog} onCancel={() => setShowDeleteDialog(false)} onConfirm={handleDelete} presetName={displayName} />
        </form>
    </Card>;
}

export default EditPresetCard;