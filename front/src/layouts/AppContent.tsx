import { makeStyles } from "@material-ui/core";
import clsx from "clsx";

const useStyles = makeStyles((theme) => ({
  content: {
    backgroundColor: theme.palette.background.default,
    overflow: "auto",
    position: "relative",
    flex: 1,
  },
  scrollable: {
    overflowY: "auto",
    overflowX: "hidden",
    height: "100%",
    width: "100%",
  },
}));

const AppContent: React.FC<{ className?: string }> = ({
  children,
  className,
}) => {
  const classes = useStyles();
  return (
    <div className={classes.content}>
      <div className={clsx(classes.scrollable, className)}>{children}</div>
    </div>
  );
};

export default AppContent;
