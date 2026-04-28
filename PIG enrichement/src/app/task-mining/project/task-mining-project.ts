import { Component, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import {
  CeButtonModule,
  CeInfoModule,
  CeMainContentModule,
  CeStatusIndicatorModule,
  CeTableGridModule,
} from '@celonis/emotion';

import { ClusteringFlowService } from '../clustering-flow.service';
import type { ClusteringRun } from '../clustering.models';

@Component({
  selector: 'app-task-mining-project',
  imports: [
    RouterLink,
    CeMainContentModule,
    CeButtonModule,
    CeTableGridModule,
    CeStatusIndicatorModule,
    CeInfoModule,
  ],
  templateUrl: './task-mining-project.html',
  styleUrl: './task-mining-project.scss',
})
export class TaskMiningProject {
  private readonly router = inject(Router);
  protected readonly flow = inject(ClusteringFlowService);

  protected formatDate(iso: string): string {
    try {
      return new Date(iso).toLocaleString(undefined, {
        dateStyle: 'medium',
        timeStyle: 'short',
      });
    } catch {
      return iso;
    }
  }

  protected createNew(): void {
    this.flow.resetDraftForNewRun();
    void this.router.navigateByUrl('/task-mining/clustering/configure');
  }

  protected openRun(run: ClusteringRun): void {
    if (run.status !== 'complete') {
      return;
    }
    // Prototype: no detail route yet
    void this.router.navigateByUrl('/task-mining/clustering/configure');
  }
}
