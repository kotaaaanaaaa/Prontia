import Stack from "@mui/material/Stack";
import ChatConversation from "./ChatConversation";
import ChatInput from "./ChatInput";

const Chat: React.FC = () => {
  return (
    <div className="chat-component" style={{ minWidth: "420px" }}>
      <Stack spacing={1}>
        <ChatConversation />
        <ChatInput />
      </Stack>
    </div>
  );
};

export default Chat;
