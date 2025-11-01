import { TextField } from "@mui/material";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import * as React from "react";

import ChatInputMenu from "./ChatInputMenu";

const ChatInput: React.FC<{
  onClickSend: (message: string) => void;
}> = ({ onClickSend }) => {
  const [message, setMessage] = React.useState("");

  const onSend = () => {
    onClickSend(message);
    setMessage("");
  };

  return (
    <div className="chat-input">
      <Card sx={{ padding: 1 }}>
        <Stack spacing={1}>
          <TextField
            multiline
            maxRows={4}
            variant="outlined"
            placeholder="Type a message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
          <ChatInputMenu onClickSend={onSend} />
        </Stack>
      </Card>
    </div>
  );
};

export default ChatInput;
