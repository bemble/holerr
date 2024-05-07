import classes from "./StateProgress.module.scss";
import { CircularProgress } from "@material-ui/core";
import classnames from "classnames";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCheck,
  faClock,
  faCloudUploadAlt,
  faExclamation,
  faFileDownload,
} from "@fortawesome/free-solid-svg-icons";
import { DownloadStep, DownloadStepStatus } from "../models/downloads.utils";

type StateProgressProps = {
  status?: DownloadStepStatus;
  step?: DownloadStep;
  progress: number;
};

const StateProgress: React.FC<StateProgressProps> = ({
  status,
  step,
  progress,
}) => {
  let icon = faClock;
  let animateIcon = true;
  let iconColor = undefined;
  let torrentClass = classes.progress;
  let downloadClass = classes.progress;

  if (status === DownloadStepStatus.FAILURE) {
    icon = faExclamation;
    iconColor = classes.error;
    if (step === DownloadStep.DEBRIDER) {
      torrentClass = classes.error;
    } else if (step === DownloadStep.DOWNLOADER) {
      torrentClass = classes.done;
      downloadClass = classes.error;
    }
  } else if (status === DownloadStepStatus.SUCCESS) {
    icon = faCheck;
    animateIcon = false;
    iconColor = classes.done;
    torrentClass = classes.done;
    downloadClass = classes.done;
  } else if (step === DownloadStep.DEBRIDER) {
    torrentClass = classes.progress;
    icon = faCloudUploadAlt;
  } else if (step === DownloadStep.DOWNLOADER) {
    torrentClass = classes.done;
    downloadClass = classes.progress;
    icon = faFileDownload;
  }

  return (
    <div className={classes.root}>
      <CircularProgress
        className={classes.torrentBottom}
        variant="determinate"
        value={100}
        thickness={5}
      />
      <CircularProgress
        className={classnames(classes.torrent, torrentClass)}
        variant="determinate"
        value={progress}
        thickness={6}
      />
      <FontAwesomeIcon
        icon={icon}
        className={classnames(classes.icon, iconColor, {
          [classes.animated]: animateIcon,
        })}
      />
    </div>
  );
};

export default StateProgress;
