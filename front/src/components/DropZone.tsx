import { makeStyles } from "@material-ui/core";
import { ReactNode } from "react";

const useStyles = makeStyles((theme) => ({
  root: {
    height: 200,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    borderColor: theme.palette.divider,
    borderStyle: "dashed",
    borderRadius: theme.shape.borderRadius,
    boxSizing: "border-box",
    padding: theme.spacing(8),
    textAlign: "center",
  },
  dragAnDrop: {
    "& p": {
      margin: theme.spacing(2),
    },
  },
}));

type DropZoneProps = {
  isDragActive?: boolean;
  isLoading?: boolean;
  loadingText?: string;
  dragText?: string;
  dropText?: string;
  orText?: string;
  children?: ReactNode;
};
const DropZone = ({
  isDragActive = false,
  isLoading = false,
  loadingText,
  dragText,
  dropText,
  orText,
  children,
}: DropZoneProps) => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      {isLoading ? (
        <p>{loadingText ?? "Loading..."}</p>
      ) : (
        <div className={classes.dragAnDrop}>
          {isDragActive ? (
            <p>{dropText ?? "Release to drop files"}</p>
          ) : (
            <p>{dragText ?? "Drag and drop files"}</p>
          )}
          {Boolean(children) && <p>{orText ?? "or"}</p>}
          {children}
        </div>
      )}
    </div>
  );
};

export default DropZone;
