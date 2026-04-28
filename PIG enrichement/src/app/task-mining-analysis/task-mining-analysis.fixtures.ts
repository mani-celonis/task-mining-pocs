export type AiPotentialLevel = 'high' | 'medium' | 'low';

export interface ProcessStep {
  id: string;
  label: string;
  ownerIds: string[];
}

export interface FinanceBusinessObject {
  id: string;
  label: string;
  steps: readonly ProcessStep[];
}

export interface PrioritizedActivityRow {
  id: string;
  activity: string;
  manualExecutionsLabel: string;
  automationRatePct: number;
  effortLabel: string;
  taskCount: number;
  subtaskCount: number;
  aiPotential: AiPotentialLevel;
  kpiImpact: string;
  businessImpactLabel: string;
}

export const PROCESS_HEADLINE_METRICS = [
  { name: 'Process variants', value: '58' },
  { name: 'Median throughput', value: '5.8 days' },
  { name: 'Manual touches / case', value: '14.2' },
  { name: 'Invoice block rate', value: '12.7%', variant: 'warning' as const },
];

export const TASK_DISCOVERY_STATS = [
  { name: 'Tasks discovered', value: '42' },
  { name: 'Subtasks discovered', value: '186' },
  { name: 'Coverage', value: '91%' },
  { name: 'Workers in scope', value: '5' },
];

export const AUTOMATION_SUMMARY_KPIS = [
  { name: 'High AI potential', value: '9' },
  { name: 'Automation-ready subtasks', value: '27' },
  { name: 'Estimated annual savings', value: '1.2M EUR', variant: 'success' as const },
  { name: 'Implementation waves', value: '3' },
];

export const TASK_DISCOVERY_ROWS = [
  { id: 'td-1', taskName: 'Triage vendor inbox', subtaskName: 'Open unread AP mail thread', count: 268, coveragePct: 100 },
  { id: 'td-2', taskName: 'Process invoice in MIRO', subtaskName: 'Enter quantity and amount corrections', count: 211, coveragePct: 79 },
  { id: 'td-3', taskName: 'Resolve three-way variance', subtaskName: 'Compare PO vs GR mismatch package', count: 143, coveragePct: 53 },
  { id: 'td-4', taskName: 'Release payment block', subtaskName: 'Approve MRBR release', count: 98, coveragePct: 37 },
];

export const PROCESS_WORKERS = [
  { id: 'all', label: 'All workers' },
  { id: 'worker_human_ap_clerk', label: 'AP Invoice Clerk' },
  { id: 'worker_human_finance', label: 'Finance Manager' },
  { id: 'worker_agent_three_way', label: 'Three-way Match Agent' },
  { id: 'worker_agent_invoice', label: 'Invoice Reconciliation Agent' },
  { id: 'worker_agent_payment_release', label: 'Payment Block & Dunning Agent' },
];

export const FINANCE_BUSINESS_OBJECTS: readonly FinanceBusinessObject[] = [
  {
    id: 'bo-invoice',
    label: 'Invoice',
    steps: [
      { id: 'inv-1', label: 'Register invoice and classify exceptions', ownerIds: ['worker_human_ap_clerk'] },
      { id: 'inv-2', label: 'Generate reconciliation suggestion', ownerIds: ['worker_agent_invoice'] },
      { id: 'inv-3', label: 'Approve high-value variance package', ownerIds: ['worker_human_finance'] },
    ],
  },
  {
    id: 'bo-po-gr',
    label: 'Purchase Order / Goods Receipt',
    steps: [
      { id: 'po-1', label: 'Fetch PO and GR references', ownerIds: ['worker_agent_three_way'] },
      { id: 'po-2', label: 'Review mismatch with supporting evidence', ownerIds: ['worker_human_ap_clerk', 'worker_human_finance'] },
    ],
  },
  {
    id: 'bo-payment',
    label: 'Payment',
    steps: [
      { id: 'pay-1', label: 'Clear eligible payment block', ownerIds: ['worker_agent_payment_release'] },
      { id: 'pay-2', label: 'Finalize treasury approval', ownerIds: ['worker_human_finance'] },
    ],
  },
];

export const PRIORITIZED_ACTIVITIES: readonly PrioritizedActivityRow[] = [
  {
    id: 'pa-1',
    activity: 'Three-way variance clarification',
    manualExecutionsLabel: '11,240',
    automationRatePct: 22,
    effortLabel: '8.2 min',
    taskCount: 7,
    subtaskCount: 31,
    aiPotential: 'high',
    kpiImpact: 'Block release lead time',
    businessImpactLabel: '420k EUR / year',
  },
  {
    id: 'pa-2',
    activity: 'Vendor inbox triage and enrichment',
    manualExecutionsLabel: '9,870',
    automationRatePct: 34,
    effortLabel: '5.1 min',
    taskCount: 5,
    subtaskCount: 24,
    aiPotential: 'high',
    kpiImpact: 'Invoice touchless ratio',
    businessImpactLabel: '310k EUR / year',
  },
  {
    id: 'pa-3',
    activity: 'Draft dunning communication',
    manualExecutionsLabel: '4,550',
    automationRatePct: 48,
    effortLabel: '3.8 min',
    taskCount: 4,
    subtaskCount: 14,
    aiPotential: 'medium',
    kpiImpact: 'Overdue receivables',
    businessImpactLabel: '160k EUR / year',
  },
  {
    id: 'pa-4',
    activity: 'Payment proposal quality check',
    manualExecutionsLabel: '2,940',
    automationRatePct: 57,
    effortLabel: '4.5 min',
    taskCount: 3,
    subtaskCount: 12,
    aiPotential: 'low',
    kpiImpact: 'Payment run stability',
    businessImpactLabel: '75k EUR / year',
  },
];
