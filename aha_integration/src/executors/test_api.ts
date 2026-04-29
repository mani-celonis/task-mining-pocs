/**
 * Test script: fetches features from Aha! API and prints those assigned to Frederik Chettouh.
 */

import "dotenv/config";
import { AhaApiClient } from "../api/client.js";

const ASSIGNEE_MATCH = "Frederik Chettouh";

interface AssignedToUser {
  id?: string;
  name?: string;
  email?: string;
}

interface Feature {
  reference_num: string;
  name: string;
  assigned_to_user?: AssignedToUser | null;
}

interface FeaturesResponse {
  features: Feature[];
  pagination?: { total_pages: number; current_page: number };
}

async function main() {
  const apiKey = process.env.AHA_API_KEY;
  if (!apiKey) {
    console.error("Missing AHA_API_KEY in .env");
    process.exit(1);
  }

  const client = new AhaApiClient({ apiKey });
  const allFeatures: Feature[] = [];
  let page = 1;
  let totalPages = 1;

  do {
    const res = await client.get<FeaturesResponse>("/features", {
      fields: "name,reference_num,assigned_to_user",
      page: String(page),
      per_page: "100",
    });

    allFeatures.push(...(res.features ?? []));
    totalPages = res.pagination?.total_pages ?? 1;
    page++;
  } while (page <= totalPages);

  const matchesAssignee = (f: Feature): boolean => {
    const assignee = f.assigned_to_user;
    if (!assignee) return false;
    const name = typeof assignee === "string" ? assignee : assignee.name ?? "";
    const email = typeof assignee === "string" ? "" : assignee.email ?? "";
    return (
      name.toLowerCase().includes(ASSIGNEE_MATCH.toLowerCase()) ||
      email.toLowerCase().includes(ASSIGNEE_MATCH.toLowerCase())
    );
  };

  const assigned = allFeatures.filter(matchesAssignee);

  console.log("\n--- Features assigned to Frederik Chettouh ---\n");
  if (assigned.length === 0) {
    console.log("(none found)\n");
    return;
  }
  assigned.forEach((f) => {
    console.log(`  ${f.reference_num}  ${f.name}`);
  });
  console.log(`\nTotal: ${assigned.length} feature(s)\n`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
