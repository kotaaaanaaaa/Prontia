export class Question {
  id: string;
  content: string;
  constructor(content: string) {
    this.id = crypto.randomUUID();
    this.content = content;
  }
}
export class Response {
  id: string;
  content: string;
  constructor(content: string) {
    this.id = crypto.randomUUID();
    this.content = content;
  }
}

export type Message = Question | Response;
