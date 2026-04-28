import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import {
  CeButtonModule,
  CeInfoModule,
  CeMainContentModule,
  CePanelModule,
} from '@celonis/emotion';

@Component({
  selector: 'app-task-mining-landing',
  imports: [RouterLink, CeMainContentModule, CeButtonModule, CePanelModule, CeInfoModule],
  templateUrl: './task-mining-landing.html',
  styleUrl: './task-mining-landing.scss',
})
export class TaskMiningLanding {
  readonly highlights = [
    {
      title: 'Automated discovery',
      body: 'Reconstruct how work really happens from system events—without manual workshops.',
    },
    {
      title: 'Standardized views',
      body: 'Compare variants, throughput, and rework with a shared task lexicon across teams.',
    },
    {
      title: 'Action-ready signals',
      body: 'Spot friction and compliance gaps early so you can prioritize improvements with evidence.',
    },
  ] as const;

  readonly metrics = [
    { value: '360°', label: 'Process visibility' },
    { value: '< 2 wks', label: 'Typical time-to-insight' },
    { value: 'Enterprise', label: 'Scale & governance' },
  ] as const;
}
