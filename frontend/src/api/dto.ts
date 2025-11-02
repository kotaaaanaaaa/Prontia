export type MessageResponse = {
  id: string;
  req_id: string;
  conversation_id: string;
  role: string;
  content: string;
};

export class ConversationResponse {
  id: string;
  title: string;
  constructor(id: string, title: string) {
    this.id = id;
    this.title = title;
  }
}
