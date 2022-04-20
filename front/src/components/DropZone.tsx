import classes from "./DropZone.module.scss";
import { ReactNode } from "react";


type DropZoneProps = {
  isDragActive?: boolean;
  isLoading?: boolean;
  loadingText?: string;
  dragText?: string;
  dropText?: string;
  orText?: string;
  children?: ReactNode;
};
const DropZone:React.FC<DropZoneProps> = ({
  isDragActive = false,
  isLoading = false,
  loadingText,
  dragText,
  dropText,
  orText,
  children,
}) => {

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
