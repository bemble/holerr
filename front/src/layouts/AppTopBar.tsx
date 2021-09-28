import { AppBar, makeStyles, Toolbar, Typography } from "@material-ui/core";
import React from "react";
import { Helmet } from "react-helmet-async";

const useStyles = makeStyles((theme) => ({
    logo: {
        width: 48,
        marginRight: theme.spacing()
    },
  title: {
    flexGrow: 1,
  },
}));

type AppTopBarProps = {
  title?: string;
};

const AppTopBar: React.FC<AppTopBarProps> = ({ children, title }) => {
  const classes = useStyles();
  return (
    <>
      <Helmet>
        <title>{[title, "Holerr"].filter(Boolean).join(" - ")}</title>
      </Helmet>
      <AppBar position="relative">
        <Toolbar>
            <img className={classes.logo} src={process.env.PUBLIC_URL + "/icon/apple-touch-icon.png"} alt="Holerr" />
          {children || (
            <Typography variant="h6" className={classes.title}>
              {title || "App"}
            </Typography>
          )}
        </Toolbar>
      </AppBar>
    </>
  );
};

export default AppTopBar;
