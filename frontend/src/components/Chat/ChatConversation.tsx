import Stack from "@mui/material/Stack";
import ChatQuestion from "./ChatQuestion";
import ChatResponse from "./ChatResponse";

const ChatConversation: React.FC = () => {
  const q1 = "こんにちは。\n今日はどんなことができますか？";
  const a1 =
    "こんにちは！\n\n私はテキストの要約、質問への回答、アイデア出しなど\nいろいろなお手伝いができます。";
  const q2 = "じゃあ、簡単な自己紹介を書いてください。";
  const a2 =
    "もちろんです。\n\n私はAIアシスタントです。\nあなたの質問に答えたり、文章を作成したり、\nコードを書くお手伝いもできます。";
  return (
    <Stack spacing={1}>
      <ChatQuestion content={q1} />
      <ChatResponse content={a1} />
      <ChatQuestion content={q2} />
      <ChatResponse content={a2} />
    </Stack>
  );
};

export default ChatConversation;
