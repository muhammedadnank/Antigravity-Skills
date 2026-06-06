export type SessionFormat = "codex" | "claude" | "pi-openclaw" | "unknown";

export type SessionEventKind =
  | "event"
  | "memory"
  | "message"
  | "reasoning"
  | "system"
  | "tool_call"
  | "tool_result";

export type SessionImage = {
  src: string;
  alt?: string;
  detail?: string;
};

export type SessionEvent = {
  id: string;
  kind: SessionEventKind;
  role?: string;
  title: string;
  text: string;
  images?: SessionImage[];
  timestamp?: string;
  callId?: string;
  toolName?: string;
  status?: "ok" | "error" | "running" | "unknown";
  raw?: unknown;
};

export type SessionDocument = {
  format: SessionFormat;
  title: string;
  sourcePath?: string;
  meta: Record<string, string | number | boolean | null>;
  events: SessionEvent[];
  warnings: string[];
};

export type JsonlRecord = {
  line: number;
  value: unknown;
};

export type SessionImporter = {
  format: Exclude<SessionFormat, "unknown">;
  detect: (records: JsonlRecord[]) => boolean;
  parse: (records: JsonlRecord[], sourcePath?: string) => SessionDocument;
};
