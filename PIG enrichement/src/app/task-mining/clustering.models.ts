export type ClusteringRunStatus = 'pending' | 'running' | 'complete' | 'failed';

export interface ClusteringRun {
  id: string;
  name: string;
  status: ClusteringRunStatus;
  taskCount: number;
  subtaskCount: number;
  /** ISO date string for display */
  createdAt: string;
  objectEventLabel: string;
  dataRangeLabel: string;
}

export interface ClusteringConfig {
  name: string;
  goal: string;
  objectEventId: string;
  dataRangeId: string;
}

export interface PreviewTaskRow {
  taskName: string;
  subtasks: string[];
}

export interface ClusteringPreviewResult {
  taskCount: number;
  subtaskCount: number;
  rows: PreviewTaskRow[];
}
