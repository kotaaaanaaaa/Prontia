import Stack from "@mui/material/Stack";
import * as React from "react";
import { sendMessage } from "../api/chat";
import ChatConversation from "../components/Chat/ChatConversation";
import ChatInput from "../components/Chat/ChatInput";
import { type Message, Question, Response } from "../components/Chat/chatModel";

const Chat: React.FC = () => {
  const [conv, setConv] = React.useState<Message[]>([]);

  const send = async (message: string) => {
    const q = new Question(message);
    setConv((prev) => [...prev, q]);
    const res = await sendMessage(message);
    const r = new Response(res.content);
    setConv((prev) => [...prev, r]);
  };

  return (
    <div className="chat-component" style={{ minWidth: "420px" }}>
      <Stack spacing={1}>
        <ChatConversation messages={conv} />
        <ChatInput onClickSend={send} />
      </Stack>
    </div>
  );
};

export default Chat;
