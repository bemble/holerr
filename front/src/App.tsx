import { HelmetProvider } from "react-helmet-async";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import Main from "./Main";
import store, { persistor } from "./store";
import { createMuiTheme } from "@material-ui/core/styles";
import { CssBaseline, ThemeProvider, useMediaQuery } from "@material-ui/core";
import { pink } from "@material-ui/core/colors";
import { useMemo } from "react";
import { I18nextProvider } from "react-i18next";
import i18n from "./i18n";

const App = () => {
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
  const theme = useMemo(
    () =>
      createMuiTheme({
        spacing: 4,
        palette: {
          primary: {
            light: "#7fb0ef",
            main: "#4b81bc",
            dark: "#03558c",
            contrastText: "#ffffff",
          },
          success: {
            light: "#B8D995",
            main: "#90c45a",
            dark: "#7abe31",
            contrastText: "#ffffff",
          },
          error: {
            light: "#DA867D",
            main: "#ca685d",
            dark: "#9e3428",
            contrastText: "#ffffff",
          },
          secondary: pink,
          type: prefersDarkMode ? "dark" : "light",
        },
        shape: {
          borderRadius: 6,
        },
      }),
    [prefersDarkMode]
  );

  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <HelmetProvider>
          <CssBaseline />
          <ThemeProvider theme={theme}>
            <I18nextProvider i18n={i18n}>
              <Main />
            </I18nextProvider>
          </ThemeProvider>
        </HelmetProvider>
      </PersistGate>
    </Provider>
  );
};

export default App;
