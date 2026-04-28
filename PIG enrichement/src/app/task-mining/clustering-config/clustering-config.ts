import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import {
  CeButtonModule,
  CeInfoModule,
  CeInputGroupModule,
  CeMainContentModule,
  CeSelectModule,
} from '@celonis/emotion';

import { ClusteringFlowService } from '../clustering-flow.service';

@Component({
  selector: 'app-clustering-config',
  imports: [
    FormsModule,
    CeMainContentModule,
    CeInputGroupModule,
    CeSelectModule,
    CeButtonModule,
    CeInfoModule,
  ],
  templateUrl: './clustering-config.html',
  styleUrl: './clustering-config.scss',
})
export class ClusteringConfigPage implements OnInit {
  private readonly router = inject(Router);
  protected readonly flow = inject(ClusteringFlowService);

  protected name = '';
  protected goal = '';
  protected objectEventId = '';
  protected dataRangeId = '';

  ngOnInit(): void {
    const d = this.flow.draft();
    this.name = d.name;
    this.goal = d.goal;
    this.objectEventId = d.objectEventId;
    this.dataRangeId = d.dataRangeId;
  }

  protected get showGoalHint(): boolean {
    return this.goal.trim().length === 0;
  }

  protected runAiClustering(): void {
    this.flow.patchDraft({
      name: this.name,
      goal: this.goal,
      objectEventId: this.objectEventId,
      dataRangeId: this.dataRangeId,
    });
    this.flow.generatePreviewSample();
    void this.router.navigateByUrl('/task-mining/clustering/preview');
  }
}
