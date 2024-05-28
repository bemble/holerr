export type Status = {
  app: {
    version: string;
    worker: {
      last_run: string;
    };
  };
  debrider: {
    id: string;
    name: string;
    connected: boolean;
  };
  downloader: {
    id: string;
    name: string;
    connected: boolean;
  };
};
