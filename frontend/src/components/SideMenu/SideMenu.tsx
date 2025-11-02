import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import MenuIcon from "@mui/icons-material/Menu";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import {
  type CSSObject,
  styled,
  type Theme,
  ThemeProvider,
} from "@mui/material/styles";
import * as React from "react";
import History from "./History";
import MainMenu from "./MainMenu";
import { SideMenuTheme } from "./SideMenuTheme";

const drawerWidth = 240;

const openedMixin = (theme: Theme): CSSObject => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: "hidden",
  width: drawerWidth,
});

const closedMixin = (theme: Theme): CSSObject => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: "hidden",
  width: theme.spacing(5),
});

const SideMenuDrawer = styled(Drawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  variants: [
    {
      props: ({ open }) => open,
      style: {
        ...openedMixin(theme),
        "& .MuiDrawer-paper": openedMixin(theme),
      },
    },
    {
      props: ({ open }) => !open,
      style: {
        ...closedMixin(theme),
        "& .MuiDrawer-paper": closedMixin(theme),
      },
    },
  ],
}));

const MenuExpander: React.FC<{
  open: boolean;
  onExpand: (open: boolean) => void;
}> = ({ open, onExpand }) => {
  return (
    <Box
      className="menu-expander"
      style={{ display: "flex", justifyContent: "flex-end" }}
    >
      {open ? (
        <IconButton onClick={() => onExpand(false)}>
          <ArrowBackIcon />
        </IconButton>
      ) : (
        <IconButton onClick={() => onExpand(true)}>
          <MenuIcon />
        </IconButton>
      )}
    </Box>
  );
};

const SideMenu: React.FC<{
  open: boolean;
  setOpen: (open: boolean) => void;
}> = ({ open, setOpen }) => {
  const [expand, setExpand] = React.useState(true);
  const onExpand = (flg: boolean) => {
    setOpen(flg);
    if (flg) {
      setExpand(true);
    } else {
      setTimeout(() => {
        setExpand(false);
      }, 150);
    }
  };

  return (
    <SideMenuDrawer className="side-menu" open={open} variant="permanent">
      <ThemeProvider theme={SideMenuTheme}>
        <MenuExpander open={open} onExpand={onExpand} />
        <MainMenu expand={expand} />
        <History />
      </ThemeProvider>
    </SideMenuDrawer>
  );
};

export default SideMenu;
