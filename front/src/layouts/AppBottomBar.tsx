import {
  BottomNavigation,
  BottomNavigationAction,
  makeStyles,
} from "@material-ui/core";
import FormatListBulletedIcon from "@material-ui/icons/FormatListBulleted";
import SettingsIcon from "@material-ui/icons/Settings";
import { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { Link, useLocation } from "react-router-dom";

type Links = {
  labelKey: string;
  icon: ReactNode;
  to: string;
};

const links: Links[] = [
  {
    labelKey: "downloads_title",
    icon: <FormatListBulletedIcon />,
    to: "/downloads",
  },
  {
    labelKey: "settings_title",
    icon: <SettingsIcon />,
    to: "/settings",
  },
];

const useStyles = makeStyles((theme) => ({
  root: {
    borderTop: `1px solid ${theme.palette.divider}`,
  },
}));

const AppBottomBar = () => {
  const location = useLocation();
  const classes = useStyles();
  const { t } = useTranslation();
  const value = location.pathname;

  return (
    <BottomNavigation value={value} showLabels className={classes.root}>
      {links.map((link) => (
        <BottomNavigationAction
          key={link.to}
          component={Link}
          to={link.to}
          value={link.to}
          label={t(link.labelKey)}
          icon={link.icon}
        />
      ))}
    </BottomNavigation>
  );
};

export default AppBottomBar;
