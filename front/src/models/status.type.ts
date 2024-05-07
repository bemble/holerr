export type Status = {
  app: {
    version: string;
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
