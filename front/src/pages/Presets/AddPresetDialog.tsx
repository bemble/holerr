import { Button, Dialog, DialogActions, DialogContent, DialogTitle } from "@material-ui/core";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import httpApi from "../../api/http";
import { Preset } from "../../models/presets.type";
import PresetForm from "./PresetForm";

type DeletePresetDialogProps = {
    open: boolean,
    onCancel: () => void,
    onConfirm: () => void
}

const AddPresetDialog:React.FC<DeletePresetDialogProps> = ({open, onCancel, onConfirm}) => {
    const {t} = useTranslation();
    const [isLoading, setIsLoading] = useState(false);
    const [isValid, setIsValid] = useState(false);
    const [currentPreset, setCurrentPreset] = useState({});

    const handlePresetUpdate = (p:Preset) => {
      setCurrentPreset(p);
      setIsValid(!!(p.name.length && p.output_dir.length && p.watch_dir.length));
    };

    const handleConfirm = async (e:React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();

      setIsLoading(true);
      await httpApi.post(`/presets`, currentPreset);
      setIsLoading(false);
      onConfirm();
  };

    return <Dialog maxWidth="xs" aria-labelledby="add-dialog-title" open={open}>
        <form onSubmit={handleConfirm}>
          <DialogTitle id="add-dialog-title">{t("presets.add_title")}</DialogTitle>
          <DialogContent dividers>
            <PresetForm preset={{} as Preset} onUpdate={handlePresetUpdate} />
          </DialogContent>
          <DialogActions>
          <Button autoFocus onClick={onCancel} disabled={isLoading}>
              {t("cancel")}
          </Button>
          <Button type="submit" color="primary" variant="contained" disabled={isLoading || !isValid}>
              {t("add")}
          </Button>
          </DialogActions>
        </form>
    </Dialog>;
};

export default AddPresetDialog;