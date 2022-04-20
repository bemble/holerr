import {
  Fab,
  IconButton,
  makeStyles,
  Tooltip,
  Typography
} from "@material-ui/core";
import AddIcon from "@material-ui/icons/Add";
import ClearAllIcon from "@material-ui/icons/ClearAll";
import RefreshIcon from "@material-ui/icons/RefreshOutlined";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import AppContent from "../../layouts/AppContent";
import AppTopBar from "../../layouts/AppTopBar";
import { useAppDispatch, useAppSelector } from "../../store";
import { downloadsSelector } from "../../store/downloads/downloads.selectors";
import {
  cleanUpDownload,
  fetchDownloads
} from "../../store/downloads/downloads.thunk";
import AddDownloadsDialog from "./AddDownloadsDialog";
import DownloadList from "./DownloadList";

const useStyles = makeStyles((theme) => ({
  rightButton: {
    marginLeft: theme.spacing(1.5),
  },
  title: {
    flex: 1,
  },
  floatingButton: {
    position: "absolute",
    bottom: theme.spacing(2),
    right: theme.spacing(2),
  },
}));

const Downloads = () => {
  const dispatch = useAppDispatch();

  const classes = useStyles();

  const downloads = useAppSelector(downloadsSelector.selectAll);

  useEffect(() => {
    dispatch(fetchDownloads());
  }, []);

  const cleanUp = () => {
    dispatch(cleanUpDownload());
  };

  const refresh = () => {
    dispatch(fetchDownloads());
  };

  const [addModalOpen, setAddModalOpen] = useState<boolean>(false);

  const { t } = useTranslation();

  return (
    <>
      <AppTopBar title={t("downloads_title")}>
        <Typography variant="h6" className={classes.title}>
          {t("downloads_title")}
        </Typography>
        <Tooltip title={t("downloads_refresh") || ""}>
          <IconButton
            edge="end"
            className={classes.rightButton}
            color="inherit"
            aria-label="menu"
            onClick={refresh}
          >
            <RefreshIcon />
          </IconButton>
        </Tooltip>
        <Tooltip title={t("downloads_clear_all") || ""}>
          <IconButton
            edge="end"
            className={classes.rightButton}
            color="inherit"
            aria-label="menu"
            onClick={cleanUp}
          >
            <ClearAllIcon />
          </IconButton>
        </Tooltip>
      </AppTopBar>
      <AppContent>
        <DownloadList items={downloads} />
        <Fab
          variant="extended"
          className={classes.floatingButton}
          color="primary"
          onClick={() => setAddModalOpen(true)}
        >
          <AddIcon />
          {t("downloads_add_torrents")}
        </Fab>
      </AppContent>
      <AddDownloadsDialog
        open={addModalOpen}
        onClose={() => setAddModalOpen(false)}
      />
    </>
  );
};

export default Downloads;
