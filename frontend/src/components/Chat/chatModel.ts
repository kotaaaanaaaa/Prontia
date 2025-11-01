export class Question {
  id: string;
  content: string;
  constructor(id: string, content: string) {
    this.id = id;
    this.content = content;
  }
}
export class Response {
  id: string;
  content: string;
  constructor(id: string, content: string) {
    this.id = id;
    this.content = content;
  }
}

export type Message = Question | Response;
