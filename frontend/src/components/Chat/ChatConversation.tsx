import Stack from "@mui/material/Stack";
import type * as React from "react";
import ChatQuestion from "./ChatQuestion";
import ChatResponse from "./ChatResponse";
import { type Message, Question, Response } from "./chatModel";

const ChatConversation: React.FC<{ messages: Message[] }> = ({ messages }) => {
  return (
    <Stack spacing={1}>
      {messages.map((item) => {
        if (item instanceof Question) {
          return <ChatQuestion key={item.id} content={item.content} />;
        }
        if (item instanceof Response) {
          return <ChatResponse key={item.id} content={item.content} />;
        }
        return null;
      })}
    </Stack>
  );
};

export default ChatConversation;
