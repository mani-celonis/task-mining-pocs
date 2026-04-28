import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { timer } from 'rxjs';
import {
  CeButtonModule,
  CeInfoModule,
  CeInputGroupModule,
  CeKpiModule,
  CeMainContentModule,
  CePlaceholderModule,
  CeSkeletonModule,
  CeSelectModule,
  CeStatusIndicatorModule,
  CeTableGridModule,
  CeTabsModule,
} from '@celonis/emotion';
import {
  AUTOMATION_SUMMARY_KPIS,
  FINANCE_BUSINESS_OBJECTS,
  PRIORITIZED_ACTIVITIES,
  PROCESS_HEADLINE_METRICS,
  PROCESS_WORKERS,
  TASK_DISCOVERY_ROWS,
  TASK_DISCOVERY_STATS,
  type AiPotentialLevel,
  type FinanceBusinessObject,
  type PrioritizedActivityRow,
  type ProcessStep,
} from './task-mining-analysis.fixtures';

type LoadState = 'loading' | 'ready' | 'error';

@Component({
  selector: 'app-task-mining-analysis',
  imports: [
    FormsModule,
    RouterLink,
    CeMainContentModule,
    CeButtonModule,
    CeInfoModule,
    CeInputGroupModule,
    CeSelectModule,
    CeKpiModule,
    CeTabsModule,
    CeTableGridModule,
    CeStatusIndicatorModule,
    CeSkeletonModule,
    CePlaceholderModule,
  ],
  templateUrl: './task-mining-analysis.html',
  styleUrl: './task-mining-analysis.scss',
})
export class TaskMiningAnalysisPage {
  private readonly destroyRef = inject(DestroyRef);
  protected readonly loadState = signal<LoadState>('loading');
  protected readonly headlineMetrics = PROCESS_HEADLINE_METRICS;
  protected readonly summaryKpis = AUTOMATION_SUMMARY_KPIS;
  protected readonly activities = PRIORITIZED_ACTIVITIES;
  protected readonly taskDiscoveryStats = TASK_DISCOVERY_STATS;
  protected readonly taskDiscoveryRows = TASK_DISCOVERY_ROWS;
  protected readonly workerOptions = PROCESS_WORKERS;
  protected readonly financeBusinessObjects = FINANCE_BUSINESS_OBJECTS;
  protected selectedWorkerId = 'all';
  protected readonly summarySkeletonSlots = [0, 1, 2, 3, 4, 5] as const;

  constructor() {
    timer(480).pipe(takeUntilDestroyed(this.destroyRef)).subscribe(() => this.loadState.set('ready'));
  }

  protected retryLoad(): void {
    this.loadState.set('loading');
    timer(400).pipe(takeUntilDestroyed(this.destroyRef)).subscribe(() => this.loadState.set('ready'));
  }

  protected aiVariant(level: AiPotentialLevel): 'success' | 'warning' | 'error' {
    if (level === 'high') return 'success';
    if (level === 'medium') return 'warning';
    return 'error';
  }

  protected aiLabel(level: AiPotentialLevel): string {
    if (level === 'high') return 'High';
    if (level === 'medium') return 'Medium';
    return 'Low';
  }

  protected manualWithRate(row: PrioritizedActivityRow): string {
    return `${row.manualExecutionsLabel} (${row.automationRatePct}%)`;
  }

  protected tasksSubtasks(row: PrioritizedActivityRow): string {
    return `${row.taskCount} / ${row.subtaskCount}`;
  }

  protected processStepsFor(object: FinanceBusinessObject): readonly ProcessStep[] {
    if (this.selectedWorkerId === 'all') return object.steps;
    return object.steps.filter((step) => step.ownerIds.includes(this.selectedWorkerId));
  }

  protected workerLabel(workerId: string): string {
    return this.workerOptions.find((w) => w.id === workerId)?.label ?? workerId;
  }

  protected showDemoError(): void {
    this.loadState.set('error');
  }
}
