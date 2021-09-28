import { makeStyles } from "@material-ui/core";
import { Download } from "../../models/downloads.type";
import DownloadItem from "./DownloadItem";

type DownloadListProps = {
  items: Download[];
};

const useStyle = makeStyles((theme) => ({
  root: {
    display: "grid",
    gridGap: theme.spacing(4),
    padding: theme.spacing(4),
    gridTemplateColumns: "repeat(1fr)",
    [theme.breakpoints.up("md")]: {
      gridTemplateColumns: "repeat(2, 1fr)",
    },
    [theme.breakpoints.up("lg")]: {
      gridTemplateColumns: "repeat(3, 1fr)",
    },
  },
}));
const DownloadList: React.FC<DownloadListProps> = ({ items }) => {
  const classes = useStyle();

  return (
    <div className={classes.root}>
      {items.map((item) => (
        <DownloadItem key={item.id} item={item} />
      ))}
    </div>
  );
};

export default DownloadList;
