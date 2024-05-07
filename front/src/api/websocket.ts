import store from "../store";

class Socket {
  path: string;
  ws?: WebSocket;
  onMessageStack: Record<string, ((data: any) => any)[]>;
  callStack: string[];

  constructor(path: string) {
    this.path = path;
    this.callStack = [];
    this.onMessageStack = {};
  }

  isConnected() {
    return this.ws && this.ws.readyState === 1;
  }

  connect() {
    let url = window.location.origin.replace("http", "ws") + this.path;
    const apiKey = store.getState().appConfig.apiKey;
    if (apiKey && apiKey.length && !apiKey.startsWith("%holerr-api-key-")) {
      url += `?x-api-key=${apiKey}`;
    }
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      while (this.callStack.length) {
        this.ws && this.ws.send(this.callStack[0]);
        this.callStack.shift();
      }
    };

    this.ws.onmessage = (evt: MessageEvent) => {
      const data = JSON.parse(evt.data) as { action: string; payload: any };
      if (data.action && this.onMessageStack[data.action]) {
        this.onMessageStack[data.action].forEach((c) => c(data.payload));
      }
    };

    this.ws.onclose = () => {
      setTimeout(() => this.connect(), 500);
    };

    this.ws.onerror = () => {
      this.ws && this.ws.close();
    };
  }

  subscribe<T = any>(action: string, callback: (data: T) => any) {
    this.on(action, callback);
    return () => this.off(action, callback);
  }

  on<T = any>(action: string, callback: (data: T) => any) {
    if (!this.onMessageStack[action]) {
      this.onMessageStack[action] = [];
    }
    this.onMessageStack[action].push(callback);
  }

  off<T = any>(action: string, callback: (data: T) => any) {
    const index = this.onMessageStack[action].indexOf(callback);
    this.onMessageStack[action].splice(index, 1);
  }

  send(data: any) {
    const body = JSON.stringify(data);
    if (!this.isConnected()) {
      this.callStack.push(body);
    } else {
      this.ws && this.ws.send(body);
    }
  }
}

let baseURL = (window as any).base_path;
if (baseURL === "/") {
  baseURL = "";
}
baseURL += "/api";
const webSocket = new Socket(`${baseURL}/ws`);

export default webSocket;
