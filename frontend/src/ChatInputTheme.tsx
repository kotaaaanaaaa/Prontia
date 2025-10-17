import { createTheme } from "@mui/material/styles";

const ChatInputTheme = createTheme({
  components: {
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

export default ChatInputTheme;
