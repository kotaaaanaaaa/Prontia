import type { MessageResponse } from "./dto";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function sendMessage(
  message: string,
  conversationId: string | undefined = undefined,
) {
  let res: Response;
  if (conversationId) {
    res = await fetch(
      `${API_BASE_URL}/conversations/${conversationId}/messages`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: message,
        }),
      },
    );
  } else {
    res = await fetch(`${API_BASE_URL}/conversations/message`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content: message,
      }),
    });
  }
  const result: MessageResponse = await res.json();
  return result;
}
