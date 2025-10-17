import { createTheme } from "@mui/material/styles";

const SideMenuTheme = createTheme({
  components: {
    MuiSvgIcon: {
      styleOverrides: {
        root: {
          height: "24px",
          width: "24px",
          margin: "0px",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          justifyContent: "flex-start",
          ":focus:not(:focus-visible)": { outline: "none" },
          height: "40px",
        },
        startIcon: {
          marginLeft: "0px",
        },
      },
      defaultProps: {
        color: "primary",
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          ":focus:not(:focus-visible)": { outline: "none" },
          "& .MuiTouchRipple-root span": {
            borderRadius: 4,
          },
          borderRadius: 4,
          display: "flex",
          justifyContent: "flex-start",
        },
      },
      defaultProps: {
        color: "primary",
      },
    },
  },
});

export { SideMenuTheme };
