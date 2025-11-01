import { Typography } from "@mui/material";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import { ThemeProvider } from "@mui/material/styles";
import ChatQuestionMenu from "./ChatQuestionMenu";
import ChatQuestionTheme from "./ChatQuestionTheme";

const ChatQuestion: React.FC<{ content: string }> = ({ content }) => {
  return (
    <div style={{ display: "flex", justifyContent: "flex-end" }}>
      <ThemeProvider theme={ChatQuestionTheme}>
        <Stack spacing={1} sx={{ width: "350px" }}>
          <div>
            <Card
              sx={{
                padding: 0.5,
                textAlign: "left",
              }}
            >
              <Typography
                variant="body2"
                color="text.primary"
                sx={{ whiteSpace: "pre-line" }}
              >
                {content}
              </Typography>
            </Card>
          </div>
          <ChatQuestionMenu />
        </Stack>
      </ThemeProvider>
    </div>
  );
};

export default ChatQuestion;
