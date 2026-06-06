import { claudeImporter } from "../importers/claude.ts";
import { codexImporter } from "../importers/codex.ts";
import { piOpenClawImporter } from "../importers/pi-openclaw.ts";
import type { JsonlRecord, SessionDocument, SessionImporter } from "./types.ts";

const importers: SessionImporter[] = [codexImporter, piOpenClawImporter, claudeImporter];

export function parseSessionDocument(records: JsonlRecord[], sourcePath?: string): SessionDocument {
  const importer = importers.find((candidate) => candidate.detect(records));
  if (!importer) {
    return {
      format: "unknown",
      title: sourcePath ? (sourcePath.split(/[\\/]/u).pop() ?? "session") : "session",
      sourcePath,
      meta: {},
      events: records.map((record) => ({
        id: `raw-${record.line}`,
        kind: "event",
        title: `raw line ${record.line}`,
        text: JSON.stringify(record.value, null, 2),
        raw: record.value,
      })),
      warnings: ["unknown session format; rendered raw JSONL rows"],
    };
  }
  return importer.parse(records, sourcePath);
}
