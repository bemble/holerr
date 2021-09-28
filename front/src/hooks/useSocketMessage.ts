import { useEffect } from "react";
import webSocket from "../api/websocket";

function useSocketMessage<T = any>(
  action: string,
  callback: (data: T) => any
) {
  useEffect(() => {
    webSocket.on(action, callback);
    return () => webSocket.off(action, callback);
  }, []);
};

export default useSocketMessage;
