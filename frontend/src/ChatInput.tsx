import { TextField } from "@mui/material";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import ChatInputMenu from "./ChatInputMenu";

const ChatInput: React.FC = () => {
  return (
    <div className="chat-input">
      <Card sx={{ padding: 1 }}>
        <Stack spacing={1}>
          <TextField
            multiline
            maxRows={4}
            variant="outlined"
            placeholder="Type a message..."
          />
          <ChatInputMenu />
        </Stack>
      </Card>
    </div>
  );
};

export default ChatInput;
