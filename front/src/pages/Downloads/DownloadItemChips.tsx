import { Chip, Grid, makeStyles } from "@material-ui/core";
import React, { FC, useEffect, useState } from "react";
import { Download } from "../../models/downloads.type";
import { DateTime } from "luxon";
import TimeIcon from "@material-ui/icons/AccessTimeOutlined";
import SettingsIcon from "@material-ui/icons/SettingsOutlined";
import prettyBytes from "pretty-bytes";
import { useTranslation } from "react-i18next";
import { grey } from "@material-ui/core/colors";

const useStyles = makeStyles((theme) => ({
  labels: {
    marginTop: 4,
    overflowY: "auto",
    "&::-webkit-scrollbar": {
      display: "none",
    },
    "& .MuiGrid-root": {
      marginLeft: 4,
    },
    "& .MuiChip-root": {
      color: grey[400],
      borderColor: grey[400],
      fontFamily: "monospace",
    },
    "& .MuiChip-icon": {
      fill: grey[400],
    },
  },
}));
type DownloadItemProps = {
  item: Download;
};
const DownloadItemChips: FC<DownloadItemProps> = ({ item }) => {
  const classes = useStyles();

  return (
    <Grid container justifyContent="flex-end" className={classes.labels}>
      <Grid item>
        <Chip
          size="small"
          icon={<SettingsIcon />}
          label={item.preset}
          variant="outlined"
        />
      </Grid>
      <Grid item>
        <TimeChip date={item.created_at} />
      </Grid>
      {item.total_bytes ? (
        <Grid item>
          <SizeChip size={item.total_bytes} />
        </Grid>
      ) : null}
    </Grid>
  );
};

type SizeChipProps = { size: number };
const SizeChip = React.memo<SizeChipProps>(({ size }) => {
  return size ? (
    <Chip
      size="small"
      icon={<TimeIcon />}
      label={prettyBytes(size)}
      variant="outlined"
    />
  ) : null;
});

const computeSince = (dateTime: DateTime, language: string = "en"): string =>
  dateTime.toRelative({ locale: language }) as string;

type TimeChipProps = { date: string };
const TimeChip = React.memo<TimeChipProps>(({ date }) => {
  const dateTime = DateTime.fromISO(date);

  const { i18n } = useTranslation();

  const [since, setSince] = useState<string>(
    computeSince(dateTime, i18n.language)
  );

  useEffect(() => {
    const interval = setInterval(() => {
      const newSince = computeSince(dateTime, i18n.language);
      if (newSince !== since) setSince(newSince);
    }, 1000);
    return () => {
      clearInterval(interval);
    };
  }, [dateTime]);

  return (
    <Chip size="small" icon={<TimeIcon />} label={since} variant="outlined" />
  );
});

export default DownloadItemChips;
