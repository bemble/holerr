import {
  AppBar,
  Button,
  Dialog,
  FormControl,
  IconButton,
  InputLabel,
  List,
  ListItem,
  ListItemIcon,
  ListItemSecondaryAction,
  ListItemText,
  makeStyles,
  Select,
  Slide,
  Toolbar,
  Typography,
  useMediaQuery,
  useTheme,
} from "@material-ui/core";
import { TransitionProps } from "@material-ui/core/transitions/transition";
import ClearIcon from "@material-ui/icons/Clear";
import CloseIcon from "@material-ui/icons/Close";
import DescriptionIcon from "@material-ui/icons/Description";
import prettyBytes from "pretty-bytes";
import { FC, forwardRef, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import { useTranslation } from "react-i18next";
import httpApi from "../../api/http";
import {DropZone, FilesInput} from "../../components";
import { useAppSelector } from "../../store";
import { presetsSelector } from "../../store/presets/presets.selectors";

const Transition = forwardRef(function Transition(
  props: TransitionProps & { children?: React.ReactElement },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const useStyles = makeStyles((theme) => ({
  appBar: {
    position: "relative",
    overflow: "hidden",
  },
  title: {
    flex: 1,
  },
  content: {
    overflow: "auto",
    position: "relative",
    flex: 1,
    display: "flex",
    flexDirection: "column",
    padding: theme.spacing(2),
    paddingTop: 0,
    paddingBottom: 0,
  },
  bottomBar: {
    padding: theme.spacing(2),
  },
  form: {
    height: "100%",
    display: "flex",
    flexDirection: "column",
    overflow: "auto",
  },
  presetSelector: {
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(2),
    width: "100%",
  },
  fileList: {
    padding: 0,
    marginTop: theme.spacing(2),
    flex: 1,
    overflow: "auto",
    borderColor: theme.palette.divider,
    borderStyle: "solid",
    borderWidth: 1,
    borderRadius: theme.shape.borderRadius,
  },
}));

const uploadTorrent = async (file: File, preset: string) => {
  if (file && preset) {
    const body = new FormData();
    body.append("preset", preset);
    body.append("torrent_file", file, file.name);

    await httpApi.post("/downloads", body, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  }
};

type AddDownloadsDialogProps = {
  open: boolean;
  onClose: () => any;
};
const AddDownloadsDialog: FC<AddDownloadsDialogProps> = ({ open, onClose }) => {
  const classes = useStyles();

  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("xs"));
  const { t } = useTranslation();

  // Files
  const [files, setFiles] = useState<File[]>([]);

  // Remove all files on close
  useEffect(() => {
    if (!open) {
      setFiles([]);
    }
  }, [open]);

  const addFiles = (newFiles: File[]) => {
    setFiles((state) => [...state, ...newFiles]);
  };

  const removeFile = (file: File) => {
    setFiles((state) => state.filter((f) => f !== file));
  };

  // Presets
  const allPresets = useAppSelector(presetsSelector.selectAll);
  const [presetName, setPresetName] = useState<string>();

  // Select first preset in the list by default
  useEffect(() => {
    setPresetName(allPresets[0]?.name);
  }, [allPresets]);

  // Drop actions
  const { getInputProps, getRootProps, isDragActive } = useDropzone({
    onDrop: addFiles,
    accept: ".torrent",
    multiple: true,
    noClick: true,
  });

  // Submit
  const isValid = presetName && files.length > 0;
  const [isLoading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    for (let f of files) {
      await uploadTorrent(f, presetName as string);
    }
    onClose();
    setFiles([]);
    setLoading(false);
  };

  return (
    <Dialog
      fullScreen={fullScreen}
      maxWidth="xs"
      fullWidth={true}
      open={open}
      onClose={onClose}
      TransitionComponent={Transition}
    >
      <form onSubmit={handleSubmit} className={classes.form}>
        <AppBar className={classes.appBar}>
          <Toolbar>
            <Typography variant="h6" className={classes.title}>
              {t("downloads_add_torrents_title")}
            </Typography>
            <IconButton
              edge="end"
              color="inherit"
              onClick={onClose}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
        <div className={classes.content} {...getRootProps()}>
          <input {...getInputProps()} />
          <FormControl variant="outlined" className={classes.presetSelector}>
            <InputLabel id="preset">{t("downloads_preset")}</InputLabel>
            <Select
              native
              id="preset"
              value={presetName || ""}
              onChange={(e) => setPresetName(e.currentTarget.value as string)}
              label={t("downloads_preset")}
            >
              <option value="" disabled hidden></option>
              {allPresets.map((preset) => (
                <option value={preset.name} key={preset.name}>
                  {preset.name}
                </option>
              ))}
            </Select>
          </FormControl>
          <DropZone
            isDragActive={isDragActive}
            isLoading={isLoading}
            dragText={t("downloads_add_torrents_drag_drop_files")}
            dropText={t("downloads_add_torrents_drop_files")}
            loadingText={t("downloads_add_torrents_loading")}
            orText={t("or")}
          >
            <FilesInput onNewFiles={addFiles}>
              {t("downloads_add_torrents_browse")}
            </FilesInput>
          </DropZone>
          {files.length > 0 && (
            <List dense className={classes.fileList}>
              {files.map((f, index) => (
                <FileItem key={index} file={f} onDelete={removeFile} />
              ))}
            </List>
          )}
        </div>
        <div className={classes.bottomBar}>
          <Button
            type="submit"
            fullWidth
            color="primary"
            variant="contained"
            disabled={!isValid || isLoading}
          >
            {t("downloads_add_torrents_action", { count: files.length })}
          </Button>
        </div>
      </form>
    </Dialog>
  );
};

type FileItemProps = {
  file: File;
  onDelete: (file: File) => any;
};
const FileItem = ({ file, onDelete }: FileItemProps) => {
  const handleDelete = () => {
    onDelete(file);
  };
  return (
    <ListItem>
      <ListItemIcon>
        <DescriptionIcon />
      </ListItemIcon>
      <ListItemText
        primary={file.name}
        primaryTypographyProps={{ noWrap: true }}
        secondary={prettyBytes(file.size)}
      />
      <ListItemSecondaryAction>
        <IconButton edge="end" aria-label="delete" onClick={handleDelete}>
          <ClearIcon />
        </IconButton>
      </ListItemSecondaryAction>
    </ListItem>
  );
};

export default AddDownloadsDialog;
