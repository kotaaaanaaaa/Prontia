import { createTheme } from "@mui/material/styles";

const HistoryTheme = createTheme({
  components: {
    MuiListItemButton: {
      styleOverrides: {
        root: {
          height: "36px",
          margin: "0px",
        },
      },
    },
  },
});

export { HistoryTheme };
