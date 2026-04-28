import { Component, inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {
  CeButtonModule,
  CeInfoModule,
  CeKpiModule,
  CeMainContentModule,
  CeTableGridModule,
} from '@celonis/emotion';

import { ClusteringFlowService } from '../clustering-flow.service';

@Component({
  selector: 'app-clustering-preview',
  imports: [
    CeMainContentModule,
    CeInfoModule,
    CeKpiModule,
    CeTableGridModule,
    CeButtonModule,
  ],
  templateUrl: './clustering-preview.html',
  styleUrl: './clustering-preview.scss',
})
export class ClusteringPreviewPage implements OnInit {
  private readonly router = inject(Router);
  protected readonly flow = inject(ClusteringFlowService);

  ngOnInit(): void {
    if (!this.flow.preview()) {
      void this.router.navigateByUrl('/task-mining/clustering/configure');
    }
  }

  protected improveInstruction(): void {
    void this.router.navigateByUrl('/task-mining/clustering/configure');
  }

  protected confirmAndRun(): void {
    this.flow.confirmRunOnFullDataset();
    void this.router.navigateByUrl('/data/pig-modeling/task-mining-project');
  }
}
