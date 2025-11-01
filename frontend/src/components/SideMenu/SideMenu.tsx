import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import EditSquareIcon from "@mui/icons-material/EditSquare";
import MenuIcon from "@mui/icons-material/Menu";
import SearchIcon from "@mui/icons-material/Search";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import type { OverridableComponent } from "@mui/material/OverridableComponent";
import Stack from "@mui/material/Stack";
import type { SvgIconTypeMap } from "@mui/material/SvgIcon";
import {
  type CSSObject,
  styled,
  type Theme,
  ThemeProvider,
} from "@mui/material/styles";
import * as React from "react";
import { SideMenuTheme } from "./SideMenuTheme";

type SvgIconComponent = OverridableComponent<SvgIconTypeMap<{}, "svg">>;

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

const MenuButtonItem: React.FC<{
  expand: boolean;
  Icon: SvgIconComponent;
  text: string;
}> = ({ expand, Icon, text }) => {
  return (
    <>
      {expand ? (
        <Button startIcon={<Icon />}>{text}</Button>
      ) : (
        <IconButton>{<Icon />}</IconButton>
      )}
    </>
  );
};

const MainMenu: React.FC<{ expand: boolean }> = ({ expand }) => {
  return (
    <div className="main-menu">
      <Stack direction="column">
        <MenuButtonItem expand={expand} Icon={EditSquareIcon} text="Edit" />
        <MenuButtonItem expand={expand} Icon={SearchIcon} text="Search" />
      </Stack>
    </div>
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
      </ThemeProvider>
    </SideMenuDrawer>
  );
};

export default SideMenu;
