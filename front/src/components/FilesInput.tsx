import { Button } from "@material-ui/core";
import { ChangeEvent, ReactNode, useRef } from "react";

type FilesInputProps = {
  onNewFiles?: (files: File[]) => any;
  children: ReactNode;
};
const FilesInput:React.FC<FilesInputProps> = ({ onNewFiles, children }) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const onFilesAdded = (e: ChangeEvent<HTMLInputElement>) => {
    const newFiles = Array.from(e.target.files ?? []);
    if (newFiles.length > 0) {
      onNewFiles?.(newFiles);
    }
    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <label htmlFor="browse">
      <Button variant="contained" color="primary" component="span">
        <input
          id="browse"
          type="file"
          hidden
          onChange={onFilesAdded}
          ref={inputRef}
          accept=".torrent"
          multiple
        />
        {children}
      </Button>
    </label>
  );
};

export default FilesInput;
