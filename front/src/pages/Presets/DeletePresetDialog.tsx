import { Button, Dialog, DialogActions, DialogContent, DialogTitle } from "@material-ui/core";
import { useTranslation } from "react-i18next";

type DeletePresetDialogProps = {
    open: boolean,
    onCancel: () => void,
    onConfirm: () => void,
    presetName: string
}

const DeletePresetDialog:React.FC<DeletePresetDialogProps> = ({open, presetName, onCancel, onConfirm}) => {
    const {t} = useTranslation();

    return <Dialog maxWidth="xs" aria-labelledby="delete-confirmation-dialog-title" open={open}>
        <DialogTitle id="delete-confirmation-dialog-title">{t("presets.delete_title")}</DialogTitle>
        <DialogContent dividers>
        <p>{t("presets.delete_content", {presetName})}</p>
        </DialogContent>
        <DialogActions>
        <Button autoFocus onClick={onCancel}>
            {t("cancel")}
        </Button>
        <Button onClick={onConfirm} color="primary" variant="contained">
            {t("confirm")}
        </Button>
        </DialogActions>
    </Dialog>;
};

export default DeletePresetDialog;