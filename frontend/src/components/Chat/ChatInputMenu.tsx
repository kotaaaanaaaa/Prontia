import AddIcon from "@mui/icons-material/Add";
import SendIcon from "@mui/icons-material/Send";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import { ThemeProvider } from "@mui/material/styles";
import ChatInputTheme from "./ChatInputTheme";

const ChatInputMenu: React.FC = () => {
  return (
    <div className="chat-input-menu">
      <ThemeProvider theme={ChatInputTheme}>
        <Stack direction="row" spacing={2}>
          <Stack direction="row">
            <IconButton>
              <AddIcon />
            </IconButton>
          </Stack>
          <Stack direction="row" justifyContent="flex-end" width="100%">
            <IconButton>
              <SendIcon />
            </IconButton>
          </Stack>
        </Stack>
      </ThemeProvider>
    </div>
  );
};

export default ChatInputMenu;
