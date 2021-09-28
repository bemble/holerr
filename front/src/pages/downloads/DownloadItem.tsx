import {
  Card,
  CardContent,
  CardHeader,
  IconButton,
  ListItemText,
  makeStyles,
  Menu,
  MenuItem
} from "@material-ui/core";
import DeleteIcon from "@material-ui/icons/DeleteOutlined";
import MoreIcon from "@material-ui/icons/MoreVertOutlined";
import { useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { useDispatch } from "react-redux";
import ProgressBar from "../../components/ProgressBar";
import { Download, DownloadStatus } from "../../models/downloads.type";
import {
  DEFAULT_STATUS_CONFIG,
  downloadStatusConfig
} from "../../models/downloads.utils";
import { deleteDownload } from "../../store/downloads/downloads.thunk";
import DownloadItemChips from "./DownloadItemChips";

type DownloadItemProps = {
  item: Download;
};

const useStyles = makeStyles((theme) => ({
  header: {
    wordBreak: "break-all",
    paddingBottom: 0,
  },
}));

const DownloadItem: React.FC<DownloadItemProps> = ({ item }) => {
  const { type, step } =
    downloadStatusConfig.get(item.status) || DEFAULT_STATUS_CONFIG;
  const classes = useStyles();

  const dispatch = useDispatch();

  const handleDeleteClick = () => {
    setMenuOpen(false);
    dispatch(deleteDownload(item.id));
  };

  const moreRef = useRef<any>(null);
  const [isMenuOpen, setMenuOpen] = useState<boolean>(false);

  const { t } = useTranslation();
  const handleMoreClick = () => {
    setMenuOpen(true);
  };
  const handleMenuClose = () => {
    setMenuOpen(false);
  };

  let progress = undefined;
  if(item.status === DownloadStatus.DEBRIDER_DOWNLOADING) {
    progress = item.torrent_info?.progress;
  }
  else if(item.status === DownloadStatus.DOWNLOADER_DOWNLOADING && item.download_info?.progress !== 100) {
    progress = item.download_info?.progress;
  }

  return (
    <>
      <Card elevation={1}>
        <ProgressBar
          stepCount={3}
          step={step}
          type={type}
          progress={progress}
        />
        <CardHeader
          className={classes.header}
          disableTypography
          action={
            <IconButton
              aria-label="settings"
              onClick={handleMoreClick}
              ref={moreRef}
            >
              <MoreIcon />
            </IconButton>
          }
          title={item.title}
        />
        <CardContent>
          <DownloadItemChips item={item} />
        </CardContent>
      </Card>

      <Menu
        anchorEl={moreRef.current}
        keepMounted
        open={isMenuOpen}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleDeleteClick}>
          <DeleteIcon />
          <ListItemText primary={t("downloads_delete")} />
        </MenuItem>
      </Menu>
    </>
  );
};

export default DownloadItem;
