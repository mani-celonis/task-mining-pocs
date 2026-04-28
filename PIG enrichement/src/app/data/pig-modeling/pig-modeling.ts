import {
  afterNextRender,
  Component,
  computed,
  effect,
  ElementRef,
  inject,
  signal,
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router } from '@angular/router';
import {
  CeButtonModule,
  CeChipsModule,
  CeIconModule,
  CeIconRegistryService,
  CeInfoModule,
  CeInputGroupModule,
  CeMainContentModule,
  CePanelModule,
  CeStatusIndicatorModule,
} from '@celonis/emotion';
import { ceIconBotFilled, ceIconTapDoubleFilled } from '@celonis/icons';

import {
  PIG_MODEL_EVENTS,
  PIG_MODEL_OBJECTS,
  PIG_MODEL_WORKERS,
  type PigModelAttribute,
  type PigModelEvent,
  type PigModelObject,
  type PigModelWorker,
} from './pig-modeling.fixtures';

export type {
  PigEventCategory,
  PigModelAttribute,
  PigModelEvent,
  PigModelEventAgentSignal,
  PigModelEventClickstreamRef,
  PigModelEventHigherTaskRef,
  PigModelEventMetadata,
  PigModelObject,
  PigModelWorker,
  PigModelWorkerObjectLink,
} from './pig-modeling.fixtures';

export type PigDataNavId = 'objects' | 'workers' | 'events';

export type PigObjectInspectorTab = 'details' | 'related-workers' | 'related-events';
export type PigObjectEventSourceTab =
  | 'all'
  | 'source-system'
  | 'task-mining'
  | 'agent-mining';

export type PigWorkerInspectorTab = 'details' | 'related-objects' | 'related-events';

export type PigEventActorType = 'SYSTEM' | 'HUMAN' | 'AGENT';
export type PigEventInspectorTab = 'details' | 'related-object' | 'related-worker';
interface PigClickstreamRow {
  title: string;
  userAction: string;
  applicationContext: string;
}

@Component({
  selector: 'app-pig-modeling',
  imports: [
    CeMainContentModule,
  CeButtonModule,
  CePanelModule,
  CeInfoModule,
  CeInputGroupModule,
  CeStatusIndicatorModule,
  CeChipsModule,
  CeIconModule,
  ],
  templateUrl: './pig-modeling.html',
  styleUrl: './pig-modeling.scss',
})
export class PigModelingPage {
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  private readonly hostRef = inject(ElementRef<HTMLElement>);

  /** Default to Workers so PiG opens on the latest Workers prototype. Override with `?ocpm=objects|events`. */
  protected readonly activeNav = signal<PigDataNavId>('workers');

  constructor() {
    inject(CeIconRegistryService).registerIcons([ceIconTapDoubleFilled, ceIconBotFilled]);

    /** Deep-link: `/data/pig-modeling?ocpm=objects|workers|events` */
    this.route.queryParamMap.pipe(takeUntilDestroyed()).subscribe((params) => {
      const tab = params.get('ocpm');
      if (tab === 'objects' || tab === 'workers' || tab === 'events') {
        this.activeNav.set(tab);
      }
    });

    afterNextRender(() => this.stripLegacyDetailPreviewControls());
    effect(() => {
      this.activeNav();
      this.objectInspectorTab();
      this.workerInspectorTab();
      this.eventInspectorTab();
      this.selectedObjectId();
      this.selectedWorkerId();
      this.selectedEventId();
      queueMicrotask(() => this.stripLegacyDetailPreviewControls());
    });
  }

  protected readonly navItems: { id: string; label: string; disabled?: boolean }[] = [
    { id: 'dashboard', label: 'Dashboard', disabled: true },
    { id: 'objects', label: 'Objects' },
    { id: 'workers', label: 'Workers' },
    { id: 'events', label: 'Events' },
    { id: 'transformations', label: 'Transformations', disabled: true },
    { id: 'perspectives', label: 'Perspectives', disabled: true },
    { id: 'catalog', label: 'Catalog', disabled: true },
  ];

  protected readonly objects = signal<PigModelObject[]>([...PIG_MODEL_OBJECTS]);
  protected readonly workers = signal<PigModelWorker[]>([...PIG_MODEL_WORKERS]);
  protected readonly events = signal<PigModelEvent[]>([...PIG_MODEL_EVENTS]);

  private createBundleSequence = 0;

  protected readonly selectedObjectId = signal(PIG_MODEL_OBJECTS[0].id);
  protected readonly selectedWorkerId = signal(PIG_MODEL_WORKERS[0].id);
  protected readonly selectedEventId = signal(PIG_MODEL_EVENTS[0].id);
  protected readonly expandedClickstreamRows = signal<Record<string, boolean>>({});
  protected readonly expandedAttributeRows = signal<Record<string, boolean>>({});

  protected readonly loadState = signal<'loaded' | 'loading' | 'error'>('loaded');

  protected readonly objectInspectorTab = signal<PigObjectInspectorTab>('details');
  protected readonly objectEventSourceTab = signal<PigObjectEventSourceTab>('all');
  protected readonly objectEventSourceTabs: PigObjectEventSourceTab[] = [
    'all',
    'source-system',
    'task-mining',
    'agent-mining',
  ];
  protected readonly objectSearchQuery = signal('');
  protected readonly objectProcessFilter = signal<'all' | string>('all');
  protected readonly workerInspectorTab = signal<PigWorkerInspectorTab>('details');

  /** Workers list: Human / Agent toggles (click again to clear filter and show all). */
  protected readonly workerActorFilter = signal<'all' | 'HUMAN' | 'AGENT'>('all');

  /** Workers list: filter by Celonis process (from related object types). */
  protected readonly workerProcessFilter = signal<'all' | string>('all');

  /** Brief highlight on list + detail when filters change (left rail ↔ main columns). */
  protected readonly workerFilterCueActive = signal(false);

  /** Events tab filters and inspector state. */
  protected readonly eventActorFilter = signal<'all' | PigEventActorType>('all');
  protected readonly eventSearchQuery = signal('');
  protected readonly eventProcessFilter = signal<'all' | string>('all');
  protected readonly eventInspectorTab = signal<PigEventInspectorTab>('details');
  protected readonly eventFilterCueActive = signal(false);

  protected readonly workerProcessOptions = computed(() =>
    Array.from(
      new Set(
        this.workers().flatMap((w) =>
          w.relatedObjects
            .map((ro) => this.objects().find((o) => o.id === ro.objectId)?.customProcessLabel)
            .filter((s): s is string => !!s),
        ),
      ),
    ).sort(),
  );

  protected readonly objectProcessOptions = computed(() =>
    Array.from(new Set(this.objects().map((o) => o.customProcessLabel))).sort(),
  );

  protected readonly eventProcessOptions = computed(() =>
    Array.from(
      new Set(this.events().map((e) => e.metadata?.reference_process ?? 'Accounts payable')),
    ).sort(),
  );

  protected readonly filteredObjects = computed(() => {
    const processFilter = this.objectProcessFilter();
    const query = this.objectSearchQuery().trim().toLowerCase();
    return this.objects().filter((o) => {
      if (processFilter !== 'all' && o.customProcessLabel !== processFilter) {
        return false;
      }
      if (!query) {
        return true;
      }
      return (
        o.name.toLowerCase().includes(query) ||
        o.namespace.toLowerCase().includes(query) ||
        o.tags.some((tag) => tag.toLowerCase().includes(query))
      );
    });
  });

  protected readonly filteredEvents = computed(() => {
    const actor = this.eventActorFilter();
    const query = this.eventSearchQuery().trim().toLowerCase();
    const proc = this.eventProcessFilter();
    return this.events().filter((ev) => {
      if (actor !== 'all' && this.eventActorTypeForEvent(ev) !== actor) {
        return false;
      }
      if (proc !== 'all' && (ev.metadata?.reference_process ?? 'Accounts payable') !== proc) {
        return false;
      }
      if (!query) {
        return true;
      }
      return (
        ev.label.toLowerCase().includes(query) ||
        (ev.objectLabel ?? '').toLowerCase().includes(query) ||
        (ev.workerLabel ?? '').toLowerCase().includes(query) ||
        ev.category.toLowerCase().includes(query)
      );
    });
  });

  protected readonly eventListSections = computed(() => {
    const raw = this.filteredEvents();
    if (this.eventActorFilter() !== 'all') {
      return [{ subtitle: null as string | null, events: raw }];
    }
    const system = raw.filter((e) => this.eventActorTypeForEvent(e) === 'SYSTEM');
    const human = raw.filter((e) => this.eventActorTypeForEvent(e) === 'HUMAN');
    const agent = raw.filter((e) => this.eventActorTypeForEvent(e) === 'AGENT');
    const out: { subtitle: string | null; events: PigModelEvent[] }[] = [];
    if (system.length) out.push({ subtitle: 'System events', events: system });
    if (human.length) out.push({ subtitle: 'Human events', events: human });
    if (agent.length) out.push({ subtitle: 'Agent events', events: agent });
    return out;
  });

  /** Event totals per worker for list metadata and sorting. */
  protected readonly workerEventCounts = computed(() => {
    const workersById = new Map(this.workers().map((w) => [w.id, w] as const));
    const m = new Map<string, number>();
    for (const e of this.events()) {
      if (e.workerId) {
        const worker = workersById.get(e.workerId);
        if (worker?.actor_type === 'HUMAN' && !worker.taskMining) {
          continue;
        }
        m.set(e.workerId, (m.get(e.workerId) ?? 0) + 1);
      }
    }
    return m;
  });

  /** Middle column: grouped when both actor types visible; sorted by activity. */
  protected readonly workerListSections = computed(() => {
    const raw = this.filteredWorkers();
    const counts = this.workerEventCounts();
    const byActivity = (a: PigModelWorker, b: PigModelWorker) =>
      (counts.get(b.id) ?? 0) - (counts.get(a.id) ?? 0) ||
      a.primaryRole.localeCompare(b.primaryRole);
    const list = [...raw].sort(byActivity);
    if (this.workerActorFilter() !== 'all') {
      return [{ subtitle: null as string | null, workers: list }];
    }
    const humans = list.filter((w) => w.actor_type === 'HUMAN');
    const agents = list.filter((w) => w.actor_type === 'AGENT');
    const out: { subtitle: string | null; workers: PigModelWorker[] }[] = [];
    if (humans.length) {
      out.push({ subtitle: 'Human roles', workers: humans });
    }
    if (agents.length) {
      out.push({ subtitle: 'Agent roles', workers: agents });
    }
    return out;
  });

  protected selectNav(id: string): void {
    if (id === 'objects' || id === 'workers' || id === 'events') {
      this.activeNav.set(id);
    }
  }

  protected isNavActive(id: string): boolean {
    return this.activeNav() === id;
  }

  protected selectObject(id: string): void {
    this.selectedObjectId.set(id);
    this.objectInspectorTab.set('details');
    this.objectEventSourceTab.set('all');
  }

  protected setObjectSearchQuery(query: string): void {
    this.objectSearchQuery.set(query);
    this.syncObjectSelectionAfterFilter();
  }

  protected onObjectSearchInput(event: Event): void {
    const target = event.target as HTMLInputElement | null;
    this.setObjectSearchQuery(target?.value ?? '');
  }

  protected selectObjectProcessFilter(process: 'all' | string): void {
    this.objectProcessFilter.set(process);
    this.syncObjectSelectionAfterFilter();
  }

  protected isObjectProcessFilter(process: 'all' | string): boolean {
    return this.objectProcessFilter() === process;
  }

  protected selectWorker(id: string): void {
    this.selectedWorkerId.set(id);
    this.workerInspectorTab.set('details');
  }

  protected selectEvent(id: string): void {
    this.selectedEventId.set(id);
    this.eventInspectorTab.set('details');
  }

  protected toggleClickstreamRows(eventId: string): void {
    this.expandedClickstreamRows.update((state) => ({
      ...state,
      [eventId]: !state[eventId],
    }));
  }

  protected clickstreamRowsExpanded(eventId: string): boolean {
    return this.expandedClickstreamRows()[eventId] === true;
  }

  protected toggleAttributeRows(eventId: string): void {
    this.expandedAttributeRows.update((state) => ({
      ...state,
      [eventId]: !state[eventId],
    }));
  }

  protected attributeRowsExpanded(eventId: string): boolean {
    return this.expandedAttributeRows()[eventId] === true;
  }

  protected clickstreamEventCount(ev: PigModelEvent): number {
    return ev.metadata?.hierarchy.granular_events_operated ?? 0;
  }

  protected clickstreamSectionTitle(ev: PigModelEvent): string {
    const count = this.clickstreamEventCount(ev);
    if (count >= 10) {
      return 'High-volume clickstream samples';
    }
    return 'Clickstream samples';
  }

  protected clickstreamOverflowCount(ev: PigModelEvent): number {
    const count = this.clickstreamEventCount(ev);
    return Math.max(count - this.clickstreamEventRows(ev).length, 0);
  }

  protected clickstreamEventRows(ev: PigModelEvent): PigClickstreamRow[] {
    if (!ev.metadata) {
      return [];
    }
    const count = ev.metadata.hierarchy.granular_events_operated;
    const maxRows = 8;
    const rowCount = Math.min(count, maxRows);
    const examples = ev.metadata.clickstream_examples;
    if (examples && examples.length > 0) {
      return Array.from({ length: rowCount }, (_, idx) => {
        const example = examples[idx % examples.length];
        return {
          title: `${idx + 1}. ${example.title}`,
          userAction: example.userAction,
          applicationContext: example.applicationContext,
        };
      });
    }
    const label = ev.metadata.hierarchy.related_clickstream_event.label;
    const application = ev.metadata.hierarchy.related_clickstream_event.application;
    return Array.from({ length: rowCount }, (_, idx) => ({
      title: `${idx + 1}. ${label}`,
      userAction: 'Click',
      applicationContext: `${application} · default interaction`,
    }));
  }

  protected selectedObject(): PigModelObject {
    const inFiltered = this.filteredObjects().find((o) => o.id === this.selectedObjectId());
    if (inFiltered) {
      return inFiltered;
    }
    return this.filteredObjects()[0] ?? this.objects()[0];
  }

  protected selectedWorker(): PigModelWorker {
    const list = this.filteredWorkers();
    const id = this.selectedWorkerId();
    const hit = list.find((w) => w.id === id);
    return hit ?? list[0] ?? this.workers()[0];
  }

  /** Inverse of worker.relatedObjects — for object detail “metamodel” context. */
  protected workersForObject(objectId: string): PigModelWorker[] {
    return this.workers().filter((w) => w.relatedObjects.some((r) => r.objectId === objectId));
  }

  protected eventsForWorker(workerId: string): PigModelEvent[] {
    const worker = this.workers().find((w) => w.id === workerId);
    if (worker?.actor_type === 'HUMAN' && !worker.taskMining) {
      return [];
    }
    return this.events().filter((e) => e.workerId === workerId);
  }

  protected eventsForObject(o: PigModelObject): PigModelEvent[] {
    return this.events().filter((e) => e.objectLabel !== null && e.objectLabel.startsWith(o.name));
  }

  protected sourceCategoryForEvent(
    ev: PigModelEvent,
  ): Exclude<PigObjectEventSourceTab, 'all'> {
    if (ev.source === 'custom_agent') {
      return 'agent-mining';
    }
    if (ev.source === 'clustering' || ev.source === 'celonis_desktop') {
      return 'task-mining';
    }
    return 'source-system';
  }

  protected objectEventsForSelectedSource(o: PigModelObject): PigModelEvent[] {
    const sourceTab = this.objectEventSourceTab();
    const allEvents = this.eventsForObject(o);
    if (sourceTab === 'all') {
      return allEvents;
    }
    return allEvents.filter((ev) => this.sourceCategoryForEvent(ev) === sourceTab);
  }

  protected objectEventSourceCount(
    o: PigModelObject,
    sourceTab: PigObjectEventSourceTab,
  ): number {
    const allEvents = this.eventsForObject(o);
    if (sourceTab === 'all') {
      return allEvents.length;
    }
    return allEvents.filter((ev) => this.sourceCategoryForEvent(ev) === sourceTab).length;
  }

  protected selectObjectEventSourceTab(tab: PigObjectEventSourceTab): void {
    this.objectEventSourceTab.set(tab);
  }

  protected isObjectEventSourceTab(tab: PigObjectEventSourceTab): boolean {
    return this.objectEventSourceTab() === tab;
  }

  protected objectEventSourceLabel(tab: PigObjectEventSourceTab): string {
    if (tab === 'all') {
      return 'All';
    }
    if (tab === 'source-system') {
      return 'Source system';
    }
    if (tab === 'task-mining') {
      return 'Task mining';
    }
    return 'Agent mining';
  }

  protected eventSourceBadgeLabel(ev: PigModelEvent): string {
    const source = this.sourceCategoryForEvent(ev);
    if (source === 'source-system') {
      return 'Source system';
    }
    if (source === 'task-mining') {
      return 'Task mining';
    }
    return 'Agent mining';
  }

  protected eventSourceBadgeClass(ev: PigModelEvent): string {
    const source = this.sourceCategoryForEvent(ev);
    if (source === 'source-system') {
      return 'pig-page__source-pill pig-page__source-pill--source-system';
    }
    if (source === 'task-mining') {
      return 'pig-page__source-pill pig-page__source-pill--task-mining';
    }
    return 'pig-page__source-pill pig-page__source-pill--agent-mining';
  }

  protected selectObjectInspectorTab(tab: PigObjectInspectorTab): void {
    this.objectInspectorTab.set(tab);
    if (tab !== 'related-events') {
      this.objectEventSourceTab.set('all');
    }
  }

  protected selectWorkerInspectorTab(tab: PigWorkerInspectorTab): void {
    this.workerInspectorTab.set(tab);
  }

  protected onAddTaskMining(): void {
    void this.router.navigateByUrl('/data/pig-modeling/task-mining-project');
  }

  protected onAddAgentMining(): void {
    void this.router.navigateByUrl('/studio/process-task-mining-discovery');
  }

  /** Prototype CTA: append a linked object type, worker, and event so all three lists stay in sync. */
  protected onCreate(): void {
    const n = ++this.createBundleSequence;
    const objectId = `obj_create_${n}`;
    const objectName = `Created type ${n}`;
    const workerId = `worker_create_${n}`;
    const workerLabel = `Created agent ${n}`;
    const eventId = `ev_create_${n}`;

    this.objectSearchQuery.set('');
    this.objectProcessFilter.set('all');
    this.eventSearchQuery.set('');
    this.eventActorFilter.set('all');
    this.eventProcessFilter.set('all');
    this.workerActorFilter.set('all');
    this.workerProcessFilter.set('all');

    const createAgentAttributes: PigModelAttribute[] = [
      { name: 'trace_id', dataType: 'String', primaryKey: true, required: true },
      { name: 'span_id', dataType: 'String', required: true },
      { name: 'gen_ai.operation.name', dataType: 'String', required: true },
      { name: 'gen_ai.system', dataType: 'String' },
      { name: 'gen_ai.agent.name', dataType: 'String' },
      { name: 'session.id', dataType: 'String' },
    ];

    const newObject: PigModelObject = {
      id: objectId,
      name: objectName,
      namespace: 'prototype',
      tags: ['create', 'prototype'],
      customProcessLabel: 'Accounts payable',
      description: 'Object type added when you used Create on this prototype.',
      attributes: [
        { name: 'ExternalId', dataType: 'String', primaryKey: true },
        { name: 'DisplayName', dataType: 'String' },
      ],
    };

    const newWorker: PigModelWorker = {
      id: workerId,
      actor_id: `actor_create_${n}`,
      actor_type: 'AGENT',
      primaryRole: workerLabel,
      namespace: 'prototype',
      tags: ['create'],
      taskMining: false,
      agentMining: true,
      relatedObjects: [{ objectId, label: objectName }],
      description: 'Worker role added when you used Create on this prototype.',
      attributes: [
        { name: 'AgentId', dataType: 'String', primaryKey: true },
        { name: 'RoleDescription', dataType: 'String' },
      ],
    };

    const newEvent: PigModelEvent = {
      id: eventId,
      label: `create.prototype · bundle ${n}`,
      category: 'Subtask',
      objectLabel: `${objectName} · NEW-${n}`,
      workerId,
      workerLabel,
      timestamp: new Date().toISOString(),
      source: 'custom_agent',
      linkage: 'object_and_worker',
      attributes: createAgentAttributes,
      agentSignals: [{ name: 'create.prototype' }, { name: 'gen_ai.operation.name' }],
    };

    this.objects.update((list) => [...list, newObject]);
    this.workers.update((list) => [...list, newWorker]);
    this.events.update((list) => [...list, newEvent]);

    this.selectedObjectId.set(objectId);
    this.selectedWorkerId.set(workerId);
    this.selectedEventId.set(eventId);
    this.objectInspectorTab.set('details');
    this.workerInspectorTab.set('details');
    this.eventInspectorTab.set('details');
  }

  protected hasAgentConnectionDetails(ev: PigModelEvent): boolean {
    return this.sourceCategoryForEvent(ev) === 'agent-mining' && !!ev.workerId;
  }

  protected agentConnectionNameForEvent(ev: PigModelEvent): string {
    if (!ev.workerId) {
      return 'Unknown agent';
    }
    return this.workers().find((w) => w.id === ev.workerId)?.primaryRole ?? 'Unknown agent';
  }

  protected agentConnectionOriginForEvent(ev: PigModelEvent): string {
    if (ev.workerId === 'worker_agent_invoice') {
      return 'Cloud';
    }
    if (ev.workerId === 'worker_agent_three_way') {
      return 'Code';
    }
    if (ev.workerId === 'worker_agent_payment_release') {
      return 'Other tool';
    }
    return 'Unknown';
  }

  protected agentConnectionSystemForEvent(ev: PigModelEvent): string {
    if (ev.workerId === 'worker_agent_invoice') {
      return 'Celonis AI Hub';
    }
    if (ev.workerId === 'worker_agent_three_way') {
      return 'MatchAgent runtime';
    }
    if (ev.workerId === 'worker_agent_payment_release') {
      return 'TreasuryAssist integration';
    }
    return 'Unmapped integration';
  }

  protected eventActorTypeForEvent(ev: PigModelEvent): PigEventActorType {
    const src = this.sourceCategoryForEvent(ev);
    if (src === 'task-mining') {
      return 'HUMAN';
    }
    if (src === 'agent-mining') {
      return 'AGENT';
    }
    return 'SYSTEM';
  }

  protected eventActorLabel(type: PigEventActorType): string {
    if (type === 'HUMAN') {
      return 'Human';
    }
    if (type === 'AGENT') {
      return 'Agent';
    }
    return 'System';
  }

  protected eventActorBadgeClass(ev: PigModelEvent): string {
    return this.eventSourceBadgeClass(ev);
  }

  protected eventNamespaceForEvent(ev: PigModelEvent): string {
    if (ev.source === 'sap_s4') {
      return 'celonis';
    }
    const worker = ev.workerId ? this.workers().find((w) => w.id === ev.workerId) : null;
    return worker?.namespace ?? 'custom';
  }

  protected eventCelonisProcessTags(ev: PigModelEvent): string[] {
    const proc = ev.metadata?.reference_process ?? 'Accounts payable';
    return [proc];
  }

  protected toggleEventActorFilter(kind: PigEventActorType): void {
    const next = this.eventActorFilter() === kind ? 'all' : kind;
    this.eventActorFilter.set(next);
    this.syncEventSelectionAfterFilter();
    this.pulseEventFilterCue();
  }

  protected clearEventActorFilter(): void {
    if (this.eventActorFilter() === 'all') {
      return;
    }
    this.eventActorFilter.set('all');
    this.syncEventSelectionAfterFilter();
    this.pulseEventFilterCue();
  }

  protected isEventActorFilterActive(kind: 'all' | PigEventActorType): boolean {
    return this.eventActorFilter() === kind;
  }

  protected onEventSearchInput(event: Event): void {
    const target = event.target as HTMLInputElement | null;
    this.eventSearchQuery.set(target?.value ?? '');
    this.syncEventSelectionAfterFilter();
  }

  protected selectEventProcessFilter(p: 'all' | string): void {
    this.eventProcessFilter.set(p);
    this.syncEventSelectionAfterFilter();
    this.pulseEventFilterCue();
  }

  protected isEventProcessFilter(p: 'all' | string): boolean {
    return this.eventProcessFilter() === p;
  }

  protected selectEventInspectorTab(tab: PigEventInspectorTab): void {
    this.eventInspectorTab.set(tab);
  }

  protected isEventInspector(tab: PigEventInspectorTab): boolean {
    return this.eventInspectorTab() === tab;
  }

  private syncEventSelectionAfterFilter(): void {
    const list = this.filteredEvents();
    if (list.length > 0 && !list.some((e) => e.id === this.selectedEventId())) {
      this.selectedEventId.set(list[0].id);
      this.eventInspectorTab.set('details');
    }
  }

  private pulseEventFilterCue(): void {
    this.eventFilterCueActive.set(false);
    requestAnimationFrame(() => {
      this.eventFilterCueActive.set(true);
      window.setTimeout(() => this.eventFilterCueActive.set(false), 520);
    });
  }

  protected canStartTaskMiningCapture(w: PigModelWorker): boolean {
    return w.actor_type === 'HUMAN' && !w.taskMining;
  }

  protected isObjectInspector(tab: PigObjectInspectorTab): boolean {
    return this.objectInspectorTab() === tab;
  }

  protected isWorkerInspector(tab: PigWorkerInspectorTab): boolean {
    return this.workerInspectorTab() === tab;
  }

  protected workerKindLabel(type: PigModelWorker['actor_type']): string {
    return type === 'HUMAN' ? 'Human' : 'Agent';
  }

  protected filteredWorkers(): PigModelWorker[] {
    const actor = this.workerActorFilter();
    const proc = this.workerProcessFilter();
    return this.workers().filter((w) => {
      if (actor !== 'all' && w.actor_type !== actor) {
        return false;
      }
      if (proc === 'all') {
        return true;
      }
      return w.relatedObjects.some(
        (ro) => this.objects().find((o) => o.id === ro.objectId)?.customProcessLabel === proc,
      );
    });
  }

  protected clearWorkerActorFilter(): void {
    if (this.workerActorFilter() === 'all') {
      return;
    }
    this.workerActorFilter.set('all');
    this.syncWorkerSelectionAfterFilter();
    this.pulseWorkerFilterCue();
  }

  /** Toggle Human / Agent; clicking the active filter again shows all workers. */
  protected toggleWorkerActorFilter(kind: 'HUMAN' | 'AGENT'): void {
    const next = this.workerActorFilter() === kind ? 'all' : kind;
    this.workerActorFilter.set(next);
    this.syncWorkerSelectionAfterFilter();
    this.pulseWorkerFilterCue();
  }

  protected isWorkerActorFilterActive(kind: 'HUMAN' | 'AGENT'): boolean {
    return this.workerActorFilter() === kind;
  }

  protected selectWorkerProcessFilter(p: 'all' | string): void {
    this.workerProcessFilter.set(p);
    this.syncWorkerSelectionAfterFilter();
    this.pulseWorkerFilterCue();
  }

  protected isWorkerProcessFilter(p: 'all' | string): boolean {
    return this.workerProcessFilter() === p;
  }

  /** Distinct process labels for the selected worker (for preview chips). */
  protected workerProcessLabels(w: PigModelWorker): string[] {
    const labels = w.relatedObjects
      .map((ro) => this.objects().find((o) => o.id === ro.objectId)?.customProcessLabel)
      .filter((s): s is string => !!s);
    return Array.from(new Set(labels)).sort();
  }

  protected workerEventCount(workerId: string): number {
    return this.workerEventCounts().get(workerId) ?? 0;
  }

  protected workerAttributes(w: PigModelWorker): PigModelAttribute[] {
    return w.attributes;
  }

  protected workerProcessTypeCount(w: PigModelWorker): number {
    return this.workerProcessLabels(w).length;
  }

  private pulseWorkerFilterCue(): void {
    this.workerFilterCueActive.set(false);
    requestAnimationFrame(() => {
      this.workerFilterCueActive.set(true);
      window.setTimeout(() => this.workerFilterCueActive.set(false), 520);
    });
  }

  private syncWorkerSelectionAfterFilter(): void {
    const list = this.filteredWorkers();
    if (list.length > 0 && !list.some((w) => w.id === this.selectedWorkerId())) {
      this.selectedWorkerId.set(list[0].id);
    }
  }

  private syncObjectSelectionAfterFilter(): void {
    const list = this.filteredObjects();
    if (list.length > 0 && !list.some((o) => o.id === this.selectedObjectId())) {
      this.selectedObjectId.set(list[0].id);
      this.objectInspectorTab.set('details');
    }
  }

  protected selectedEvent(): PigModelEvent {
    return this.events().find((e) => e.id === this.selectedEventId()) ?? this.events()[0];
  }

  protected linkageVariant(
    linkage: PigModelEvent['linkage'],
  ): 'success' | 'warning' | 'neutral' {
    if (linkage === 'object_and_worker') {
      return 'success';
    }
    if (linkage === 'worker_only') {
      return 'warning';
    }
    return 'neutral';
  }

  protected linkageLabel(linkage: PigModelEvent['linkage']): string {
    if (linkage === 'object_and_worker') {
      return 'Object + worker';
    }
    if (linkage === 'worker_only') {
      return 'Worker only';
    }
    return 'Object only';
  }

  /** Returns the object type name only, stripping any case instance suffix (e.g. "AP Case · CASE-20041" → "AP Case"). */
  protected eventObjectTypeName(ev: PigModelEvent): string {
    const label = ev.objectLabel;
    if (!label) {
      return '';
    }
    return label.split(' · ')[0].trim();
  }

  protected formatTs(iso: string): string {
    try {
      return new Date(iso).toLocaleString(undefined, {
        dateStyle: 'medium',
        timeStyle: 'short',
      });
    } catch {
      return iso;
    }
  }

  /** Remove legacy detail toolbar nodes if an old bundle or extension injects them. */
  private stripLegacyDetailPreviewControls(): void {
    const root = this.hostRef.nativeElement;
    if (!root?.isConnected) {
      return;
    }
    root.querySelectorAll('.pig-page__detail-toolbar').forEach((el: Element) => el.remove());
    root.querySelectorAll('button, a[role="button"], [ceButton]').forEach((el: Element) => {
      const t = (el.textContent ?? '').trim();
      if (t === 'Data preview' || t === 'View in Graph') {
        el.remove();
      }
    });
  }

}
