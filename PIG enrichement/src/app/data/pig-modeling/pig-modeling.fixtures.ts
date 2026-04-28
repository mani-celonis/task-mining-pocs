export interface PigModelAttribute {
  name: string;
  dataType: string;
  primaryKey?: boolean;
  required?: boolean;
  fillDescription?: string;
}

export interface PigModelObject {
  id: string;
  name: string;
  namespace: string;
  tags: string[];
  customProcessLabel: string;
  attributes: PigModelAttribute[];
  description: string;
}

export interface PigModelWorkerObjectLink {
  objectId: string;
  label: string;
}

export interface PigModelWorker {
  id: string;
  actor_id: string;
  actor_type: 'HUMAN' | 'AGENT';
  primaryRole: string;
  namespace: string;
  tags: string[];
  taskMining: boolean;
  agentMining: boolean;
  relatedObjects: PigModelWorkerObjectLink[];
  description: string;
  attributes: PigModelAttribute[];
}

export type PigEventCategory = 'Task' | 'Subtask' | 'SoR';

export interface PigModelEventAgentSignal {
  name: string;
}

export interface PigModelEventHigherTaskRef {
  id: string;
  label: string;
}

export interface PigModelEventClickstreamRef {
  id: string;
  label: string;
  application: string;
}

export interface PigModelEventClickstreamExample {
  title: string;
  userAction: string;
  applicationContext: string;
}

export interface PigModelEventMetadata {
  hierarchy: {
    clustered_task: PigModelEventHigherTaskRef;
    subtask: PigModelEventHigherTaskRef;
    related_object: PigModelEventHigherTaskRef;
    related_clickstream_event: PigModelEventClickstreamRef;
    granular_events_operated: number;
  };
  reference_process: string;
  context: string;
  description: string;
  clickstream_examples?: PigModelEventClickstreamExample[];
}

export interface PigModelEvent {
  id: string;
  label: string;
  category: PigEventCategory;
  objectLabel: string | null;
  workerId: string | null;
  workerLabel: string | null;
  timestamp: string;
  source: string;
  linkage: 'object_and_worker' | 'worker_only' | 'object_only';
  attributes: PigModelAttribute[];
  agentSignals?: PigModelEventAgentSignal[];
  metadata?: PigModelEventMetadata;
}

function agentSignalFieldNames(...fieldNames: string[]): PigModelEventAgentSignal[] {
  return fieldNames.map((name) => ({ name }));
}

function workerCanonicalEventAttributes(): PigModelAttribute[] {
  return [
    { name: 'Id', dataType: 'String', primaryKey: true, required: true },
    { name: 'CaseId', dataType: 'String', required: true },
    { name: 'ActorId', dataType: 'String', required: true },
    { name: 'RoleType', dataType: 'String' },
    { name: 'SessionId', dataType: 'String' },
    { name: 'ActivityName', dataType: 'String' },
    { name: 'WorkChannel', dataType: 'String' },
  ];
}

/** OTel GenAI semantic conventions (gen_ai.*) for agent-mining events. */
function agentMiningEventAttributes(): PigModelAttribute[] {
  return [
    { name: 'trace_id', dataType: 'String', primaryKey: true, required: true },
    { name: 'span_id', dataType: 'String', required: true },
    { name: 'gen_ai.operation.name', dataType: 'String', required: true },
    { name: 'gen_ai.system', dataType: 'String' },
    { name: 'gen_ai.agent.name', dataType: 'String' },
    { name: 'session.id', dataType: 'String' },
  ];
}

function financeManagerAttributes(): PigModelAttribute[] {
  return [
    { name: 'EmployeeId', dataType: 'String', primaryKey: true },
    { name: 'RoleDescription', dataType: 'String' },
    { name: 'Department', dataType: 'String' },
    { name: 'ApprovalLimit', dataType: 'Currency' },
  ];
}

function apInvoiceClerkAttributes(): PigModelAttribute[] {
  return [
    { name: 'EmployeeId', dataType: 'String', primaryKey: true },
    { name: 'RoleDescription', dataType: 'String' },
    { name: 'LanguageSkills', dataType: 'String' },
    { name: 'VendorPortfolioSize', dataType: 'Integer' },
  ];
}

function invoiceReconciliationAgentAttributes(): PigModelAttribute[] {
  return [
    { name: 'AgentId', dataType: 'String', primaryKey: true },
    { name: 'RoleDescription', dataType: 'String' },
    { name: 'OwnerTeam', dataType: 'String' },
    { name: 'PrimaryObjective', dataType: 'String' },
  ];
}

function threeWayMatchAgentAttributes(): PigModelAttribute[] {
  return [
    { name: 'AgentId', dataType: 'String', primaryKey: true },
    { name: 'RoleDescription', dataType: 'String' },
    { name: 'MatchingToleranceProfile', dataType: 'String' },
    { name: 'ConnectedSystems', dataType: 'String' },
  ];
}

function paymentReleaseAgentAttributes(): PigModelAttribute[] {
  return [
    { name: 'AgentId', dataType: 'String', primaryKey: true },
    { name: 'RoleDescription', dataType: 'String' },
    { name: 'PolicyVersion', dataType: 'String' },
    { name: 'RuntimeEnvironment', dataType: 'String' },
  ];
}

function apTaskMiningMetadata(
  partial: Omit<PigModelEventMetadata, 'hierarchy'> & {
    clusteredTask: PigModelEventHigherTaskRef;
    subtask: PigModelEventHigherTaskRef;
    relatedObject: PigModelEventHigherTaskRef;
    relatedClickstreamEvent: PigModelEventClickstreamRef;
    granularEventsOperated: number;
  },
): PigModelEventMetadata {
  return {
    hierarchy: {
      clustered_task: partial.clusteredTask,
      subtask: partial.subtask,
      related_object: partial.relatedObject,
      related_clickstream_event: partial.relatedClickstreamEvent,
      granular_events_operated: partial.granularEventsOperated,
    },
    reference_process: partial.reference_process,
    context: partial.context,
    description: partial.description,
    ...(partial.clickstream_examples && { clickstream_examples: partial.clickstream_examples }),
  };
}

export const PIG_MODEL_OBJECTS: PigModelObject[] = [
  {
    id: 'invoice',
    name: 'Invoice',
    namespace: 'accounts_payable',
    tags: ['ocpm', 'accounts_payable'],
    customProcessLabel: 'Accounts payable',
    description: 'AP invoice object correlated to worker actions and system postings.',
    attributes: [
      { name: 'InvoiceId', dataType: 'String', primaryKey: true },
      { name: 'VendorId', dataType: 'String' },
      { name: 'Amount', dataType: 'Decimal' },
      { name: 'DueDate', dataType: 'Date' },
    ],
  },
  {
    id: 'vendor',
    name: 'Vendor',
    namespace: 'accounts_payable',
    tags: ['master_data', 'accounts_payable'],
    customProcessLabel: 'Accounts payable',
    description: 'Vendor account with payment terms and tax identifiers used in AP validation.',
    attributes: [
      { name: 'VendorId', dataType: 'String', primaryKey: true },
      { name: 'VendorName', dataType: 'String' },
      { name: 'PaymentTerms', dataType: 'String' },
      { name: 'VatId', dataType: 'String' },
    ],
  },
  {
    id: 'purchase_order',
    name: 'Purchase Order',
    namespace: 'accounts_payable',
    tags: ['procurement', 'accounts_payable'],
    customProcessLabel: 'Accounts payable',
    description: 'PO reference used for three-way matching in invoice verification.',
    attributes: [
      { name: 'PurchaseOrderId', dataType: 'String', primaryKey: true },
      { name: 'SupplierId', dataType: 'String' },
      { name: 'Plant', dataType: 'String' },
      { name: 'OrderAmount', dataType: 'Decimal' },
    ],
  },
  {
    id: 'goods_receipt',
    name: 'Goods Receipt',
    namespace: 'accounts_payable',
    tags: ['logistics', 'accounts_payable'],
    customProcessLabel: 'Accounts payable',
    description: 'Goods receipt records that complete the PO-GR-Invoice match triangle.',
    attributes: [
      { name: 'GoodsReceiptId', dataType: 'String', primaryKey: true },
      { name: 'PurchaseOrderId', dataType: 'String' },
      { name: 'PostingDate', dataType: 'Date' },
      { name: 'Quantity', dataType: 'Decimal' },
    ],
  },
  {
    id: 'payment',
    name: 'Payment',
    namespace: 'accounts_payable',
    tags: ['treasury', 'accounts_payable'],
    customProcessLabel: 'Accounts payable',
    description: 'Outgoing payment document generated after invoice block release.',
    attributes: [
      { name: 'PaymentId', dataType: 'String', primaryKey: true },
      { name: 'InvoiceId', dataType: 'String' },
      { name: 'Amount', dataType: 'Decimal' },
      { name: 'PaymentDate', dataType: 'Date' },
    ],
  },
  {
    id: 'ap_case',
    name: 'AP Case',
    namespace: 'accounts_payable',
    tags: ['task_mining', 'accounts_payable'],
    customProcessLabel: 'Accounts payable',
    description: 'Task-mining work case that groups AP subtasks across systems.',
    attributes: [
      { name: 'CaseId', dataType: 'String', primaryKey: true },
      { name: 'InvoiceId', dataType: 'String' },
      { name: 'Priority', dataType: 'String' },
      { name: 'OwnerRole', dataType: 'String' },
    ],
  },
];

export type PigWorkerCollaborationKind =
  | 'agent_assists_human'
  | 'human_reviews_agent'
  | 'sequential_handoff'
  | 'shared_workspace';

export interface PigModelWorkerCollaborationEdge {
  id: string;
  fromWorkerId: string;
  toWorkerId: string;
  kind: PigWorkerCollaborationKind;
  label: string;
  processLabels: string[];
}

export const PIG_MODEL_WORKERS: PigModelWorker[] = [
  {
    id: 'worker_human_finance',
    actor_id: 'human_finance_manager',
    actor_type: 'HUMAN',
    primaryRole: 'Finance Manager',
    namespace: 'custom',
    tags: ['Accounts payable'],
    taskMining: false,
    agentMining: false,
    relatedObjects: [
      { objectId: 'invoice', label: 'Invoice' },
      { objectId: 'payment', label: 'Payment' },
      { objectId: 'ap_case', label: 'AP Case' },
    ],
    description: 'Approves high-risk invoice variances and final payment release decisions.',
    attributes: financeManagerAttributes(),
  },
  {
    id: 'worker_human_ap_clerk',
    actor_id: 'human_ap_invoice_clerk',
    actor_type: 'HUMAN',
    primaryRole: 'AP Invoice Clerk',
    namespace: 'custom',
    tags: ['Accounts payable', 'Vendor inbox'],
    taskMining: true,
    agentMining: false,
    relatedObjects: [
      { objectId: 'invoice', label: 'Invoice' },
      { objectId: 'vendor', label: 'Vendor' },
      { objectId: 'purchase_order', label: 'Purchase Order' },
      { objectId: 'goods_receipt', label: 'Goods Receipt' },
    ],
    description: 'Runs daily AP execution from vendor inbox triage through MIRO posting.',
    attributes: apInvoiceClerkAttributes(),
  },
  {
    id: 'worker_agent_invoice',
    actor_id: 'agent_invoice_reconciliation',
    actor_type: 'AGENT',
    primaryRole: 'Invoice Reconciliation Agent',
    namespace: 'DuplicateInvoiceChecker',
    tags: ['Accounts payable', 'Automation'],
    taskMining: false,
    agentMining: true,
    relatedObjects: [
      { objectId: 'invoice', label: 'Invoice' },
      { objectId: 'vendor', label: 'Vendor' },
      { objectId: 'ap_case', label: 'AP Case' },
    ],
    description: 'Proposes reconciliation actions and drafts explanations for invoice variances.',
    attributes: invoiceReconciliationAgentAttributes(),
  },
  {
    id: 'worker_agent_three_way',
    actor_id: 'agent_three_way_match',
    actor_type: 'AGENT',
    primaryRole: 'Three-way Match Agent',
    namespace: 'MatchAgent',
    tags: ['Accounts payable', 'GR/IR'],
    taskMining: false,
    agentMining: true,
    relatedObjects: [
      { objectId: 'invoice', label: 'Invoice' },
      { objectId: 'purchase_order', label: 'Purchase Order' },
      { objectId: 'goods_receipt', label: 'Goods Receipt' },
    ],
    description: 'Continuously checks PO, GR, and invoice consistency and escalates anomalies.',
    attributes: threeWayMatchAgentAttributes(),
  },
  {
    id: 'worker_agent_payment_release',
    actor_id: 'agent_payment_block_clearer',
    actor_type: 'AGENT',
    primaryRole: 'Payment Block & Dunning Agent',
    namespace: 'TreasuryAssist',
    tags: ['Accounts payable', 'Payment run'],
    taskMining: false,
    agentMining: true,
    relatedObjects: [
      { objectId: 'payment', label: 'Payment' },
      { objectId: 'invoice', label: 'Invoice' },
      { objectId: 'ap_case', label: 'AP Case' },
    ],
    description: 'Clears eligible blocks, prepares payment proposals, and drafts dunning content.',
    attributes: paymentReleaseAgentAttributes(),
  },
];

export const PIG_MODEL_WORKER_COLLABORATION_EDGES: PigModelWorkerCollaborationEdge[] = [
  {
    id: 'collab-ap-human-reviews-invoice-agent',
    fromWorkerId: 'worker_human_finance',
    toWorkerId: 'worker_agent_invoice',
    kind: 'human_reviews_agent',
    label: 'Policy and posting validation',
    processLabels: ['Accounts payable'],
  },
  {
    id: 'collab-ap-invoice-agent-handoff-finance',
    fromWorkerId: 'worker_agent_invoice',
    toWorkerId: 'worker_human_finance',
    kind: 'sequential_handoff',
    label: 'Variance package routed for approval',
    processLabels: ['Accounts payable'],
  },
  {
    id: 'collab-ap-3wm-assists-clerk',
    fromWorkerId: 'worker_agent_three_way',
    toWorkerId: 'worker_human_ap_clerk',
    kind: 'agent_assists_human',
    label: 'Suggested PO/GR matching groups',
    processLabels: ['Accounts payable'],
  },
  {
    id: 'collab-ap-clerk-reviews-payment-agent',
    fromWorkerId: 'worker_human_ap_clerk',
    toWorkerId: 'worker_agent_payment_release',
    kind: 'human_reviews_agent',
    label: 'Confirm invoice readiness before payment run',
    processLabels: ['Accounts payable'],
  },
  {
    id: 'collab-ap-payment-agent-finance',
    fromWorkerId: 'worker_agent_payment_release',
    toWorkerId: 'worker_human_finance',
    kind: 'sequential_handoff',
    label: 'Payment proposal ready for treasury sign-off',
    processLabels: ['Accounts payable'],
  },
];

const PIG_MODEL_EVENTS_RAW: Omit<PigModelEvent, 'attributes'>[] = [
  {
    id: 'ev-ap-1',
    label: 'Triage Invoice · AP Shared Inbox',
    category: 'Subtask',
    objectLabel: 'Vendor · VEND-1140',
    workerId: 'worker_human_ap_clerk',
    workerLabel: 'AP Invoice Clerk',
    timestamp: '2026-04-12T07:40:00Z',
    source: 'clustering',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: { id: 'tm-ap-inbox-triage', label: 'Process vendor inbox – morning batch' },
      subtask: { id: 'st-ap-triage-invoice', label: 'Triage Invoice · AP Shared Inbox' },
      relatedObject: { id: 'vendor', label: 'Vendor' },
      relatedClickstreamEvent: {
        id: 'cs-outlook-inbox-triage',
        label: 'Outlook inbox vendor email open',
        application: 'Microsoft Outlook',
      },
      granularEventsOperated: 18,
      reference_process: 'Accounts payable',
      context: 'ap-invoices@celonis.com · morning batch · ACME Industrial',
      description:
        'Clerk opens the AP shared mailbox, filters unread vendor emails, identifies pending invoice PDFs, and queues them for verification.',
      clickstream_examples: [
        {
          title: 'Filter inbox by unread sender: ACME Industrial',
          userAction: 'Click',
          applicationContext: 'Microsoft Outlook · AP shared inbox · filter bar',
        },
        {
          title: 'Open vendor email with subject "Invoice INV-9022 attached"',
          userAction: 'Click',
          applicationContext: 'Microsoft Outlook · inbox message list row',
        },
        {
          title: 'Scroll email body to locate invoice reference number',
          userAction: 'Scroll',
          applicationContext: 'Microsoft Outlook · email reading pane',
        },
        {
          title: 'Download attached PDF invoice to AP processing folder',
          userAction: 'Click',
          applicationContext: 'Microsoft Outlook · attachment inline preview bar',
        },
        {
          title: 'Right-click email to flag as "Processing"',
          userAction: 'Right-click',
          applicationContext: 'Microsoft Outlook · inbox message context menu',
        },
        {
          title: 'Copy invoice reference INV-9022 from email subject line',
          userAction: 'Double-click + Copy',
          applicationContext: 'Microsoft Outlook · email subject field',
        },
      ],
    }),
  },
  {
    id: 'ev-ap-2',
    label: 'Verify Invoice against Purchase Order · SAP MIRO',
    category: 'Subtask',
    objectLabel: 'Invoice · INV-9022',
    workerId: 'worker_human_ap_clerk',
    workerLabel: 'AP Invoice Clerk',
    timestamp: '2026-04-12T08:01:00Z',
    source: 'celonis_desktop',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: { id: 'tm-ap-miro-verification', label: 'Invoice verification in SAP MIRO' },
      subtask: { id: 'st-ap-verify-po-miro', label: 'Verify Invoice against Purchase Order · SAP MIRO' },
      relatedObject: { id: 'invoice', label: 'Invoice' },
      relatedClickstreamEvent: {
        id: 'cs-sap-miro-line-review',
        label: 'SAP MIRO item overview line review',
        application: 'SAP MIRO',
      },
      granularEventsOperated: 14,
      reference_process: 'Accounts payable',
      context: 'INV-9022 · PO-7781 · ACME Industrial · quantity discrepancy flag',
      description:
        'Clerk opens MIRO, enters the PO reference, and reviews each invoice line against the PO amount and goods receipt quantity before deciding to post or park.',
      clickstream_examples: [
        {
          title: 'Enter purchase order number PO-7781 in MIRO reference field',
          userAction: 'Type',
          applicationContext: 'SAP MIRO · Enter Invoice · header PO reference field',
        },
        {
          title: 'Select invoice date from document date calendar picker',
          userAction: 'Click',
          applicationContext: 'SAP MIRO · Enter Invoice · document date field',
        },
        {
          title: 'Review PO line item amounts in item overview tab',
          userAction: 'Click',
          applicationContext: 'SAP MIRO · Enter Invoice · item overview tab',
        },
        {
          title: 'Expand GR/IR balance line to check quantity mismatch indicator',
          userAction: 'Click',
          applicationContext: 'SAP MIRO · Enter Invoice · GR/IR balance detail row',
        },
        {
          title: 'Open tax line detail to verify VAT code assignment',
          userAction: 'Click',
          applicationContext: 'SAP MIRO · Enter Invoice · tax line details panel',
        },
        {
          title: 'Run simulate posting to compare header amount against PO net value',
          userAction: 'Click',
          applicationContext: 'SAP MIRO · Enter Invoice · simulate posting toolbar button',
        },
      ],
    }),
  },
  {
    id: 'ev-ap-3',
    label: 'agent.toolCall · fetch_goods_receipts',
    category: 'Subtask',
    objectLabel: 'Goods Receipt · GR-55089',
    workerId: 'worker_agent_three_way',
    workerLabel: 'Three-way Match Agent',
    timestamp: '2026-04-12T07:53:10Z',
    source: 'custom_agent',
    linkage: 'object_and_worker',
    agentSignals: agentSignalFieldNames('gen_ai.operation.name', 'gen_ai.tool.name', 'gen_ai.tool.call.id', 'gen_ai.system'),
  },
  {
    id: 'ev-ap-4',
    label: 'agent.completion · match decision draft',
    category: 'Subtask',
    objectLabel: 'Purchase Order · PO-7781',
    workerId: 'worker_agent_three_way',
    workerLabel: 'Three-way Match Agent',
    timestamp: '2026-04-12T07:53:48Z',
    source: 'custom_agent',
    linkage: 'object_and_worker',
    agentSignals: agentSignalFieldNames('gen_ai.operation.name', 'gen_ai.response.model', 'gen_ai.usage.output_tokens', 'gen_ai.response.finish_reasons'),
  },
  {
    id: 'ev-ap-5',
    label: 'Review variance package from agent queue',
    category: 'Subtask',
    objectLabel: 'AP Case · CASE-20041',
    workerId: 'worker_human_finance',
    workerLabel: 'Finance Manager',
    timestamp: '2026-04-12T08:10:00Z',
    source: 'celonis_desktop',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: { id: 'tm-ap-variance-approval', label: 'Approve variance package' },
      subtask: { id: 'st-ap-review-agent-package', label: 'Review variance package from agent queue' },
      relatedObject: { id: 'ap_case', label: 'AP Case' },
      relatedClickstreamEvent: {
        id: 'cs-celonis-queue-open',
        label: 'Celonis queue row open',
        application: 'Celonis',
      },
      granularEventsOperated: 9,
      reference_process: 'Accounts payable',
      context: 'CASE-20041 · high amount threshold',
      description: 'Task-mining event linked to finance manager approval flow.',
      clickstream_examples: [
        {
          title: 'Open variance package row',
          userAction: 'Double-click',
          applicationContext: 'Celonis · Agent queue table',
        },
        {
          title: 'Copy case reference',
          userAction: 'Copy',
          applicationContext: 'Celonis · case details panel',
        },
      ],
    }),
  },
  {
    id: 'ev-ap-6',
    label: 'Coordinate invoice unblock decision in Teams channel',
    category: 'Subtask',
    objectLabel: 'Invoice · INV-9022',
    workerId: 'worker_human_finance',
    workerLabel: 'Finance Manager',
    timestamp: '2026-04-12T08:22:00Z',
    source: 'celonis_desktop',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: {
        id: 'tm-ap-unblock-collaboration',
        label: 'Collaborate on invoice unblock decision',
      },
      subtask: {
        id: 'st-ap-teams-unblock',
        label: 'Coordinate invoice unblock decision in Teams channel',
      },
      relatedObject: { id: 'invoice', label: 'Invoice' },
      relatedClickstreamEvent: {
        id: 'cs-teams-unblock-thread',
        label: 'Teams unblock thread update',
        application: 'Microsoft Teams',
      },
      granularEventsOperated: 10,
      reference_process: 'Accounts payable',
      context: 'INV-9022 · AP escalation channel',
      description: 'Task-mining sequence for cross-tool collaboration before release in source systems.',
      clickstream_examples: [
        {
          title: 'Open AP escalation thread for invoice',
          userAction: 'Click',
          applicationContext: 'Microsoft Teams · AP escalation channel',
        },
        {
          title: 'Tag approver and request unblock decision',
          userAction: 'Type + Mention',
          applicationContext: 'Microsoft Teams · message composer',
        },
        {
          title: 'Attach updated variance sheet',
          userAction: 'Upload',
          applicationContext: 'Microsoft Teams · file attachment',
        },
      ],
    }),
  },
  {
    id: 'ev-ap-7',
    label: 'agent.invoke · explain invoice variance',
    category: 'Task',
    objectLabel: 'Invoice · INV-9022',
    workerId: 'worker_agent_invoice',
    workerLabel: 'Invoice Reconciliation Agent',
    timestamp: '2026-04-12T08:23:00Z',
    source: 'custom_agent',
    linkage: 'object_and_worker',
    agentSignals: agentSignalFieldNames('gen_ai.operation.name', 'gen_ai.system', 'gen_ai.request.model', 'gen_ai.usage.input_tokens'),
  },
  {
    id: 'ev-ap-8',
    label: 'agent.completion · draft vendor follow-up',
    category: 'Subtask',
    objectLabel: 'Vendor · VEND-1140',
    workerId: 'worker_agent_invoice',
    workerLabel: 'Invoice Reconciliation Agent',
    timestamp: '2026-04-12T08:24:00Z',
    source: 'custom_agent',
    linkage: 'object_and_worker',
    agentSignals: agentSignalFieldNames('gen_ai.operation.name', 'gen_ai.usage.output_tokens', 'gen_ai.response.finish_reasons', 'trace_id'),
  },
  {
    id: 'ev-ap-9',
    label: 'agent.invoke · clear payment block',
    category: 'Task',
    objectLabel: 'Payment · PAY-44102',
    workerId: 'worker_agent_payment_release',
    workerLabel: 'Payment Block & Dunning Agent',
    timestamp: '2026-04-12T09:05:00Z',
    source: 'custom_agent',
    linkage: 'object_and_worker',
    agentSignals: agentSignalFieldNames('gen_ai.operation.name', 'gen_ai.system', 'gen_ai.request.model'),
  },
  {
    id: 'ev-ap-10',
    label: 'agent.completion · draft dunning notice',
    category: 'Subtask',
    objectLabel: 'AP Case · CASE-20041',
    workerId: 'worker_agent_payment_release',
    workerLabel: 'Payment Block & Dunning Agent',
    timestamp: '2026-04-12T09:06:12Z',
    source: 'custom_agent',
    linkage: 'object_and_worker',
    agentSignals: agentSignalFieldNames('gen_ai.operation.name', 'gen_ai.response.model', 'gen_ai.usage.output_tokens'),
  },
  {
    id: 'ev-ap-18',
    label: 'Clarify Invoice Discrepancy · Vendor Email',
    category: 'Subtask',
    objectLabel: 'Invoice · INV-9022',
    workerId: 'worker_human_ap_clerk',
    workerLabel: 'AP Invoice Clerk',
    timestamp: '2026-04-12T08:40:00Z',
    source: 'clustering',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: { id: 'tm-ap-vendor-clarify', label: 'Clarify invoice discrepancy with vendor' },
      subtask: { id: 'st-ap-clarify-email', label: 'Clarify Invoice Discrepancy · Vendor Email' },
      relatedObject: { id: 'invoice', label: 'Invoice' },
      relatedClickstreamEvent: {
        id: 'cs-outlook-vendor-reply',
        label: 'Outlook vendor email reply compose',
        application: 'Microsoft Outlook',
      },
      granularEventsOperated: 7,
      reference_process: 'Accounts payable',
      context: 'INV-9022 · ACME Industrial · price vs. PO unit rate mismatch',
      description:
        'Clerk replies to the vendor email thread requesting a corrected invoice or credit note, attaching the MIRO quantity comparison as evidence.',
      clickstream_examples: [
        {
          title: 'Open vendor contact card for ACME Industrial in people pane',
          userAction: 'Click',
          applicationContext: 'Microsoft Outlook · people pane · contact card',
        },
        {
          title: 'Click Reply on previous invoice email thread with vendor',
          userAction: 'Click',
          applicationContext: 'Microsoft Outlook · email reading pane · reply button',
        },
        {
          title: 'Type invoice reference and discrepancy amount in email body',
          userAction: 'Type',
          applicationContext: 'Microsoft Outlook · new email compose · message body',
        },
        {
          title: 'Paste MIRO quantity comparison screenshot inline into email body',
          userAction: 'Ctrl+V',
          applicationContext: 'Microsoft Outlook · new email compose · inline image paste',
        },
        {
          title: 'Add accounting@acmeindustrial.com to CC field for finance copy',
          userAction: 'Type',
          applicationContext: 'Microsoft Outlook · new email compose · CC address field',
        },
        {
          title: 'Click Send to dispatch clarification request to vendor',
          userAction: 'Click',
          applicationContext: 'Microsoft Outlook · new email compose · send button',
        },
      ],
    }),
  },
  {
    id: 'ev-ap-19',
    label: 'Park Invoice Document · SAP FB60',
    category: 'Subtask',
    objectLabel: 'Invoice · INV-9022',
    workerId: 'worker_human_ap_clerk',
    workerLabel: 'AP Invoice Clerk',
    timestamp: '2026-04-12T09:00:00Z',
    source: 'celonis_desktop',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: { id: 'tm-ap-park-invoice', label: 'Park invoice pending vendor response' },
      subtask: { id: 'st-ap-park-fb60', label: 'Park Invoice Document · SAP FB60' },
      relatedObject: { id: 'invoice', label: 'Invoice' },
      relatedClickstreamEvent: {
        id: 'cs-sap-fb60-park',
        label: 'SAP FB60 park document action',
        application: 'SAP GUI',
      },
      granularEventsOperated: 12,
      reference_process: 'Accounts payable',
      context: 'INV-9022 · FB60 · vendor ACME Industrial · parked pending clarification',
      description:
        'Clerk parks the invoice document in SAP FB60, holding it out of the payment run until the vendor responds with a corrected invoice or credit note.',
      clickstream_examples: [
        {
          title: 'Enter vendor account number V001140 in FB60 vendor search field',
          userAction: 'Type',
          applicationContext: 'SAP GUI · FB60 · vendor account input field',
        },
        {
          title: 'Click document date field and enter invoice date from PDF header',
          userAction: 'Click + Type',
          applicationContext: 'SAP GUI · FB60 · document date entry field',
        },
        {
          title: 'Type reference document number INV-9022 in external reference field',
          userAction: 'Type',
          applicationContext: 'SAP GUI · FB60 · document reference text field',
        },
        {
          title: 'Enter net invoice amount 14 820.00 EUR in header amount field',
          userAction: 'Type',
          applicationContext: 'SAP GUI · FB60 · invoice amount and currency fields',
        },
        {
          title: 'Assign expense GL account 476000 and cost center CC-AP01 to line item',
          userAction: 'Click',
          applicationContext: 'SAP GUI · FB60 · G/L account assignment row',
        },
        {
          title: 'Click Park toolbar button to save as parked document awaiting approval',
          userAction: 'Click',
          applicationContext: 'SAP GUI · FB60 · park document toolbar button',
        },
      ],
    }),
  },
  {
    id: 'ev-ap-20',
    label: 'Escalate Invoice Block · AP Teams Channel',
    category: 'Subtask',
    objectLabel: 'Invoice · INV-9022',
    workerId: 'worker_human_ap_clerk',
    workerLabel: 'AP Invoice Clerk',
    timestamp: '2026-04-12T09:25:00Z',
    source: 'clustering',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: { id: 'tm-ap-escalate-block', label: 'Escalate payment block to finance' },
      subtask: { id: 'st-ap-escalate-teams', label: 'Escalate Invoice Block · AP Teams Channel' },
      relatedObject: { id: 'invoice', label: 'Invoice' },
      relatedClickstreamEvent: {
        id: 'cs-teams-ap-escalation-post',
        label: 'Teams AP escalation channel message post',
        application: 'Microsoft Teams',
      },
      granularEventsOperated: 8,
      reference_process: 'Accounts payable',
      context: 'INV-9022 · Invoice Exceptions channel · @Finance Manager',
      description:
        'Clerk posts an escalation thread in the Invoice Exceptions Teams channel to alert the Finance Manager of the blocked invoice and attach the variance summary.',
      clickstream_examples: [
        {
          title: 'Navigate to AP Finance team from left sidebar',
          userAction: 'Click',
          applicationContext: 'Microsoft Teams · left sidebar · AP Finance team entry',
        },
        {
          title: 'Open Invoice Exceptions channel within AP Finance team',
          userAction: 'Click',
          applicationContext: 'Microsoft Teams · channel list · Invoice Exceptions channel',
        },
        {
          title: 'Click New Conversation to start escalation thread',
          userAction: 'Click',
          applicationContext: 'Microsoft Teams · channel view · new conversation button',
        },
        {
          title: 'Type block reason and invoice reference INV-9022 in message body',
          userAction: 'Type',
          applicationContext: 'Microsoft Teams · message composer · text input area',
        },
        {
          title: 'Type @mention to tag Finance Manager for approval attention',
          userAction: 'Type',
          applicationContext: 'Microsoft Teams · message composer · @mention autocomplete',
        },
        {
          title: 'Attach variance summary Excel screenshot from local downloads',
          userAction: 'Click',
          applicationContext: 'Microsoft Teams · message composer · attach file button',
        },
        {
          title: 'Send escalation message to AP Invoice Exceptions channel',
          userAction: 'Click',
          applicationContext: 'Microsoft Teams · message composer · send button',
        },
      ],
    }),
  },
  {
    id: 'ev-ap-21',
    label: 'Update Invoice Status · AP Aging Report',
    category: 'Subtask',
    objectLabel: 'Invoice · INV-9022',
    workerId: 'worker_human_ap_clerk',
    workerLabel: 'AP Invoice Clerk',
    timestamp: '2026-04-12T10:05:00Z',
    source: 'celonis_desktop',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: { id: 'tm-ap-aging-update', label: 'Update AP aging report after parking' },
      subtask: { id: 'st-ap-status-aging', label: 'Update Invoice Status · AP Aging Report' },
      relatedObject: { id: 'invoice', label: 'Invoice' },
      relatedClickstreamEvent: {
        id: 'cs-excel-aging-status-update',
        label: 'Excel AP Aging status cell update',
        application: 'Microsoft Excel',
      },
      granularEventsOperated: 6,
      reference_process: 'Accounts payable',
      context: 'INV-9022 · AP Aging Report · Current Month sheet · status: Parked – Pending Approval',
      description:
        'After parking the invoice in SAP, clerk updates the AP Aging Report on SharePoint to reflect the new status and enter a forecast clearing date.',
      clickstream_examples: [
        {
          title: 'Open AP Aging Report workbook from SharePoint recent files',
          userAction: 'Click',
          applicationContext: 'Microsoft Excel · recent files list · AP Aging Report entry',
        },
        {
          title: 'Click Current Month sheet tab to navigate to active period',
          userAction: 'Click',
          applicationContext: 'Microsoft Excel · sheet tab bar · Current Month tab',
        },
        {
          title: 'Use Ctrl+F to search for invoice number INV-9022 in the sheet',
          userAction: 'Ctrl+F + Type',
          applicationContext: 'Microsoft Excel · Find & Replace · search input box',
        },
        {
          title: 'Click Status cell in invoice row highlighted by search result',
          userAction: 'Click',
          applicationContext: 'Microsoft Excel · AP Aging · Status column cell row 47',
        },
        {
          title: 'Select "Parked – Pending Approval" from in-cell status dropdown list',
          userAction: 'Click',
          applicationContext: 'Microsoft Excel · AP Aging · Status in-cell dropdown list',
        },
        {
          title: 'Enter expected clearing date 2026-04-25 in Forecast Date column',
          userAction: 'Click + Type',
          applicationContext: 'Microsoft Excel · AP Aging · Forecast Date column cell',
        },
      ],
    }),
  },
  {
    id: 'ev-ap-11',
    label: 'Post vendor payment',
    category: 'SoR',
    objectLabel: 'Payment · PAY-44102',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T09:15:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-12',
    label: 'Post goods receipt',
    category: 'SoR',
    objectLabel: 'Goods Receipt · GR-55089',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-11T16:45:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-13',
    label: 'Create vendor master record',
    category: 'SoR',
    objectLabel: 'Vendor · VEND-1140',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-11T08:05:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-14',
    label: 'Release purchase order for invoicing',
    category: 'SoR',
    objectLabel: 'Purchase Order · PO-7781',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-11T14:18:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-15',
    label: 'Post incoming invoice document',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T07:49:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-sor-01',
    label: 'Create invoice header record',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T07:45:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-sor-02',
    label: 'Set invoice payment block R – price variance',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T07:50:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-sor-03',
    label: 'Calculate tax amount · VAT input deduction',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T07:51:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-sor-04',
    label: 'Assign cost center and GL account',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T07:52:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-sor-05',
    label: 'GR/IR clearing account updated',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T07:55:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-sor-06',
    label: 'Invoice parked – pending approval',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T09:02:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-sor-07',
    label: 'Remove payment block after approval',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T10:45:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-sor-08',
    label: 'Invoice due date set · net 30',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-12T10:46:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-sor-09',
    label: 'Invoice cleared against payment run',
    category: 'SoR',
    objectLabel: 'Invoice · INV-9022',
    workerId: null,
    workerLabel: null,
    timestamp: '2026-04-14T11:00:00Z',
    source: 'sap_s4',
    linkage: 'object_only',
  },
  {
    id: 'ev-ap-16',
    label: 'Reconcile Invoice Variance · AP Tracker',
    category: 'Subtask',
    objectLabel: 'Invoice · INV-9022',
    workerId: 'worker_human_ap_clerk',
    workerLabel: 'AP Invoice Clerk',
    timestamp: '2026-04-12T08:22:00Z',
    source: 'celonis_desktop',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: { id: 'tm-ap-variance-reconcile', label: 'Reconcile invoice discrepancy batch' },
      subtask: { id: 'st-ap-reconcile-tracker', label: 'Reconcile Invoice Variance · AP Tracker' },
      relatedObject: { id: 'invoice', label: 'Invoice' },
      relatedClickstreamEvent: {
        id: 'cs-excel-tracker-variance-edit',
        label: 'Excel AP Tracker variance row edit',
        application: 'Microsoft Excel',
      },
      granularEventsOperated: 9,
      reference_process: 'Accounts payable',
      context: 'INV-9022 · AP Tracker · variance batch Apr 12',
      description:
        'Clerk opens the shared Excel AP Tracker on SharePoint, filters to variance rows, updates corrected amounts and reason codes for the invoice batch.',
      clickstream_examples: [
        {
          title: 'Apply AutoFilter on Invoice Status column to show "Variance" rows only',
          userAction: 'Click',
          applicationContext: 'Microsoft Excel · AP Tracker · Invoice Status AutoFilter dropdown',
        },
        {
          title: 'Scroll to invoice row INV-9022 in filtered result set',
          userAction: 'Scroll',
          applicationContext: 'Microsoft Excel · AP Tracker · invoice data table body',
        },
        {
          title: 'Double-click Variance Amount cell and type corrected supplier value',
          userAction: 'Double-click + Type',
          applicationContext: 'Microsoft Excel · AP Tracker · Variance Amount column cell',
        },
        {
          title: 'Click Reason Code dropdown and select "Price Discrepancy"',
          userAction: 'Click',
          applicationContext: 'Microsoft Excel · AP Tracker · Reason Code in-cell dropdown',
        },
        {
          title: 'Click Comments cell and type note referencing vendor email thread',
          userAction: 'Click + Type',
          applicationContext: 'Microsoft Excel · AP Tracker · Comments column cell',
        },
        {
          title: 'Click aged totals formula cell to recalculate SUM across variance rows',
          userAction: 'Click',
          applicationContext: 'Microsoft Excel · AP Tracker · aged totals summary row',
        },
        {
          title: 'Save workbook with Ctrl+S before closing variance tab',
          userAction: 'Ctrl+S',
          applicationContext: 'Microsoft Excel · AP Tracker · workbook title bar',
        },
      ],
    }),
  },
  {
    id: 'ev-ap-17',
    label: 'Attach invoice evidence note for finance approval',
    category: 'Subtask',
    objectLabel: 'Invoice · INV-9022',
    workerId: 'worker_human_finance',
    workerLabel: 'Finance Manager',
    timestamp: '2026-04-12T08:15:30Z',
    source: 'celonis_desktop',
    linkage: 'object_and_worker',
    metadata: apTaskMiningMetadata({
      clusteredTask: { id: 'tm-ap-variance-approval', label: 'Approve variance package' },
      subtask: { id: 'st-ap-attach-evidence-note', label: 'Attach invoice evidence note for approval' },
      relatedObject: { id: 'invoice', label: 'Invoice' },
      relatedClickstreamEvent: {
        id: 'cs-celonis-note-attachment',
        label: 'Celonis note and attachment update',
        application: 'Celonis',
      },
      granularEventsOperated: 8,
      reference_process: 'Accounts payable',
      context: 'INV-9022 · risk note for treasury review',
      description: 'Manual approval annotation step outside pure system-of-record posting.',
      clickstream_examples: [
        {
          title: 'Open approval note editor',
          userAction: 'Click',
          applicationContext: 'Celonis · case side panel',
        },
        {
          title: 'Copy variance summary from agent output',
          userAction: 'Copy + Paste',
          applicationContext: 'Agent queue -> Celonis note editor',
        },
      ],
    }),
  },
];

export const PIG_MODEL_EVENTS: PigModelEvent[] = PIG_MODEL_EVENTS_RAW.map((event) => ({
  ...event,
  attributes:
    event.source === 'custom_agent'
      ? agentMiningEventAttributes()
      : workerCanonicalEventAttributes(),
}));
