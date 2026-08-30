import { components } from "./api-types";

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

export type Run = components["schemas"]["Run"];
