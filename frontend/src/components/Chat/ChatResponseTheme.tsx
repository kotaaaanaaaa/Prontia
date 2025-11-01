import { createTheme } from "@mui/material/styles";

const ChatResponseTheme = createTheme({
  components: {
    MuiSvgIcon: {
      styleOverrides: {
        root: {
          height: "18px",
          width: "18px",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          justifyContent: "flex-start",
          ":focus:not(:focus-visible)": { outline: "none" },
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          ":focus:not(:focus-visible)": { outline: "none" },
          "& .MuiTouchRipple-root span": {},
        },
      },
    },
  },
});

export default ChatResponseTheme;
