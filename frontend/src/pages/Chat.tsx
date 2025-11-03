import Stack from "@mui/material/Stack";
import * as React from "react";
import { useParams } from "react-router";
import { fetchMessages, sendMessage } from "../api/chat";
import ChatConversation from "../components/Chat/ChatConversation";
import ChatInput from "../components/Chat/ChatInput";
import { type Message, Question, Response } from "../components/Chat/chatModel";

const Chat: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [conv, setConv] = React.useState<Message[]>([]);
  const [convId, setConvId] = React.useState<string | undefined>();

  React.useEffect(() => {
    if (id !== undefined) {
      setConvId(id);

      const fetch = async () => {
        const res = await fetchMessages(id);
        const msgs = res.map((msg) => {
          if (msg.role === "user") {
            return new Question(msg.id, msg.content);
          } else {
            return new Response(msg.id, msg.content);
          }
        });
        setConv(msgs);
      };
      fetch();
    } else {
      setConvId(undefined);
      setConv([]);
    }
  }, [id]);

  const send = async (message: string) => {
    const q = new Question(crypto.randomUUID(), message);
    setConv((prev) => [...prev, q]);
    const res = await sendMessage(message, convId);
    q.id = res.req_id;
    if (convId === undefined) {
      setConvId(res.conversation_id);
    }
    const r = new Response(res.id, res.content);
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
