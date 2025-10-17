import { Typography } from "@mui/material";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import { ThemeProvider } from "@mui/material/styles";
import ChatResponseMenu from "./ChatResponseMenu";
import ChatResponseTheme from "./ChatResponseTheme";

const ChatResponse: React.FC<{ content: string }> = ({ content }) => {
  return (
    <ThemeProvider theme={ChatResponseTheme}>
      <Stack spacing={1}>
        <Paper elevation={0} sx={{ textAlign: "left", padding: 0.5 }}>
          <Typography
            variant="body2"
            color="text.primary"
            sx={{ whiteSpace: "pre-line" }}
          >
            {content}
          </Typography>
        </Paper>
        <ChatResponseMenu />
      </Stack>
    </ThemeProvider>
  );
};

export default ChatResponse;
