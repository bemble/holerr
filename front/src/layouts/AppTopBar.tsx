import { AppBar, CircularProgress, makeStyles, Toolbar, Typography } from "@material-ui/core";
import React from "react";
import { Helmet } from "react-helmet-async";
import Logo from "../logo.svg";

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
  isLoading?: boolean;
};

const AppTopBar: React.FC<AppTopBarProps> = ({ children, title, isLoading }) => {
  const classes = useStyles();
  return  <>
      <Helmet>
        <title>{[title, "Holerr"].filter(Boolean).join(" - ")}</title>
      </Helmet>
      <AppBar position="relative">
        <Toolbar>
            <img className={classes.logo} src={Logo} alt="Holerr" />
          {children || <>
            <Typography variant="h6" className={classes.title}>
              {title || "App"}
            </Typography>
            {isLoading ? <CircularProgress color="secondary" /> : null}
          </>}
        </Toolbar>
      </AppBar>
    </>;
};

export default AppTopBar;
