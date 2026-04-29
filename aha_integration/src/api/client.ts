/**
 * Base Aha! REST API client.
 * Handles auth, headers, and rate limiting per .cursorrules.
 */

const BASE_URL = "https://celonis.aha.io/api/v1";
const USER_AGENT = "Celonis PM Automation (Agent)";

export interface AhaApiOptions {
  apiKey: string;
}

export class AhaApiClient {
  private apiKey: string;

  constructor(options: AhaApiOptions) {
    this.apiKey = options.apiKey;
  }

  async get<T>(path: string, params?: Record<string, string>): Promise<T> {
    const url = new URL(path, BASE_URL);
    if (params) {
      Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
    }

    const res = await fetch(url.toString(), {
      method: "GET",
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        Accept: "application/json",
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
      },
    });

    if (res.status === 429) {
      const retryAfter = res.headers.get("Retry-After");
      const delay = retryAfter ? parseInt(retryAfter, 10) * 1000 : 60000;
      await this.sleep(delay);
      return this.get<T>(path, params);
    }

    if (!res.ok) {
      const body = await res.text();
      throw new Error(`Aha! API error ${res.status}: ${body}`);
    }

    return res.json() as Promise<T>;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
