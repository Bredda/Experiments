export type Event = {
  id: string;
  timestamp: string;
  step: number;
  type: string;
  agent_id?: string;
  room_id?: string;
  content?: string;
  action?: {
    agent_id: string;
    room_id?: string;
    content?: string;
    urgency?: number;
    relevance?: number;
    social_cost?: number;
  };
};

export type Run = {
  run_id: string;
  scenario: {
    name: string;
    seed: number;
    agents: { id: string; behavior: string }[];
    room: {
      id: string;
      members: string[];
    };
    scheduler: { type: string };
    steps: number;
  };
};
