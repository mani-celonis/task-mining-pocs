import type {
  PigModelWorker,
  PigModelWorkerCollaborationEdge,
  PigWorkerCollaborationKind,
} from './pig-modeling.fixtures';

export interface WorkerCollaborationGraph {
  empty: boolean;
  processSummary: string;
  viewBox: string;
  viewHeight: number;
  laneBandX: { human: number; agent: number; bandW: number };
  nodes: {
    workerId: string;
    actorType: PigModelWorker['actor_type'];
    primaryRole: string;
    x: number;
    y: number;
  }[];
  edges: {
    id: string;
    kind: PigWorkerCollaborationKind;
    pathD: string;
    graphLabel: string;
    labelX: number;
    labelY: number;
    fromRole: string;
    toRole: string;
    label: string;
  }[];
}

const LANE_HUMAN_X = 34;
const LANE_AGENT_X = 516;
const LANE_BAND_W = 168;
const VIEW_W = 720;
const TOP_Y = 88;
const STEP_Y = 110;

function centerX(actorType: PigModelWorker['actor_type']): number {
  return actorType === 'HUMAN' ? LANE_HUMAN_X + LANE_BAND_W / 2 : LANE_AGENT_X + LANE_BAND_W / 2;
}

function edgePath(fromX: number, fromY: number, toX: number, toY: number): string {
  const dx = Math.abs(toX - fromX);
  const c = Math.max(80, Math.min(160, dx * 0.45));
  return `M ${fromX} ${fromY} C ${fromX + c} ${fromY}, ${toX - c} ${toY}, ${toX} ${toY}`;
}

export function collaborationKindLegend(): { kind: PigWorkerCollaborationKind; title: string }[] {
  return [
    { kind: 'agent_assists_human', title: 'Agent assists human' },
    { kind: 'human_reviews_agent', title: 'Human reviews agent' },
    { kind: 'sequential_handoff', title: 'Sequential handoff' },
    { kind: 'shared_workspace', title: 'Shared workspace' },
  ];
}

export function buildWorkerCollaborationGraph(
  workers: PigModelWorker[],
  edges: PigModelWorkerCollaborationEdge[],
  processFilter: 'all' | string,
): WorkerCollaborationGraph {
  const scopedEdges = edges.filter(
    (edge) => processFilter === 'all' || edge.processLabels.includes(processFilter),
  );
  const ids = new Set(scopedEdges.flatMap((edge) => [edge.fromWorkerId, edge.toWorkerId]));
  const graphWorkers = workers.filter((worker) => ids.has(worker.id));

  const humanWorkers = graphWorkers.filter((w) => w.actor_type === 'HUMAN');
  const agentWorkers = graphWorkers.filter((w) => w.actor_type === 'AGENT');

  const nodes = [
    ...humanWorkers.map((w, idx) => ({
      workerId: w.id,
      actorType: w.actor_type,
      primaryRole: w.primaryRole,
      x: centerX('HUMAN'),
      y: TOP_Y + idx * STEP_Y,
    })),
    ...agentWorkers.map((w, idx) => ({
      workerId: w.id,
      actorType: w.actor_type,
      primaryRole: w.primaryRole,
      x: centerX('AGENT'),
      y: TOP_Y + idx * STEP_Y,
    })),
  ];

  const nodeById = new Map(nodes.map((n) => [n.workerId, n] as const));
  const roleById = new Map(workers.map((w) => [w.id, w.primaryRole] as const));

  const graphEdges = scopedEdges
    .map((edge) => {
      const from = nodeById.get(edge.fromWorkerId);
      const to = nodeById.get(edge.toWorkerId);
      if (!from || !to) return null;
      return {
        id: edge.id,
        kind: edge.kind,
        pathD: edgePath(from.x, from.y, to.x, to.y),
        graphLabel: edge.label.length > 42 ? `${edge.label.slice(0, 39)}...` : edge.label,
        labelX: (from.x + to.x) / 2,
        labelY: (from.y + to.y) / 2 - 8,
        fromRole: roleById.get(edge.fromWorkerId) ?? edge.fromWorkerId,
        toRole: roleById.get(edge.toWorkerId) ?? edge.toWorkerId,
        label: edge.label,
      };
    })
    .filter((edge): edge is NonNullable<typeof edge> => edge !== null);

  const rowCount = Math.max(humanWorkers.length, agentWorkers.length, 1);
  const viewHeight = 66 + rowCount * STEP_Y;
  return {
    empty: graphEdges.length === 0,
    processSummary: processFilter === 'all' ? 'All processes' : processFilter,
    viewBox: `0 0 ${VIEW_W} ${viewHeight}`,
    viewHeight,
    laneBandX: { human: LANE_HUMAN_X, agent: LANE_AGENT_X, bandW: LANE_BAND_W },
    nodes,
    edges: graphEdges,
  };
}
