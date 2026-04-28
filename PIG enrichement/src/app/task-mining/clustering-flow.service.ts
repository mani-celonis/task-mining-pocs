import { Injectable, computed, signal } from '@angular/core';

import type {
  ClusteringConfig,
  ClusteringPreviewResult,
  ClusteringRun,
  ClusteringRunStatus,
} from './clustering.models';

const OBJECT_OPTIONS = [
  { id: 'oe-order', label: 'Order item (O2C)' },
  { id: 'oe-delivery', label: 'Delivery / shipment event' },
  { id: 'oe-invoice', label: 'Invoice object' },
] as const;

const DATA_RANGE_OPTIONS = [
  { id: 'dr-30', label: 'Last 30 days' },
  { id: 'dr-90', label: 'Last 90 days' },
  { id: 'dr-ytd', label: 'Year to date' },
  { id: 'dr-all', label: 'Full project history' },
] as const;

function mockRuns(): ClusteringRun[] {
  const now = new Date();
  const iso = (d: Date) => d.toISOString();
  return [
    {
      id: 'run-1',
      name: 'Q1 touchless rework scan',
      status: 'complete',
      taskCount: 128,
      subtaskCount: 412,
      createdAt: iso(new Date(now.getTime() - 5 * 86400000)),
      objectEventLabel: OBJECT_OPTIONS[0].label,
      dataRangeLabel: DATA_RANGE_OPTIONS[1].label,
    },
    {
      id: 'run-2',
      name: 'Vendor invoice exceptions',
      status: 'running',
      taskCount: 0,
      subtaskCount: 0,
      createdAt: iso(new Date(now.getTime() - 3600000)),
      objectEventLabel: OBJECT_OPTIONS[2].label,
      dataRangeLabel: DATA_RANGE_OPTIONS[0].label,
    },
    {
      id: 'run-3',
      name: 'Pilot — logistics handoffs',
      status: 'failed',
      taskCount: 0,
      subtaskCount: 0,
      createdAt: iso(new Date(now.getTime() - 14 * 86400000)),
      objectEventLabel: OBJECT_OPTIONS[1].label,
      dataRangeLabel: DATA_RANGE_OPTIONS[2].label,
    },
  ];
}

function mockPreview(goal: string): ClusteringPreviewResult {
  const base = goal.trim().length > 0 ? goal.slice(0, 48) : 'Untitled goal';
  return {
    taskCount: 24,
    subtaskCount: 67,
    rows: [
      {
        taskName: `${base} — variant A`,
        subtasks: ['Capture event', 'Normalize attributes', 'Map to activity'],
      },
      {
        taskName: 'Exception handling cluster',
        subtasks: ['Manual review', 'Rework queue', 'Re-submit'],
      },
      {
        taskName: 'Straight-through processing',
        subtasks: ['Validate', 'Post'],
      },
    ],
  };
}

@Injectable({ providedIn: 'root' })
export class ClusteringFlowService {
  readonly projectName = signal('Order-to-Cash — Task Mining project');

  readonly objectOptions = OBJECT_OPTIONS;
  readonly dataRangeOptions = DATA_RANGE_OPTIONS;

  private readonly _runs = signal<ClusteringRun[]>(mockRuns());
  readonly runs = this._runs.asReadonly();

  private readonly _draft = signal<ClusteringConfig>({
    name: '',
    goal: '',
    objectEventId: OBJECT_OPTIONS[0].id,
    dataRangeId: DATA_RANGE_OPTIONS[1].id,
  });
  readonly draft = this._draft.asReadonly();

  private readonly _preview = signal<ClusteringPreviewResult | null>(null);
  readonly preview = this._preview.asReadonly();

  readonly hasPreview = computed(() => this._preview() !== null);

  labelForObject(id: string): string {
    return OBJECT_OPTIONS.find((o) => o.id === id)?.label ?? id;
  }

  labelForDataRange(id: string): string {
    return DATA_RANGE_OPTIONS.find((o) => o.id === id)?.label ?? id;
  }

  patchDraft(partial: Partial<ClusteringConfig>): void {
    this._draft.update((d) => ({ ...d, ...partial }));
  }

  resetDraftForNewRun(): void {
    this._draft.set({
      name: '',
      goal: '',
      objectEventId: OBJECT_OPTIONS[0].id,
      dataRangeId: DATA_RANGE_OPTIONS[1].id,
    });
    this._preview.set(null);
  }

  /** Sample preview after “Run AI task clustering” (subsample; fast). */
  generatePreviewSample(): void {
    const d = this._draft();
    this._preview.set(mockPreview(d.goal));
  }

  clearPreview(): void {
    this._preview.set(null);
  }

  confirmRunOnFullDataset(): void {
    const d = this._draft();
    const p = this._preview();
    const id = `run-${Date.now()}`;
    const run: ClusteringRun = {
      id,
      name: d.name.trim() || 'Untitled run',
      status: 'running' as ClusteringRunStatus,
      taskCount: p?.taskCount ?? 0,
      subtaskCount: p?.subtaskCount ?? 0,
      createdAt: new Date().toISOString(),
      objectEventLabel: this.labelForObject(d.objectEventId),
      dataRangeLabel: this.labelForDataRange(d.dataRangeId),
    };
    this._runs.update((list) => [run, ...list]);
    this._preview.set(null);
  }

  statusVariant(
    status: ClusteringRunStatus,
  ): 'queued' | 'process' | 'success' | 'error' {
    switch (status) {
      case 'pending':
        return 'queued';
      case 'running':
        return 'process';
      case 'complete':
        return 'success';
      case 'failed':
        return 'error';
    }
  }

  statusLabel(status: ClusteringRunStatus): string {
    switch (status) {
      case 'pending':
        return 'Pending';
      case 'running':
        return 'Running';
      case 'complete':
        return 'Complete';
      case 'failed':
        return 'Failed';
    }
  }
}
